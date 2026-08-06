# Harvester Source Specification: Company Reports and Investor Publications

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-REPORT`**

## 1. Purpose

Use official annual reports, financial statements, investor presentations, governance reports, sustainability reports, strategy documents, and public filings to identify formal strategy, scale, projects, risks, priorities, and dated organizational disclosures.

## 2. Approved source boundary

- Official organization reports and investor publications.
- Regulator-hosted filings and authorized filing feeds.
- Public governance, strategy, sustainability, and operational reports.
- Document versions, reporting periods, corrections, and restatements must be retained.

## 3. Strong signal uses

- Formal organization identity and reporting period.
- Governance, strategy, disclosed projects, scale, and officially stated risks.
- Dated financial or operational measures where the report is authoritative.
- Approved capital projects, expansion plans, investments, and stated priorities.

## 4. Secondary signal uses

- Technology, infrastructure, operational, compliance, and sustainability priorities.
- Responsible functions and named executives.
- Existing systems, project partners, and future-direction context.

## 5. Weak or unsupported inferences

- Reports may be delayed, selective, promotional, restated, or superseded.
- Planned initiatives may not be funded or completed.
- A disclosed risk does not automatically create an opportunity.
- Historical financial scale does not prove current budget.
- Forward-looking statements are not completed facts.

## 6. Source fields and evidence targets

- organization, document type, reporting period, version, and source
- publication, effective, approval, correction, and restatement dates
- sections, page references, tables, measures, projects, risks, and attributed statements
- checksum, language, parser version, and filing identifier

## 7. Keyword and query inputs

- resolved organization and report type
- selected domain and approved activity
- project, technology, risk, investment, expansion, and governance terms
- active provider-offering problem, existing-solution, investment, or intent profiles
- restated, corrected, discontinued, delayed, cancelled, or completed terms

## 8. Governed query templates

```text
<organization> + annual report/investor presentation
<organization> + strategy/capital project/expansion
<organization> + technology/infrastructure/risk
<filing identifier> + amendment/restatement
<project> + delayed/cancelled/completed
```

## 9. Inspection sequence

1. Use the official filing or organization source.
2. Identify reporting period, version, approval, restatement, and document status.
3. Capture precise section, page, table, and statement context.
4. Separate historical fact, current state, plan, risk, estimate, and forward-looking statement.
5. Check later reports, amendments, and completion outcomes.

## 10. Required provenance

- document, filing identifier, organization, canonical URL, and reporting period
- version, checksum, page, section, table, and parser version
- publication, approval, correction, restatement, event, and retrieval dates
- contributing domain, activity, project, problem, offering, and source-profile versions

## 11. Freshness and event time

Report evidence is period- and statement-specific. Later filings, restatements, interim updates, and event disclosures may supersede earlier statements.

## 12. Duplication and corroboration

The same report may appear on investor, regulator, archive, and media sites. Match filing identifier, period, checksum, and version to one origin.

## 13. Privacy, authorization, and compliance

- Use public or authorized reports and respect licensing and access rules.
- Do not extract undisclosed or restricted investor information.
- Forward-looking statements and estimates require explicit classification.

## 14. Non-detection and failure states

- `REPORT_RECORD_DETECTED`
- `REPORT_RECORD_NOT_DETECTED`
- `REPORT_SOURCE_UNAVAILABLE`
- `REPORT_ACCESS_RESTRICTED`
- `REPORT_PARSE_FAILED`
- `REPORT_RECORD_STALE`
- `REPORT_RESTATED_SUPERSEDED_OR_CONTRADICTED`

## 15. Acceptance criteria

- Reporting period and document version are retained.
- Precise page or section context is preserved.
- Fact, plan, estimate, risk, and forward-looking statement remain separate.
- Restatements and later disclosures are checked.
- Duplicate copies do not inflate corroboration.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [News and Media](news-media.md).
- [Semantic, Entity and Classification Expansion](../semantic-entity-and-classification-expansion.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement filing feeds, document parsing, storage, metric extraction, classifiers, scoring, or contact workflows.
