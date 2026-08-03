#!/usr/bin/env python3
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TAX = ROOT / "docs" / "taxonomy"
OUT = TAX / "keywords"
DOMAIN_OUT = OUT / "domain-keywords"

STOP = {
    "and", "of", "the", "for", "to", "in", "with", "or", "services",
    "service", "products", "product", "systems", "system",
}


def ascii_text(value: str) -> str:
    return unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode()


def unique(values: list[str], limit: int) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in values:
        clean = re.sub(r"\s+", " ", value.strip())
        key = clean.casefold()
        if clean and key not in seen:
            seen.add(key)
            result.append(clean)
        if len(result) >= limit:
            break
    return result


def name_variants(name: str) -> list[str]:
    value = ascii_text(name).strip()
    variants = [value, value.replace(" and ", " & "), value.replace("&", "and"), value.replace("-", " ")]
    for tail in (" Services", " Service", " Products", " Product", " Systems", " System", " Equipment", " Operations"):
        if value.endswith(tail):
            variants.append(value[: -len(tail)])
    if " and " in value:
        parts = value.split(" and ")
        if len(parts) == 2:
            variants.extend(parts)
    return unique(variants, 6)


def activity_keywords(name: str) -> list[str]:
    low = ascii_text(name).lower()
    values = [v.lower() for v in name_variants(name)]
    if low.endswith("ing") and len(low) > 5:
        stem = low[:-3]
        values.append(stem + "e" if stem.endswith("at") else stem)
    values.extend([
        f"{low} services", f"{low} operations", f"{low} provider",
        f"we provide {low}", f"our {low} services", f"{low} department",
    ])
    return unique(values, 10)


def domain_keywords(name: str) -> list[str]:
    low = ascii_text(name).lower()
    values = [v.lower() for v in name_variants(name)]
    values.append(re.sub(r"\([^)]*\)", "", low).strip())
    tokens = [token for token in re.findall(r"[a-z0-9]+", low) if token not in STOP]
    if 1 <= len(tokens) <= 4:
        values.append(" ".join(tokens))
    return unique(values, 8)


def parse_activities() -> list[tuple[str, str, str]]:
    activities: list[tuple[str, str, str]] = []
    family = ""
    files = sorted(TAX.glob("activity-registry-part-*.md"))
    if not files:
        files = [TAX / "activity-registry.md"]
    for path in files:
        for line in path.read_text(encoding="utf-8").splitlines():
            family_match = re.match(r"^###(?:\s+\d+(?:\.\d+)*)?\s+(.+)$", line)
            if family_match:
                family = family_match.group(1).strip()
            row = re.match(r"^\| `(ACT-[A-Z]+-\d+)` \| ([^|]+) \|", line)
            if row:
                item = (row.group(1), row.group(2).strip(), family)
                if item not in activities:
                    activities.append(item)
    return activities


def parse_sector_domains() -> list[tuple[str, str, list[tuple[str, str]]]]:
    sectors: list[tuple[str, str, list[tuple[str, str]]]] = []
    for path in sorted(TAX.glob("*-domain-registry.md")):
        if path.name.startswith("broad-"):
            continue
        text = path.read_text(encoding="utf-8")
        heading = re.search(r"^# Harvester (.+?) Product and Service Domain Registry$", text, re.M)
        sector = heading.group(1) if heading else path.stem.replace("-domain-registry", "").replace("-", " ").title()
        domains: list[tuple[str, str]] = []
        for line in text.splitlines():
            row = re.match(r"^\| `([A-Z0-9-]+)` \| ([^|]+) \|?$", line)
            if row and not row.group(1).startswith(("ACT-", "BS-")):
                domains.append((row.group(1), row.group(2).strip()))
        if domains:
            slug = path.name.replace("-domain-registry.md", "")
            sectors.append((slug, sector, domains))
    return sectors


def ambiguity_controls(name: str) -> str:
    low = name.lower()
    if any(term in low for term in ("education", "training", "course", "school", "university", "college")):
        return "`unrelated jobs`; `definition-only result`; `student assignment`"
    if any(term in low for term in ("retail", "store", "shop", "marketplace", "e-commerce")):
        return "`unrelated jobs`; `definition-only result`; `single consumer listing`"
    if any(term in low for term in ("staffing", "recruitment", "human resources")):
        return "`definition-only result`; `unrelated training`; `single candidate profile`"
    return "`jobs`; `course`; `definition`; `consumer-only result`"


def write_activity_parts(activities: list[tuple[str, str, str]]) -> None:
    for index, start in enumerate(range(0, len(activities), 175), 1):
        part = activities[start : start + 175]
        lines = [
            f"# Harvester Canonical Activity Keywords — Part {index}", "",
            "Status: **Proposed**  ", "Version: **1.0**  ", "Date: **4 August 2026**  ",
            "Implementation status: **Not implemented**", "",
            "This file defines default discovery terms for canonical business activities. Terms identify possible activity evidence only. They do not prove that an organization performs the activity.", "",
            "| Activity code | Activity | Family | Default activity terms and phrases |",
            "| --- | --- | --- | --- |",
        ]
        for code, name, family in part:
            keywords = "; ".join(f"`{term}`" for term in activity_keywords(name))
            lines.append(f"| `{code}` | {name} | {family} | {keywords} |")
        lines.extend(["", "## Interpretation rule", "", "An activity term should normally be evaluated with a selected domain term, organization identity, source reliability, and negative context. A phrase such as ‘manufacturing course’ is not evidence that the publisher manufactures anything.", ""])
        (OUT / f"activity-keywords-part-{index}.md").write_text("\n".join(lines), encoding="utf-8")


def write_domain_files(sectors: list[tuple[str, str, list[tuple[str, str]]]]) -> None:
    DOMAIN_OUT.mkdir(parents=True, exist_ok=True)
    for slug, sector, domains in sectors:
        lines = [
            f"# Harvester {sector} Domain Keyword Registry", "",
            "Status: **Proposed**  ", "Version: **1.0**  ", "Date: **4 August 2026**  ",
            "Implementation status: **Not implemented**", "",
            f"This file defines default domain-identification terms for all **{len(domains)}** canonical domains in `{sector}`. Domain keywords identify what an organization deals with; activity keywords identify what it does.", "",
            "| Domain code | Domain | Primary domain terms and aliases | Default ambiguity controls |",
            "| --- | --- | --- | --- |",
        ]
        for code, name in domains:
            keywords = "; ".join(f"`{term}`" for term in domain_keywords(name))
            lines.append(f"| `{code}` | {name} | {keywords} | {ambiguity_controls(name)} |")
        lines.extend(["", "## Composition rule", "", "A domain match alone does not establish the target activity. Harvester must combine the domain profile with the separately approved activity profile and inspect source context.", "", "## Local terminology", "", "Urdu, Roman Urdu, abbreviations, local trade names, spelling variants, and jurisdiction-specific terminology must be maintained in separately versioned locale overlays.", ""])
        (DOMAIN_OUT / f"{slug}-domain-keywords.md").write_text("\n".join(lines), encoding="utf-8")


def write_indexes(activities, sectors) -> None:
    total_domains = sum(len(domains) for _, _, domains in sectors)
    registry = [
        "# Harvester Keyword Registry and Composition Rules", "",
        "Status: **Proposed**  ", "Version: **1.0**  ", "Date: **4 August 2026**  ",
        "Implementation status: **Not implemented**", "",
        f"This registry defines controlled keyword profiles for Harvester's **{total_domains} canonical product or service domains** and **{len(activities)} canonical business activities**. Keywords are discovery aids and evidence-strengthening signals. They never independently prove an activity, service gap, opportunity, or lead qualification.", "",
        "## Locked composition model", "", "```text", "Selected broad sector", "+ selected domain keyword profile", "+ selected activity keyword profile", "+ provider-selected service keyword profile", "+ source and geography constraints", "+ exclusions and negative context", "= search and evidence profile", "```", "",
        "Domain and activity keywords remain separate. Service-gap and buying-intent keywords belong to active provider service profiles.", "",
        "## Keyword classes", "", "`DOMAIN_TERM`; `DOMAIN_ALIAS`; `ACTIVITY_TERM`; `ACTIVITY_PHRASE`; `ORGANIZATION_SIGNAL`; `PROBLEM_SIGNAL`; `BUYING_SIGNAL`; `EXISTING_SOLUTION`; `EXCLUSION`; `LOCAL_TERMINOLOGY`", "",
        "## Match modes", "", "`EXACT`; `PHRASE`; `SEMANTIC`; `ENTITY`; reviewed `REGEX`", "",
        "## Universal safeguards", "",
        "1. A keyword match creates a candidate evidence signal, not a classification fact.",
        "2. Domain and activity terms must normally co-occur within bounded source context.",
        "3. Search snippets alone are insufficient evidence.",
        "4. Duplicate sources do not increase confidence.",
        "5. ‘Not found’ is not ‘absent’ without sufficient coverage.",
        "6. Employment, training, dictionary, news-only, marketplace, and consumer contexts require explicit handling.",
        "7. Local-language profiles are separately versioned and reviewed.",
        "8. Service and buying terms attach only to active provider offerings.",
        "9. Profiles cannot silently mutate after approval.",
        "10. Completed jobs preserve exact profile versions.", "",
        "## Activity keyword files", "",
        "- [Part 1](activity-keywords-part-1.md)", "- [Part 2](activity-keywords-part-2.md)", "- [Part 3](activity-keywords-part-3.md)", "",
        "## Sector domain keyword files", "",
    ]
    for slug, sector, _ in sectors:
        registry.append(f"- [{sector}](domain-keywords/{slug}-domain-keywords.md)")
    registry.extend(["", "## Delivery boundary", "", "These files define controlled documentation datasets. They do not implement search queries, connectors, classifiers, scoring, interfaces, or runtime evidence decisions.", ""])
    (OUT / "keyword-registry.md").write_text("\n".join(registry), encoding="utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    activities = parse_activities()
    sectors = parse_sector_domains()
    if len(activities) != 519:
        raise SystemExit(f"Expected 519 activities, found {len(activities)}")
    total_domains = sum(len(domains) for _, _, domains in sectors)
    if total_domains != 1586:
        raise SystemExit(f"Expected 1586 domains, found {total_domains}")
    write_activity_parts(activities)
    write_domain_files(sectors)
    write_indexes(activities, sectors)
    print(f"Generated {len(activities)} activity profiles and {total_domains} domain profiles across {len(sectors)} sectors")


if __name__ == "__main__":
    main()
