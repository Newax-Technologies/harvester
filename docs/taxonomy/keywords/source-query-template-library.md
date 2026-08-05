# Harvester Source Query Template Library

Status: **Proposed**  
Version: **2.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This library defines source-specific query and inspection patterns. It does not authorize scraping, bypassing access controls, violating platform terms, or collecting private data.

## 1. General rule

A source adapter must translate canonical profiles into the fields and syntax actually supported by that source. It must not pretend every source is a general web search engine wearing a different logo.

## 2. Organization websites

### Discovery targets

- page titles and headings;
- About, Products, Services, Facilities, Locations, Careers, News, Procurement, Contact;
- structured data and metadata;
- downloadable brochures and catalogues;
- public policies, certifications, and annual reports.

### Templates

```text
site:<official-domain> <domain term>
site:<official-domain> <approved activity>
site:<official-domain> <event or procurement signal>
site:<official-domain> <technology or integration term>
site:<official-domain> <responsible function or official contact route>
```

### Weaknesses

- marketing language;
- outdated pages;
- missing content does not prove absence;
- parent and branch content may be mixed.

## 3. Business directories and maps

### Useful fields

- category;
- business name;
- address and location;
- official website;
- phone;
- opening status;
- branch count;
- services or attributes;
- verified owner data where legitimately available.

### Controls

- category is identity evidence, not activity proof;
- duplicate directories are not independent corroboration;
- user reviews require cautious interpretation;
- closed or moved status must be verified.

## 4. Government and regulator registries

### Useful fields

- legal name;
- registration or licence identifier;
- status;
- legal form;
- registered address;
- permitted activity or category;
- effective and expiry dates;
- directors or public officers only where lawful and necessary.

### Query patterns

```text
exact legal name
registration or licence number
reviewed classification code
status + effective date
entity + regulator category
```

### Evidence use

Authoritative for the exact fields governed by that registry. Not automatically authoritative for current operational capability, technology, demand, or contact intent.

## 5. Procurement and tender portals

### Fields

- notice identifier;
- buyer;
- title and description;
- category;
- publication and deadline dates;
- amendment, cancellation, award, or completion status;
- eligibility;
- submission route;
- value where officially disclosed.

### Query families

```text
<offering or capability> + tender/RFP/RFQ/EOI
<domain> + procurement + <geography>
<buyer entity> + current notices
<notice identifier> + amendment/cancellation/award
```

### Controls

- inspect the actual notice and attachments;
- retain amendments and status changes;
- do not contact outside the permitted procurement route;
- expired, cancelled, or awarded notices cannot remain active.

## 6. Job boards and careers pages

### Useful signals

- expansion;
- new capability;
- technology footprint;
- workflow ownership;
- implementation or transformation activity;
- location growth.

### Templates

```text
<entity> + <responsible role>
<entity> + implementation/integration/automation role
<domain> + new facility or operations hiring
```

### Controls

A vacancy does not prove budget, outsourcing interest, project approval, or dissatisfaction with current systems.

## 7. News and media

### Useful events

- launch;
- expansion;
- funding;
- acquisition;
- facility opening;
- partnership;
- regulatory action;
- project award;
- public incident.

### Controls

- distinguish event date from publication date;
- syndicated copies count as one origin;
- opinion, allegation, and verified fact remain separate;
- high-impact negative signals require authoritative support and review.

## 8. Social and messaging platforms

Use only public or authorized content under platform and jurisdiction rules.

Potential signals:

- official launch or branch announcement;
- public service update;
- recruitment;
- event participation;
- public inquiry route;
- product or facility evidence.

User comments and follower data are normally weak and must not be mined for sensitive or private inferences.

## 9. Technology-footprint sources

Potential evidence:

- official integration pages;
- app-marketplace listings;
- public technical documentation;
- public DNS, headers, scripts, or metadata where lawful;
- case studies naming the organization;
- implementation-partner announcements.

Controls:

- technology detection is probabilistic and time-sensitive;
- shared hosting or third-party scripts may create false attribution;
- presence does not prove satisfaction or replacement intent;
- absence does not prove non-use.

## 10. App marketplaces

Useful fields:

- product and vendor;
- category;
- integration relationship;
- supported region;
- listing status;
- reviews or installation indicators only when reliable and lawful.

A marketplace listing may support vendor capability, not necessarily customer adoption.

## 11. Professional networks

Use only authorized access and permitted public fields.

Potential evidence:

- current organization and role;
- functional responsibility;
- organization hiring or growth;
- public company descriptions.

Controls:

- title does not prove authority;
- current affiliation must be reverified;
- personal contact details are not inferred or bypassed;
- contact policy remains separate.

## 12. User-authorized imports

Imports supplied by the user may include CRM records, spreadsheets, notes, or permitted datasets.

Requirements:

- provenance;
- authorization scope;
- tenant isolation;
- row-level validation;
- suppression and consent state;
- source record preservation;
- no silent overwriting of stronger evidence.

## 13. Source-specific negative queries

For every material positive signal, inspect:

```text
cancelled
awarded
completed
closed
expired
suspended
revoked
moved
renamed
merged
superseded
do not contact
no longer employed
```

Interpret the term in context. `closed for Eid` is not dissolution; software remains annoyingly dependent on reading the sentence.

## 14. Acceptance criteria

- Each source class has a defined evidentiary purpose and weakness.
- Queries use only fields and syntax supported by the source.
- Access controls, terms, rate limits, and privacy rules are respected.
- Source suitability affects evidence confidence.
- Event dates, amendments, cancellations, and awards are retained.
- Duplicate origins do not inflate corroboration.
- Source-specific absence is not treated as universal absence.
