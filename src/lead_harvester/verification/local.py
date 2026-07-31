from __future__ import annotations

import asyncio
import re

from lead_harvester.models.verification import VerificationStatus
from .base import EmailVerificationProvider, VerificationOutcome

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

ROLE_LOCAL_PARTS = {
    "info", "admin", "administrator", "office", "contact", "support",
    "sales", "hello", "hr", "webmaster", "postmaster", "noreply", "no-reply",
}

DISPOSABLE_DOMAINS = {
    "mailinator.com", "10minutemail.com", "guerrillamail.com", "tempmail.com",
    "yopmail.com", "trashmail.com", "throwawaymail.com",
}


class LocalHeuristicProvider(EmailVerificationProvider):
    """
    Free, always-available fallback: syntax validation, role-account and
    known-disposable-domain detection, and an MX record lookup. This can only
    confirm a domain CAN receive mail, not that a specific mailbox exists --
    for real deliverability confirmation, configure a licensed provider (see
    licensed.py).
    """

    name = "local_heuristic"

    async def verify(self, email: str) -> VerificationOutcome:
        email = (email or "").strip().lower()

        if not EMAIL_RE.match(email):
            return VerificationOutcome(
                provider=self.name,
                status=VerificationStatus.INVALID,
                raw_response={"reason": "malformed"},
            )

        local_part, _, domain = email.partition("@")
        is_role_account = local_part in ROLE_LOCAL_PARTS
        is_disposable = domain in DISPOSABLE_DOMAINS

        mx_found = await self._has_mx_record(domain)

        if mx_found is False:
            status = VerificationStatus.INVALID
        elif is_disposable or is_role_account:
            status = VerificationStatus.RISKY
        elif mx_found is True:
            status = VerificationStatus.VALID
        else:
            status = VerificationStatus.UNKNOWN

        return VerificationOutcome(
            provider=self.name,
            status=status,
            is_disposable=is_disposable,
            is_role_account=is_role_account,
            mx_found=mx_found,
            raw_response={"domain": domain},
        )

    async def _has_mx_record(self, domain: str) -> bool | None:
        try:
            import dns.resolver
        except ImportError:
            return None

        loop = asyncio.get_running_loop()
        try:
            answers = await loop.run_in_executor(None, dns.resolver.resolve, domain, "MX")
            return len(answers) > 0
        except dns.resolver.NXDOMAIN:
            return False
        except dns.resolver.NoAnswer:
            # Some domains accept mail via an A record with no MX; inconclusive either way.
            return None
        except Exception:
            return None
