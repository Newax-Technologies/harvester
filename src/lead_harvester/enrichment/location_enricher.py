"""
Parses a crawled page's structured address signal (JSON-LD PostalAddress,
via extractors.py::extract_page_identity) into Branch-ready city/
country_code fields -- see docs/ROADMAP.md module 6 ("Enrichment").

canonical/merger.py's WEBSITE branch of display_fields has never supplied
city/country_code at all (its own comment: "every other source's
display_fields returns "" for both") -- not because the data isn't there,
but because extract_page_identity only ever joined the JSON-LD address's
locality/region/country into one free-text `location` string for display,
discarding the individual addressLocality/addressCountry components. This
is that missing step: reuses resolution/normalize.py's country_to_iso2 --
the same free-text-country -> ISO-2 table AUTHORIZED_IMPORT rows already
go through -- so a web-crawled institution's Branch gets the same
structured city/country_code an authorized-import row does, instead of
always falling through to _build_branch's UNKNOWN sentinel.
"""

from __future__ import annotations

from lead_harvester.resolution.normalize import country_to_iso2


def enrich_location(address_locality: str, address_country: str) -> tuple[str, str]:
    """
    Returns (city, country_code). `city` is the locality as-extracted,
    trimmed, or "" if blank. `country_code` is the ISO-2 code
    country_to_iso2 resolves `address_country` to, or "" if blank or
    unrecognized -- never guessed.
    """
    city = (address_locality or "").strip()
    country_code = country_to_iso2(address_country or "") or ""
    return city, country_code
