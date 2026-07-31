"""
Declares, per SourceType, the legal/authorization basis this codebase
claims for collecting data that way -- see docs/ROADMAP.md module 11's
source_policy sub-concern. A static registry (not DB-backed): this is a
policy DECLARATION reviewed and changed by people, not runtime data a
service mutates.

This module does not enforce anything by itself -- see
compliance/channel_eligibility.py and services/compliance_service.py for
the parts that actually gate behavior (suppression, deletion). Its job is
visibility: make the authorization basis for every connector explicit and
inspectable, including where that basis is contested, rather than
implicit or silently assumed.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass

from lead_harvester.models.source import SourceType


class AuthorizationBasis(str, enum.Enum):
    LICENSED_API = "licensed_api"
    AUTHORIZED_IMPORT = "authorized_import"
    MANUAL_RESEARCH = "manual_research"
    PUBLIC_WEB_CRAWL = "public_web_crawl"
    ACCOUNT_AUTOMATION = "account_automation"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass(frozen=True)
class SourcePolicy:
    authorization_basis: AuthorizationBasis
    # True if this source's own terms of service or applicable law
    # requires telling contacted individuals/institutions how their data
    # was obtained -- a policy fact for a human to act on (e.g. in an
    # email footer), not something this module enforces.
    requires_disclosure: bool
    notes: str


# docs/ROADMAP.md's own "Source Connectors" module description states:
# "Unauthorized scraping/account automation is out of bounds; authorized
# imports and licensed/manual research are the accepted pattern." LINKEDIN
# below is the one entry that does not meet that bar -- sources/
# linkedin_stealth.py and sources/account_farm.py implement exactly the
# account automation that sentence rules out. This registry states that
# contradiction plainly rather than either quietly calling it compliant
# (it is not, by this repo's own documented standard) or unilaterally
# disabling a working, relied-upon feature (a business decision outside
# what a data model can decide for the people who run this system).
# Whether to keep, restrict, or replace LINKEDIN's collection method is a
# decision for whoever owns that tradeoff -- this entry exists so the
# question can't be missed, not to answer it.
SOURCE_POLICIES: dict[SourceType, SourcePolicy] = {
    SourceType.GOOGLE_PLACES: SourcePolicy(
        authorization_basis=AuthorizationBasis.LICENSED_API,
        requires_disclosure=False,
        notes="Google Places API, used under Google's commercial API terms.",
    ),
    SourceType.WEBSITE: SourcePolicy(
        authorization_basis=AuthorizationBasis.PUBLIC_WEB_CRAWL,
        requires_disclosure=False,
        notes=(
            "Crawls publicly published pages (ingestion/web_crawler.py). No account "
            "automation or authentication bypass involved."
        ),
    ),
    SourceType.AUTHORIZED_IMPORT: SourcePolicy(
        authorization_basis=AuthorizationBasis.AUTHORIZED_IMPORT,
        requires_disclosure=False,
        notes="Bulk CSV import of licensed or manually-sourced data (sources/authorized_imports.py).",
    ),
    SourceType.MANUAL: SourcePolicy(
        authorization_basis=AuthorizationBasis.MANUAL_RESEARCH,
        requires_disclosure=False,
        notes="Human-entered leads (cold call, referral, field visit) via api/routes/manual_leads.py.",
    ),
    SourceType.LINKEDIN: SourcePolicy(
        authorization_basis=AuthorizationBasis.ACCOUNT_AUTOMATION,
        requires_disclosure=True,
        notes=(
            "CONTESTED: sources/linkedin_stealth.py and sources/account_farm.py automate "
            "browser sessions against real LinkedIn accounts (stealth fingerprinting, CAPTCHA "
            "solving, human-emulated timing) -- this is the 'unauthorized scraping/account "
            "automation' docs/ROADMAP.md's own Source Connectors section says is 'out of "
            "bounds'. Documented here, not hidden or silently resolved; deciding whether to "
            "keep operating it is outside this module's authority."
        ),
    ),
    SourceType.TELEGRAM: SourcePolicy(
        authorization_basis=AuthorizationBasis.NOT_IMPLEMENTED,
        requires_disclosure=False,
        notes="Planned (docs/ROADMAP.md module 2) -- no connector exists yet.",
    ),
    SourceType.YANDEX: SourcePolicy(
        authorization_basis=AuthorizationBasis.NOT_IMPLEMENTED,
        requires_disclosure=False,
        notes="Planned (docs/ROADMAP.md module 2) -- no connector exists yet.",
    ),
    SourceType.APPLE_MAPS: SourcePolicy(
        authorization_basis=AuthorizationBasis.NOT_IMPLEMENTED,
        requires_disclosure=False,
        notes="Planned (docs/ROADMAP.md module 2) -- no connector exists yet.",
    ),
}


def get_source_policy(source_type: SourceType) -> SourcePolicy:
    return SOURCE_POLICIES[source_type]


def contested_sources() -> list[SourceType]:
    """SourceTypes whose own declared policy admits they don't meet this repo's stated bar."""
    return [
        source_type
        for source_type, policy in SOURCE_POLICIES.items()
        if policy.authorization_basis == AuthorizationBasis.ACCOUNT_AUTOMATION
    ]
