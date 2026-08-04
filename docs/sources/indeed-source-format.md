# Harvester Indeed Source Format

Status: **Proposed source and formatting contract**  
Version: **1.0**  
Date: **4 August 2026**  
Implementation status: **Not implemented**  
External-reference review: **Indeed Partner APIs, Hiring Lab access, employer data, job synchronization, licensing and partner eligibility must be revalidated before implementation**

## 1. Purpose

This document defines how customer-authorized, partner-approved, licensed, imported, or manually referenced Indeed employer and job information may enter Harvester.

Harvester must not scrape Indeed search pages, employer pages, resumes, candidate data, or job listings through browser automation.

## 2. Source modes

```text
INDEED_PARTNER_EMPLOYER_AUTHORIZED
INDEED_PARTNER_JOB_AUTHORIZED
INDEED_HIRING_LAB_LICENSED
INDEED_AUTHORIZED_IMPORT
INDEED_OPERATOR_REFERENCE
```

Indeed partner APIs are designed for approved integration use cases. Access to one API does not imply access to employer search, candidate data, or a general prospecting database.

## 3. User configuration

```text
mode
partner_account_reference
credential_reference_id
ats_identifier
employer_identifiers
job_identifiers
approved_api_products
approved_scopes
country_codes
language_codes
job_status_filters
occupation_filters
location_filters
freshness_window
field_profile_version
request_budget
retention_policy_version
deletion_policy_version
import_authorization_reference
operator_reference_urls
```

Candidate and application data are out of scope for lead discovery unless a separate customer-owned operational use case, privacy basis, and source document are approved.

## 4. Native objects

| Native object | Identifier | Role |
| --- | --- | --- |
| Employer | Indeed or partner employer ID | Hiring organization reference |
| Job posting | Indeed job ID or partner external ID | Hiring, capability and timing evidence |
| Job location | Job and location identifiers | Branch or operating-location hint |
| Hiring Lab record | Dataset-specific key | Licensed labor-market evidence |
| Authorized import row | Customer external ID | Customer-owned or licensed job record |
| Operator reference | Indeed URL | Manual navigation and bounded assertion |

## 5. Canonical formatting

### Employer observation

```text
source.code = INDEED
source.mode = INDEED_PARTNER_EMPLOYER_AUTHORIZED
native.object_type = employer
native.object_id = Indeed or partner employer identifier
entity_hints.organization_names = employer name
entity_hints.domains = approved employer website field when supplied
entity_hints.addresses = approved employer location fields
entity_hints.provider_identifiers = ATS identifier plus employer identifier
policy.authorization_basis = PARTNER_CONTRACT
```

### Job observation

```text
native.object_type = job_posting
native.object_id = Indeed job ID or partner external job ID
native.parent_id = employer identifier
native.url = permitted job URL
content.title = job title
content.summary = bounded normalized description or reference
content.published_at = job creation or publication date
entity_hints.organization_names = hiring company
entity_hints.addresses = job location
signals.job_roles = normalized role
signals.activity_codes = activity evidence inferred through approved rules
signals.technology_mentions = explicit technology requirements
signals.event_types = hiring, expansion or capability-investment hypothesis
```

## 6. Example job envelope

```json
{
  "schema_version": "1.0",
  "source": {"code": "INDEED", "mode": "INDEED_PARTNER_JOB_AUTHORIZED"},
  "native": {
    "object_type": "job_posting",
    "object_id": "job-123",
    "parent_id": "employer-456",
    "url": "https://example.com/jobs/job-123"
  },
  "entity_hints": {
    "organization_names": ["Example Distribution Company"],
    "addresses": ["Lahore, Pakistan"],
    "provider_identifiers": [
      {"type": "INDEED_EMPLOYER_ID", "value": "employer-456"},
      {"type": "INDEED_JOB_ID", "value": "job-123"}
    ]
  },
  "content": {
    "title": "Warehouse Systems Manager",
    "summary": "Authorized job record describing warehouse-system responsibilities.",
    "language": "en",
    "published_at": "2026-08-01T00:00:00Z",
    "content_type": "job_posting"
  },
  "signals": {
    "activity_codes": ["ACT-LOG-003"],
    "event_types": ["HIRING_SIGNAL"],
    "job_roles": ["warehouse systems manager"]
  },
  "policy": {
    "authorization_basis": "PARTNER_CONTRACT",
    "retention_policy": "INDEED_PRODUCT_SPECIFIC",
    "attribution_required": true,
    "redistribution_allowed": false,
    "model_training_allowed": false
  }
}
```

## 7. Outcome states

```text
INDEED_SUCCESS
INDEED_ZERO_RECORDS
INDEED_PARTNER_ACCESS_REQUIRED
INDEED_ATS_IDENTIFIER_INVALID
INDEED_EMPLOYER_NOT_REGISTERED
INDEED_JOB_NOT_FOUND
INDEED_JOB_EXPIRED
INDEED_JOB_REMOVED
INDEED_MODERATION_REJECTED
INDEED_RATE_LIMITED
INDEED_SCOPE_REJECTED
INDEED_IMPORT_AUTHORIZATION_MISSING
INDEED_POLICY_BLOCKED
```

## 8. Retention and privacy

- Retain the stable pairing of ATS identifier and employer identifier when required for correct employer association.
- Preserve job source, external ID, employer ID, dates, status, location, and provenance.
- Expired, removed, or moderated jobs remain historical observations only when the active agreement permits retention.
- Candidate, application, resume, disposition, and personal-contact data require a separate operational purpose and privacy model.
- Imported data must declare owner, license, purpose, export date, retention, and deletion obligations.

## 9. Evidence boundaries

Indeed may support hiring activity, role demand, location growth, technology requirements, operational capability, and customer-authorized employer information.

A job posting does not prove current budget, procurement authority, guaranteed expansion, service absence, or consent to contact individuals named in the posting.

## 10. Delivery boundary

This document does not implement Indeed partner onboarding, APIs, employer registration, job synchronization, imports, labor-market datasets, parsing, evidence extraction, or scoring.