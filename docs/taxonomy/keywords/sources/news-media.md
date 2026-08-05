# Harvester Source Specification: News and Media

Status: **Proposed**  
Version: **2.1**  
Date: **5 August 2026**  
Implementation status: **Not implemented**  
Source class: **`SRC-NEWS`**

## 1. Purpose

Use reputable news, trade media, official press releases, and public announcements to identify dated events such as launches, expansion, funding, acquisitions, facility openings, partnerships, contracts, regulatory actions, and public incidents.

## 2. Approved source boundary

- Reputable news publishers and trade publications.
- Official press releases and public statements.
- Public broadcaster reports and authorized news feeds.
- Event reporting and source-attributed claims only.

## 3. Strong signal uses

- A dated event reported by a credible origin or confirmed by an official source.
- Public launch, expansion, funding, acquisition, facility opening, partnership, contract, award, or regulatory action.
- Current executive or organization changes when attributable.

## 4. Secondary signal uses

- Strategic priorities and market context.
- Project direction, public risk, and operational events.
- Responsible functions and named public representatives.

## 5. Weak or unsupported inferences

- Publication date may differ from event date.
- Syndicated articles are not independent corroboration.
- Opinion, allegation, anonymous claims, and verified facts remain separate.
- A public incident does not automatically create an opportunity.
- Headlines may omit corrections, updates, or final outcomes.

## 6. Source fields and evidence targets

- publisher, author, canonical URL, article identifier, and origin
- headline, summary, body section, entities, event type, geography, and attributed statements
- event, publication, update, correction, and retrieval dates
- original press release or primary source where available

## 7. Keyword and query inputs

- resolved organization, facility, project, or executive
- selected domain and approved activity
- launch, expansion, funding, acquisition, partnership, award, incident, and regulatory terms
- active provider-offering event, problem, intent, and contradiction profiles
- cancelled, denied, corrected, delayed, closed, superseded, or completed terms

## 8. Governed query templates

```text
<entity> + launch/expansion/funding/acquisition
<entity> + facility opening/partnership/project award
<entity> + regulatory action/incident/correction
<project or event> + official statement
<headline or event> + update/cancelled/completed
```

## 9. Inspection sequence

1. Identify the original report or press-release origin.
2. Separate event, publication, update, correction, and collection dates.
3. Resolve entities and attributed speakers.
4. Classify fact, allegation, opinion, correction, and contradiction separately.
5. Check later updates and final outcomes before using a material signal.

## 10. Required provenance

- publisher, origin, author, canonical URL, and source type
- event, publication, update, correction, and retrieval dates
- attributed statement and surrounding context
- entity-resolution and syndication-cluster identifiers
- matched event, offering, problem, and source-profile versions

## 11. Freshness and event time

The event date controls recency. Later corrections, updates, outcomes, and official confirmations may supersede the initial report.

## 12. Duplication and corroboration

Wire copies, mirrored stories, press-release syndication, and rewrites with the same origin must not inflate evidence diversity.

## 13. Privacy, authorization, and compliance

- Respect copyright, licensing, robots, access controls, and feed terms.
- Do not republish protected articles in full.
- High-impact negative or sensitive claims require authoritative support and review.

## 14. Non-detection and failure states

- `NEWS_EVENT_DETECTED`
- `NEWS_EVENT_NOT_DETECTED`
- `NEWS_SOURCE_UNAVAILABLE`
- `NEWS_ACCESS_RESTRICTED`
- `NEWS_INSPECTION_FAILED`
- `NEWS_EVENT_STALE`
- `NEWS_EVENT_CORRECTED_OR_CONTRADICTED`

## 15. Acceptance criteria

- Event and publication dates remain separate.
- Original sources and syndication clusters are retained.
- Facts, allegations, opinions, corrections, and contradictions remain distinguishable.
- Later outcomes are checked before material use.
- Runtime implementation is not falsely claimed.

## 16. Related documents

- [Keyword Benchmark and Gold-Set Standard](../benchmark-and-gold-set-standard.md).
- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).

## 17. Delivery boundary

This specification does not implement feeds, crawling, article storage, event resolution, classifiers, scoring, or contact workflows.
