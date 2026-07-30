"""
Whether a specific normalized contact value may currently be contacted on
a specific channel -- see docs/ROADMAP.md module 11's channel_eligibility
sub-concern. Pure function over an already-looked-up SuppressionEntry (or
None); services/compliance_service.py does the actual DB lookup.
"""

from __future__ import annotations

from dataclasses import dataclass

from lead_harvester.models.compliance import SuppressionEntry


@dataclass(frozen=True)
class EligibilityResult:
    eligible: bool
    reason: str


def is_channel_eligible(channel: str, suppression: SuppressionEntry | None) -> EligibilityResult:
    """
    Ineligible if a suppression entry exists for this contact value and
    either applies to every channel (suppression.channel is None -- a
    blanket "never contact this person again") or specifically names this
    channel (e.g. suppressed for "email" but still fine to call).
    """
    if suppression is None:
        return EligibilityResult(eligible=True, reason="not suppressed")

    if suppression.channel is None or suppression.channel == channel:
        return EligibilityResult(
            eligible=False,
            reason=f"suppressed ({suppression.reason.value}): {suppression.note}".rstrip(": "),
        )

    return EligibilityResult(
        eligible=True, reason=f"suppressed for {suppression.channel!r} only, not {channel!r}"
    )
