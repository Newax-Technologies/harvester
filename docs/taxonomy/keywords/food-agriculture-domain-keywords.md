# Harvester Food and Agriculture Domain Keyword Registry

Status: **Proposed**  
Version: **1.2**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

Review boundary: **Controlled discovery baseline. Human sector review, source-level validation, locale review, benchmark testing, and approved activation are required before runtime use.**

This file defines separate discovery keyword profiles for the **103** canonical domains in the Food and Agriculture sector.

Domain aliases support discovery only. Activity keywords resolve through the canonical activity registry and the existing domain–activity mapping. Organization and exclusion codes resolve through [Keyword Control Profiles](control-profiles.md).

Keywords identify evidence candidates. They do not independently prove that an organization belongs to a domain, performs an activity, needs a provider service, has buying intent, presents a service gap, or qualifies as a lead.

| Profile | Domain | Reviewed domain terms | Organization profile | Exclusion profile |
| --- | --- | --- | --- | --- |
| `KW-FAG-CRO-001-V1` | Cereal Crops | cereal crops; cereal crop | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-002-V1` | Rice | rice | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-CRO-003-V1` | Wheat | wheat | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-CRO-004-V1` | Maize and Corn | maize and corn; maize & corn | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-005-V1` | Pulses and Legumes | pulses and legumes; pulses & legumes | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-006-V1` | Oilseed Crops | oilseed crops; oilseed crop | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-007-V1` | Sugar Crops | sugar crops; sugar crop | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-008-V1` | Cotton and Fibre Crops | cotton and fibre crops; cotton & fibre crops | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-009-V1` | Vegetables | vegetables; vegetable | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-CRO-010-V1` | Fruits | fruits; fruit | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-CRO-011-V1` | Citrus Fruits | citrus fruits; citrus fruit | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-012-V1` | Dates | dates; date | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-CRO-013-V1` | Nuts and Dry Fruits | nuts and dry fruits; nuts & dry fruits | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-014-V1` | Herbs and Spices | herbs and spices; herbs & spices | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-015-V1` | Tea and Coffee | tea and coffee; tea & coffee | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-016-V1` | Medicinal and Aromatic Plants | medicinal and aromatic plants; medicinal & aromatic plants | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-FAG-CRO-017-V1` | Floriculture | floriculture | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-CRO-018-V1` | Nurseries and Seedlings | nurseries and seedlings; nurseries & seedlings | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-019-V1` | Greenhouse Farming | greenhouse farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-CRO-020-V1` | Hydroponics and Controlled-Environment Agriculture | hydroponics and controlled-environment agriculture; hydroponics & controlled-environment agriculture | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-001-V1` | Cattle Farming | cattle farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-002-V1` | Buffalo Farming | buffalo farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-003-V1` | Sheep and Goat Farming | sheep and goat farming; sheep & goat farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-004-V1` | Poultry Farming | poultry farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-005-V1` | Egg Production | egg production | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-006-V1` | Dairy Farming | dairy farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-007-V1` | Milk Collection | milk collection | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-008-V1` | Animal Feed | animal feed | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-009-V1` | Animal Breeding and Genetics | animal breeding and genetics; animal breeding & genetics | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-010-V1` | Veterinary Livestock Services | veterinary livestock services; veterinary livestock service; veterinary livestock providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-FAG-LIV-011-V1` | Meat Production | meat production | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-012-V1` | Slaughterhouses and Abattoirs | slaughterhouses and abattoirs; slaughterhouses & abattoirs | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-013-V1` | Leather and Hides | leather and hides; leather & hides | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-014-V1` | Beekeeping and Honey | beekeeping and honey; beekeeping & honey | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-015-V1` | Camel Farming | camel farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-LIV-016-V1` | Equine and Working Animals | equine and working animals; equine & working animals | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-001-V1` | Marine Fisheries | marine fisheries; marine fishery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-002-V1` | Inland Fisheries | inland fisheries; inland fishery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-003-V1` | Fish Farming | fish farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-004-V1` | Shrimp and Prawn Farming | shrimp and prawn farming; shrimp & prawn farming | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-005-V1` | Hatcheries | hatcheries; hatchery | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-AQU-006-V1` | Aquaculture Feed | aquaculture feed | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-007-V1` | Seafood Processing | seafood processing | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-008-V1` | Cold-Water Fisheries | cold-water fisheries; cold-water fishery | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-AQU-009-V1` | Fish Markets and Auctions | fish markets and auctions; fish markets & auctions | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-INP-001-V1` | Seeds | seeds; seed | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-INP-002-V1` | Fertilizers | fertilizers; fertilizer | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-INP-003-V1` | Crop Protection Products | crop protection products; crop protection product | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-004-V1` | Soil Conditioners | soil conditioners; soil conditioner | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-INP-005-V1` | Irrigation Equipment | irrigation equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-006-V1` | Farm Machinery | farm machinery | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-007-V1` | Tractors and Implements | tractors and implements; tractors & implements | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-INP-008-V1` | Greenhouse Equipment | greenhouse equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-009-V1` | Livestock Equipment | livestock equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-010-V1` | Poultry Equipment | poultry equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-011-V1` | Dairy Equipment | dairy equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-012-V1` | Aquaculture Equipment | aquaculture equipment | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-013-V1` | Agricultural Drones | agricultural drones; agricultural drone | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-INP-014-V1` | Farm Sensors and Telemetry | farm sensors and telemetry; farm sensors & telemetry | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-INP-015-V1` | Agricultural Packaging | agricultural packaging | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-INP-016-V1` | Farm Energy and Solar Systems | farm energy and solar systems; farm energy & solar systems; farm power and solar systems | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-PRO-001-V1` | Grains and Milling Products | grains and milling products; grains & milling products | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-PRO-002-V1` | Flour and Bakery Ingredients | flour and bakery ingredients; flour & bakery ingredients | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-003-V1` | Edible Oils and Fats | edible oils and fats; edible oils & fats | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-004-V1` | Sugar and Sweeteners | sugar and sweeteners; sugar & sweeteners | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-005-V1` | Fresh Produce | fresh produce | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-006-V1` | Frozen Foods | frozen foods; frozen food | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-007-V1` | Canned Foods | canned foods; canned food | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-008-V1` | Dairy Products | dairy products; dairy product | `ORG-PRODUCT` | `EX-BROAD` |
| `KW-FAG-PRO-009-V1` | Meat and Poultry Products | meat and poultry products; meat & poultry products | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-PRO-010-V1` | Seafood Products | seafood products; seafood product | `ORG-PRODUCT` | `EX-BROAD` |
| `KW-FAG-PRO-011-V1` | Bakery Products | bakery products; bakery product | `ORG-PRODUCT` | `EX-BROAD` |
| `KW-FAG-PRO-012-V1` | Confectionery | confectionery | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-PRO-013-V1` | Snacks | snacks; snack | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-PRO-014-V1` | Spices and Condiments | spices and condiments; spices & condiments | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-015-V1` | Sauces and Preserves | sauces and preserves; sauces & preserves | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-016-V1` | Ready-to-Eat Meals | ready-to-eat meals; ready-to-eat meal | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-017-V1` | Beverages | beverages; beverage | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-PRO-018-V1` | Bottled Water | bottled water | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-019-V1` | Juices | juices; juice | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-PRO-020-V1` | Tea and Coffee Products | tea and coffee products; tea & coffee products | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-PRO-021-V1` | Infant and Clinical Foods | infant and clinical foods; infant & clinical foods | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-PRO-022-V1` | Halal Food Products | halal food products; halal food product | `ORG-PRODUCT` | `EX-PHRASE` |
| `KW-FAG-OPS-001-V1` | Farm Management Services | farm management services; farm management service; farm management providers | `ORG-SERVICE` | `EX-BROAD` |
| `KW-FAG-OPS-002-V1` | Agricultural Extension Services | agricultural extension services; agricultural extension service; agricultural extension providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-FAG-OPS-003-V1` | Crop Testing Laboratories | crop testing laboratories; crop testing laboratory; crop testing labs | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-FAG-OPS-004-V1` | Food Testing Laboratories | food testing laboratories; food testing laboratory; food testing labs | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-FAG-OPS-005-V1` | Quality Certification | quality certification | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-006-V1` | Halal Certification | halal certification | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-007-V1` | Commodity Trading | commodity trading | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-008-V1` | Agricultural Cooperatives | agricultural cooperatives; agricultural cooperative | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-009-V1` | Produce Markets | produce markets; produce market | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-010-V1` | Grain Storage | grain storage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-011-V1` | Silos | silos; silo | `ORG-GENERIC` | `EX-BROAD` |
| `KW-FAG-OPS-012-V1` | Cold Storage | cold storage | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-013-V1` | Pack Houses and Grading Centres | pack houses and grading centres; pack houses & grading centres; pack houses and grading centers | `ORG-INSTITUTION` | `EX-PHRASE` |
| `KW-FAG-OPS-014-V1` | Food Warehousing | food warehousing; food warehouse | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-015-V1` | Refrigerated Transport | refrigerated transport | `ORG-GENERIC` | `EX-PHRASE` |
| `KW-FAG-OPS-016-V1` | Agricultural Export Services | agricultural export services; agricultural export service; agricultural export providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-FAG-OPS-017-V1` | Farm-to-Market Platforms | farm-to-market platforms; farm-to-market platform | `ORG-SOFTWARE` | `EX-MARKET` |
| `KW-FAG-OPS-018-V1` | Food Traceability Systems | food traceability systems; food traceability system | `ORG-SOFTWARE` | `EX-PHRASE` |
| `KW-FAG-OPS-019-V1` | Agricultural Finance Services | agricultural finance services; agricultural finance service; agricultural finance providers | `ORG-SERVICE` | `EX-PHRASE` |
| `KW-FAG-OPS-020-V1` | Agricultural Insurance and Takaful | agricultural insurance and takaful; agricultural insurance & takaful | `ORG-GENERIC` | `EX-PHRASE` |

## Locked interpretation

1. Every canonical domain retains a separate keyword profile and version.
2. Domain terms identify the market or subject area; activity terms remain separately governed.
3. Organization cues improve precision but are not mandatory when authoritative classification evidence exists.
4. Broad or ambiguous phrases require sector, organization, activity, source, entity, proximity, or co-occurrence context.
5. Service-gap, buying-intent, problem, competitor, replacement, integration, and existing-solution terms require an active provider offering and separate service-specific profiles.
6. Urdu, Roman Urdu, and other locale aliases require reviewed locale packs and gold-set validation before activation.
7. A matched phrase is an evidence candidate, not a domain, activity, opportunity, authority, consent, or lead decision.
8. Completed Harvest Jobs preserve the exact keyword-profile and control-profile versions used when they ran.

## Delivery boundary

This Markdown registry is a controlled documentation dataset. It does not implement database records, APIs, search indexes, embeddings, source queries, classifiers, evidence scoring, opportunity scoring, contact discovery, outreach, or releases.
