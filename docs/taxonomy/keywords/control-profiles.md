# Harvester Keyword Control Profiles

Status: **Proposed**  
Version: **1.1**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

These shared controls reduce repeated text across domain, activity, lead-signal, role, and source keyword registries. They do not weaken provider-offering, evidence, qualification, consent, or compliance requirements.

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
| `EX-ASSET` | Distinguish financial, property, physical, and IT asset management through sector context. |
| `EX-NETWORK` | Distinguish telecom, logistics, dealer, healthcare, social, and computer networks through domain context. |
| `EX-AI` | Exclude generic promotional uses; require defined technical, analytical, or decision-support context. |
| `EX-JOB` | A vacancy supports hiring or expansion only after entity, location, date, and role relevance are verified; it does not prove purchasing intent or budget. |
| `EX-REQUEST` | Distinguish a genuine buyer or service request from copied content, instructional examples, forums, templates, and provider advertising. |
| `EX-TENDER` | Confirm buyer, authority, deadline, status, amendments, cancellation, and award state before treating a tender as active intent. |
| `EX-REVIEW` | Reviews may support service-quality or operational-research hypotheses but do not independently prove an internal capability gap. |
| `EX-NEWS` | Distinguish original reporting or attributable announcements from speculation, summaries, and syndicated copies. |
| `EX-VENDOR` | Existing-vendor evidence may indicate replacement, integration, optimization, support, or no opportunity; never disqualify automatically. |
| `EX-CLOSED` | Closure, dissolution, cancellation, award, or inactivity evidence suppresses stale positive signals when authoritative and current. |
| `EX-ROLE` | A title indicates possible responsibility; confirm current organization affiliation and do not infer purchase authority automatically. |
| `EX-CONTACT` | A public contact route is not automatic permission to contact; consent, suppression, jurisdiction, channel, and platform policies still apply. |
| `EX-HEALTH` | Do not infer diagnosis, treatment need, pregnancy, disability, or private health status from unrelated personal content. |
| `EX-LEGAL-RISK` | Do not infer misconduct, liability, legal exposure, or case need from allegations, weak sources, or sensational reporting. |
| `EX-FINANCIAL-RISK` | Do not infer financial distress, fraud, credit weakness, or investment need from weak or indirect evidence. |
| `EX-POLITICAL` | Political persuasion, voter targeting, protected-belief profiling, and unrelated political inference are outside this lead taxonomy. |

## Evidence-control profiles

| Code | Requirement |
| --- | --- |
| `EVID-DIRECT` | One attributable direct inquiry, explicit request, official statement, or authoritative active procurement record. |
| `EVID-AUTH` | One authoritative registry, regulator, official report, certification, or government source appropriate to the claim. |
| `EVID-CORR-2` | Two independent evidence origins supporting the same material claim. |
| `EVID-INDIRECT` | Indirect or circumstantial indicators may enter a research queue but cannot become contact-ready. |
| `EVID-HUMAN` | Human review is required for sensitive, contradictory, high-value, or reputationally risky claims. |
| `EVID-NEGATIVE` | Run negative and contradiction checks before activating a material opportunity. |
| `EVID-FRESH` | Use the underlying event date where known and expire the signal according to its profile. |
| `EVID-SOURCE-FIT` | The source must be suitable for the claim; source authority and source-signal relevance are separate dimensions. |
| `EVID-DEDUP` | Copied, mirrored, syndicated, or directory-replicated evidence counts as one origin. |

## Contact and role controls

| Code | Rule |
| --- | --- |
| `CTRL-ENTITY-FIRST` | Resolve the organization before combining sector, domain, activity, role, and contact evidence. |
| `CTRL-ROLE-AFTER-ENTITY` | Decision-maker discovery begins only after entity resolution reaches the configured threshold. |
| `CTRL-CONTACT-AFTER-OPPORTUNITY` | Contact-route discovery begins only when the profile permits it and an opportunity is supported or under approved verification. |
| `CTRL-SUPPRESSION-FIRST` | Suppression, deletion, conflict, do-not-contact, referral, and consent rules override commercial relevance. |
| `CTRL-NO-RAW-COUNT` | Raw keyword or source match counts never become a lead or opportunity score. |
| `CTRL-PROFILE-SPECIFIC` | One organization may qualify differently for several provider offerings and lead-generation profiles. |

## Acceptance criteria

- Shared controls are stable, versioned references rather than copied prose.
- Ambiguous terms have explicit disambiguation requirements.
- Job, tender, role, contact, news, review, and existing-vendor evidence have dedicated restrictions.
- Sensitive healthcare, legal, financial, and political inferences are prohibited or review-gated.
- Evidence strength, freshness, source fit, and duplicate origin remain separate controls.
- Runtime implementation is not falsely claimed.
