# Harvester Source-to-Signal Matrix

Status: **Proposed**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

This matrix identifies which lead-generation signals each approved source class can reasonably support. A source adapter may collect only what its authorization, policy, and documented format permit.

## Source classes

| Source class | Strong signal uses | Secondary uses | Common weaknesses |
| --- | --- | --- | --- |
| Organization website | Domain identity; services; locations; leadership; public technology; expansion; direct inquiry routes | Operational language; case studies; partner ecosystem | Marketing bias; internal capability silence; stale pages |
| Government or professional registry | Legal identity; operating status; licence; incorporation; regulated category; location | New registration; renewal; ownership changes where public | Limited operational detail; update delays |
| Procurement and tender portal | Active purchase intent; project requirement; budget or scope; deadline; eligibility | Vendor requirements; technology or asset specifications | Awards, cancellations, and amendments may change quickly |
| Job board or careers page | Hiring; expansion; technology footprint; process ownership; new capability | Location growth; implementation program; team structure | A vacancy does not prove purchase intent or budget |
| Authorized professional network | Current roles; organization affiliation; hiring; announcements; partnerships | Decision-maker and functional-owner cues | Access and reuse restrictions; self-reported data |
| News and media | Funding; expansion; launch; acquisition; public incidents; contracts | Strategic priorities; executive changes | Syndication duplicates; speculation; event date ambiguity |
| Maps and business listings | Location; branch; category; operating hours; public contact route | New branch; closure; customer-facing presence | User edits; duplicate listings; weak legal identity |
| Business directory | Category; organization identity; public contact route | Supplier and distributor discovery | Stale records; resellers; duplicate entities |
| Social platform | Launches; direct requests; campaigns; events; public announcements | Customer-service pressure; seasonal activity | Informal language; impersonation; platform terms |
| App marketplace or technology directory | Existing solution; software vendor; integrations; ratings; release activity | Replacement or upgrade context | Listing presence does not prove active deployment |
| Company report or investor publication | Strategy; budget; expansion; risks; projects; financial scale | Technology and operational priorities | Reporting lag; selective disclosure |
| Certification or accreditation source | Standards; compliance; scope; expiry; quality status | Facility or product capability | Certification does not prove operational effectiveness |
| Manual authorized import | Customer-owned evidence; known accounts; CRM context; consent | Verification and enrichment | Input quality and lawful-use basis vary |
| Direct inquiry or referral | Expressed need; urgency; contact permission; scope | Qualification and routing | Identity, authority, and fit still require verification |

## Source selection rules

1. Use the highest-authority source reasonably available for the claim.
2. Match the source to the signal. A job board is strong for hiring and weak for confirmed purchasing.
3. Preserve the original event date separately from the collection date.
4. Detect copied content, press-release syndication, and directory replication as one evidence origin.
5. A source adapter may not expand its collection because a keyword profile contains an interesting term.
6. Source failure, access denial, or absence of a page reduces coverage; it does not prove a gap.
7. Procurement signals must track amendments, cancellations, awards, and deadlines.
8. Role and contact data must be current enough for the configured contact policy.
9. Sensitive personal data is excluded unless explicitly authorized and necessary for the approved workflow.
10. Every Harvest Job snapshot preserves source-policy and adapter-version references.

## Recommended source combinations

| Objective | Preferred combination |
| --- | --- |
| New business or facility | Registry + organization website + map or announcement |
| Active procurement | Authoritative tender portal + buyer website + amendment/award tracking |
| Expansion | Company announcement + job activity + location or registry corroboration |
| Technology replacement | Direct statement or procurement + existing-solution evidence + role context |
| Operational pain | Direct statement + process evidence + second independent source |
| Decision-maker resolution | Official organization source + authorized professional source |
| Contact-ready lead | Supported opportunity + current lawful contact route + suppression/consent check |

## Acceptance criteria

- Every source class has defined strong and weak uses.
- Source authority and signal relevance remain distinct dimensions.
- Duplicated publications do not inflate evidence diversity.
- Direct inquiry and referral sources remain separate from public discovery.
- Source policy and adapter authorization override keyword ambition.
- Runtime implementation is not falsely claimed.
