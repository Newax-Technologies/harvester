# Harvester Decision-Maker and Contact-Cue Registry

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This registry defines role and contact cues used to identify likely organizational responsibility and lawful contact routes after a relevant opportunity has been supported.

A title match does not prove authority. A public email address does not automatically create permission to contact. Decision-maker confidence and contact eligibility remain separate assessments.

## 1. Functional role groups

| Profile code | Functional responsibility | Reviewed title and role cues |
| --- | --- | --- |
| `ROLE-EXEC-001` | Executive ownership | owner; founder; co-founder; chief executive officer; CEO; managing director; president; proprietor; partner |
| `ROLE-OPS-001` | Operations | chief operating officer; COO; head of operations; operations director; operations manager; general manager; branch operations |
| `ROLE-IT-001` | Technology and systems | chief information officer; CIO; chief technology officer; CTO; IT director; head of IT; systems manager; applications manager; digital transformation lead |
| `ROLE-DATA-001` | Data and analytics | chief data officer; data director; analytics lead; business intelligence manager; reporting manager; data governance lead |
| `ROLE-FIN-001` | Finance and budget | chief financial officer; CFO; finance director; head of finance; controller; treasury head; accounts manager; budget officer |
| `ROLE-PROC-001` | Procurement and sourcing | chief procurement officer; procurement director; procurement manager; sourcing manager; purchasing manager; supply-chain head; tender committee |
| `ROLE-COM-001` | Commercial and growth | chief commercial officer; sales director; business development director; marketing director; growth lead; commercial manager |
| `ROLE-CUST-001` | Customer and service operations | customer experience director; service delivery manager; customer support head; patient experience; student services; guest relations |
| `ROLE-HR-001` | People and workforce | chief human resources officer; HR director; head of people; talent acquisition lead; learning and development manager; payroll manager |
| `ROLE-RISK-001` | Risk, compliance and audit | chief risk officer; compliance officer; internal audit head; information security officer; data protection officer; quality manager; Shariah compliance officer |
| `ROLE-FAC-001` | Facilities and property operations | facilities director; facility manager; property manager; estate manager; maintenance manager; building operations manager |
| `ROLE-ENG-001` | Engineering, plant and assets | engineering director; plant manager; production manager; maintenance engineer; reliability manager; asset manager; technical services manager |
| `ROLE-LOG-001` | Logistics and fleet | logistics director; fleet manager; transport manager; warehouse manager; distribution manager; dispatch manager; last-mile operations |
| `ROLE-CLIN-001` | Healthcare administration | hospital administrator; medical director; clinic manager; practice manager; nursing director; biomedical engineering head; laboratory manager |
| `ROLE-EDU-001` | Education administration | vice chancellor; rector; principal; registrar; dean; director academics; admissions head; examinations controller; campus administrator |
| `ROLE-LEGAL-001` | Legal operations | managing partner; senior partner; legal operations director; practice head; general counsel; company secretary; compliance counsel; matter-management lead |
| `ROLE-RETAIL-001` | Retail and commerce | retail director; category manager; merchandising head; store operations manager; e-commerce head; inventory manager; franchise manager |
| `ROLE-HOSP-001` | Hospitality | general manager; hotel manager; rooms division manager; front-office manager; revenue manager; food and beverage director; housekeeping manager |
| `ROLE-GOV-001` | Government and public administration | secretary; director general; commissioner; department director; program director; project director; procurement officer; chief information officer |
| `ROLE-NPO-001` | Nonprofit and development | executive director; country director; program director; grants manager; monitoring and evaluation lead; fundraising director; operations manager |

## 2. Authority-confidence levels

```text
CONFIRMED_OWNER
CONFIRMED_FUNCTIONAL_OWNER
LIKELY_FUNCTIONAL_OWNER
INFLUENCER
GENERAL_CONTACT
UNKNOWN
```

A role may be relevant without holding purchase authority. A technical manager may define requirements while procurement controls vendor engagement and finance controls budget.

## 3. Contact-route profiles

| Code | Contact route | Default treatment |
| --- | --- | --- |
| `CONTACT-DIRECT-001` | Direct voluntary inquiry or reply | Highest contact eligibility when consent and identity are valid |
| `CONTACT-OFFICIAL-001` | Official business email, phone, or contact form | Eligible only under workspace policy and jurisdictional rules |
| `CONTACT-PROC-001` | Procurement, tender, supplier, or vendor-registration portal | Use only for the stated procurement purpose and deadline |
| `CONTACT-REFERRAL-001` | Valid professional or customer referral | Requires recorded referral basis and any sector-specific consent |
| `CONTACT-PUBLIC-ROLE-001` | Publicly listed organizational role | Role relevance may be used; private personal data must not be inferred |
| `CONTACT-SOCIAL-001` | Authorized social or platform messaging route | Subject to platform terms, consent policy, rate limits, and suppression |
| `CONTACT-DIRECTORY-001` | Business directory contact | Lower confidence; verify organization and route before contact-ready status |
| `CONTACT-NONE-001` | No lawful contact route | Candidate may remain research-worthy but cannot become contact-ready |

## 4. Role-resolution rules

1. Match titles as phrases, entities, and normalized role concepts, not uncontrolled substrings.
2. Preserve the source title exactly alongside the normalized role group.
3. Confirm that the person remains associated with the target organization.
4. Prefer current organization pages, authorized professional profiles, official directories, and attributable announcements.
5. Treat scraped aggregators and stale biographies as weak evidence.
6. A role older than the configured freshness window requires reverification.
7. Shared inboxes such as `info@`, `sales@`, or `procurement@` are organizational routes, not named decision makers.
8. Do not infer protected traits, private health status, personal finances, or family relationships from a role profile.
9. A named decision maker does not override suppression, consent, conflict, do-not-contact, or channel restrictions.
10. Communicator receives only approved role context and contact-eligibility state, not unrestricted personal-source data.

## 5. Sector-to-role guidance

The provider offering determines the relevant role group. Examples:

```text
Enterprise software for a hospital
→ hospital administration + IT + operations + finance/procurement

Cold-chain monitoring for a pharmaceutical distributor
→ logistics + warehouse + quality/compliance + IT + procurement

Matter-management system for a law firm
→ managing partner + legal operations + IT + finance

Fleet telemetry for a courier operator
→ logistics/fleet + operations + engineering/maintenance + IT
```

## 6. Acceptance criteria

- Functional responsibility is separated from contact eligibility.
- Titles are normalized without discarding the original source text.
- Current organization affiliation is verified before high-confidence attribution.
- Named roles, shared inboxes, direct inquiries, referrals, and procurement channels remain distinct.
- Suppression and consent rules override role relevance.
- Runtime implementation is not falsely claimed.
