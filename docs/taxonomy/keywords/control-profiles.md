# Harvester Keyword Control Profiles

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

## Organization cue profiles

| Code | Eligible cues |
| --- | --- |
| `ORG-GENERIC` | business; provider; company; organization |
| `ORG-INSTITUTION` | operator; institution; facility; organization |
| `ORG-SOFTWARE` | software vendor; platform provider; technology company; solution provider |
| `ORG-PRODUCT` | manufacturer; producer; supplier; distributor |
| `ORG-SERVICE` | service provider; specialist firm; operator; contractor |
| `ORG-COMMERCE` | retailer; seller; merchant; distributor |
| `ORG-PUBLIC` | public authority; government department; regulator; public institution |
| `ORG-NONPROFIT` | nonprofit organization; NGO; charity; foundation |

## Exclusion and context profiles

| Code | Rule |
| --- | --- |
| `EX-PHRASE` | Require the exact domain phrase or a reviewed alias plus sector, organization, or activity context. |
| `EX-BROAD` | Require at least one activity or organization cue; do not qualify from this broad term alone. |
| `EX-BANK` | Exclude river-bank, blood-bank, and data-bank meanings unless the selected domain explicitly requires them. |
| `EX-CLOUD` | Exclude weather meanings; require computing, hosting, data, or infrastructure context. |
| `EX-PORT` | Require transport, shipping, airport, logistics, or computing context appropriate to the selected domain. |
| `EX-PLANT` | Distinguish industrial facilities from botanical plants through production, utility, factory, or agriculture context. |
| `EX-SECURITY` | Distinguish cybersecurity, private security, public safety, and financial-security meanings through sector and activity evidence. |
| `EX-AUDIT` | Distinguish financial, compliance, quality, security, and code audits through sector and activity context. |
| `EX-TRUST` | Distinguish legal entities, charitable organizations, financial trusts, and technical foundations through sector context. |
| `EX-SCHOOL` | Exclude school-of-thought and unrelated uses; require education, teaching, student, or training evidence. |
| `EX-CLINIC` | Require healthcare delivery, patient, diagnostic, treatment, or licensed-practice context. |
| `EX-MARKET` | Distinguish retail marketplaces, financial markets, physical markets, and market research through activity context. |
| `EX-ASSET` | Distinguish financial, property, and IT asset management through sector context. |
| `EX-NETWORK` | Distinguish telecom, logistics, dealer, healthcare, social, and computer networks through domain context. |
| `EX-AI` | Exclude generic promotional uses; require defined technical, analytical, or decision-support context. |

These profiles reduce repeated text. They do not weaken the evidence requirements in the keyword taxonomy index.
