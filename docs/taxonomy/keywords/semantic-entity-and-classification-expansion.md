# Harvester Semantic, Entity and Classification Expansion Standard

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This standard defines controlled expansion beyond literal keyword matching. It covers semantic concepts, organization aliases, structured classifications, identifiers, facilities, brands, products, locations, and relationships.

## 1. Why lexical matching is insufficient

Organizations may describe the same operation differently:

- `pharmaceutical distributor`;
- `medicine wholesaler`;
- `authorized drug supplier`;
- `healthcare distribution company`;
- `national stockist`.

Literal matching alone misses valid variants. Uncontrolled semantic matching invents relationships. Harvester therefore combines lexical profiles, entity resolution, classification crosswalks, semantic seeds, and evidence controls.

## 2. Entity types

```text
ORGANIZATION
ORGANIZATION_UNIT
BRAND
PRODUCT_OR_SERVICE
FACILITY
ASSET_OR_EQUIPMENT
PROJECT
PROCUREMENT_EVENT
CONTRACT
REGULATORY_LICENCE
PERSON_ROLE
LOCATION
TECHNOLOGY_PRODUCT
STANDARD_OR_CERTIFICATION
```

## 3. Organization-name normalization

Normalize without destroying evidence:

- capitalization and punctuation;
- legal suffixes such as Limited, Ltd, Private Limited, Pvt Ltd, SMC-Private;
- ampersand and `and` variants;
- spacing and hyphenation;
- common transliteration variants;
- known former names and trading names;
- parent, subsidiary, branch, franchise, and brand relationships.

Store the original name from every source. Never replace source history with one normalized string.

## 4. Alias classes

| Alias class | Example | Confidence requirement |
| --- | --- | --- |
| Legal name | ABC Pharmaceuticals (Private) Limited | Registry or official source |
| Trading name | ABC Pharma | First-party or corroborated |
| Acronym | ABCL | Ambiguity review |
| Former name | XYZ Labs, renamed ABC Pharma | Dated authoritative evidence |
| Local-script name | اے بی سی فارما | Reviewed locale or official record |
| Brand | MedicaPlus | Brand-owner relationship evidence |
| Branch name | ABC Pharma Lahore Depot | Parent and location evidence |
| Common misspelling | ABC Pharmaceuticles | Discovery only, never canonical |

## 5. Classification crosswalk fields

Profiles should support optional mappings to:

- national business-registration categories;
- Pakistan Standard Industrial Classification where available;
- ISIC or other international industry classifications;
- NAICS or regional classifications where relevant;
- procurement category codes;
- map and directory categories;
- schema.org entity types;
- app-marketplace categories;
- regulator or licence categories;
- customs, product, medical-device, commodity, or tariff classifications where lawful and useful.

The code system, edition, jurisdiction, effective date, and source must be stored. Codes must not be copied between editions as though standards never change, an optimism unsupported by standards bodies.

## 6. Semantic profile

A semantic profile may contain:

```text
canonical definition
included concepts
excluded concepts
parent concepts
child concepts
sibling concepts
operational processes
organization archetypes
facilities and assets
products and services
positive examples
near-positive examples
negative examples
ambiguous examples
locale-specific examples
```

## 7. Ontology relationships

```text
IS_A
PART_OF
PRODUCES
PROVIDES
DISTRIBUTES
SELLS
OPERATES
USES
INSTALLED_AT
REGULATED_BY
CERTIFIED_TO
LOCATED_AT
OWNED_BY
SUBSIDIARY_OF
BRAND_OF
SUCCESSOR_OF
PARTNER_OF
SERVES_MARKET
```

Relationship evidence must be stored separately from the entity nodes. A keyword co-occurrence does not automatically create a relationship.

## 8. Facility and asset evidence

Facilities and assets may strengthen activity classification:

- manufacturing plant;
- distribution centre;
- cold store;
- hospital;
- diagnostic laboratory;
- school campus;
- hotel property;
- fleet depot;
- data centre;
- power plant;
- warehouse;
- branch network.

The existence of a facility does not prove ownership, operational control, capacity, or unmet need. Store the relationship and confidence separately.

## 9. Semantic similarity controls

- Record model, version, embedding date, and language.
- Compare against reviewed profile seeds, not only profile names.
- Calibrate thresholds by sector and source.
- Do not use one global threshold for legal, healthcare, retail, and technology text.
- Inspect nearest negative examples.
- Route low-margin or high-impact matches to human review.
- Preserve text spans and explanation for every accepted semantic match.
- Re-embed or migrate profiles under controlled versioning when models change.

## 10. Entity-resolution evidence

A resolved organization may use:

- legal or registration number;
- official domain;
- verified phone or address;
- official social account;
- regulator record;
- parent-subsidiary relationship;
- consistent location and operating description;
- unique facility, brand, or product relationship.

Name similarity alone is insufficient for high-confidence merging.

## 11. Branches and franchises

Branches, franchisees, dealerships, campuses, facilities, and subsidiaries must not be collapsed automatically into the parent.

Store:

```text
entity type
parent relationship
ownership or control type
location
operating name
source evidence
validity dates
whether opportunity and contact decisions occur at parent, branch, or both
```

## 12. Acceptance criteria

- Literal, semantic, entity, and classification evidence remain distinguishable.
- Source names are preserved alongside normalized entities.
- Structured codes include system, edition, jurisdiction, and date.
- Relationships require evidence and confidence.
- Branches and parents are not silently merged.
- Semantic matches retain model version and supporting text.
- Negative and ambiguous benchmark examples are used.
- No semantic or classification match independently creates an opportunity.
