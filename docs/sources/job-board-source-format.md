# Harvester General Job Board Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**

## 1. Purpose

This document defines how licensed job-board APIs, customer-authorized employer feeds, public employer job pages, authorized imports, and manual references enter Harvester when the source is not governed by a dedicated provider document such as Indeed.

Job postings can support hiring, capability, technology, location and timing hypotheses. They are not automatic evidence of procurement intent or a service gap.

## 2. Source modes

```text
JOB_BOARD_API_LICENSED
JOB_BOARD_EMPLOYER_FEED_AUTHORIZED
JOB_BOARD_PUBLIC_EMPLOYER_PAGE
JOB_BOARD_AUTHORIZED_IMPORT
JOB_BOARD_OPERATOR_REFERENCE
```

## 3. User configuration

```text
provider_code
mode
credential_or_connection_reference_id
license_profile_id
employer_filters
job_title_filters
occupation_filters
skill_filters
technology_filters
location_filters
remote_policy
freshness_window
status_filters
maximum_pages
request_budget
retention_policy_version
operator_reference_urls
```

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Employer | Provider employer ID | Hiring-organization reference |
| Job posting | Provider job ID | Hiring and capability evidence |
| Job location | Job-location identifier | Operating-location hint |
| Skill or occupation | Provider taxonomy ID | Source-native classification |
| Employer feed row | Customer external ID | Customer-authorized job evidence |
| Operator reference | Job URL | Manual navigation and review |

## 5. Canonical formatting

```text
source.code = JOB_BOARD
source.mode = selected job-board mode
native.object_type = employer | job_posting | job_location | taxonomy_term
native.object_id = provider object ID
native.parent_id = employer ID for job records
native.url = permitted job or employer URL
entity_hints.organization_names = hiring company
entity_hints.domains = employer domain when supplied
entity_hints.addresses = job and employer locations
entity_hints.provider_identifiers = employer and job IDs
content.title = job title
content.summary = bounded job description or artifact reference
content.published_at = posting date
signals.job_roles = normalized job role
signals.activity_codes = approved activity evidence
signals.technology_mentions = explicit technologies
signals.event_types = hiring, expansion or capability-investment hypothesis
```

## 6. Example job envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "JOB_BOARD", "mode": "JOB_BOARD_API_LICENSED"},
  "native": {"object_type": "job_posting", "object_id": "provider-job-123", "parent_id": "provider-employer-55", "url": "https://jobs.example/job-123"},
  "entity_hints": {
    "organization_names": ["Example Foods"],
    "addresses": ["Faisalabad, Pakistan"],
    "provider_identifiers": [
      {"type": "JOB_BOARD_EMPLOYER_ID", "value": "provider-employer-55"},
      {"type": "JOB_BOARD_JOB_ID", "value": "provider-job-123"}
    ]
  },
  "content": {
    "title": "Production Planning Manager",
    "summary": "Licensed job record requests production planning and ERP experience.",
    "language": "en",
    "published_at": "2026-07-28T00:00:00Z",
    "content_type": "job_posting"
  },
  "signals": {
    "activity_codes": ["ACT-PRD-016"],
    "technology_mentions": ["ERP"],
    "event_types": ["HIRING_SIGNAL"]
  },
  "policy": {
    "authorization_basis": "LICENSED_API",
    "retention_policy": "JOB_BOARD_PROVIDER_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
JOB_BOARD_SUCCESS
JOB_BOARD_ZERO_RESULTS
JOB_BOARD_JOB_EXPIRED
JOB_BOARD_JOB_REMOVED
JOB_BOARD_EMPLOYER_UNRESOLVED
JOB_BOARD_DUPLICATE_POSTING
JOB_BOARD_LOCATION_AMBIGUOUS
JOB_BOARD_RATE_LIMITED
JOB_BOARD_LICENSE_BLOCKED
JOB_BOARD_POLICY_BLOCKED
```

## 8. Evidence boundaries

Job boards may support hiring, role, technology, department, location and organizational-change evidence.

They do not independently prove a planned purchase, current budget, service absence, employee identity, contact permission or a qualified opportunity.

## 9. Delivery boundary

This document does not implement provider adapters, employer resolution, job normalization, technology extraction, retention or scoring.