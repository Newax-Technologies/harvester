# Harvester Source Adapter Documentation Template

Status: **Proposed template**  
Version: **1.0**  
Date: **4 August 2026**

Every new source adapter must receive a separate Markdown document using this structure before production activation.

## 1. Source identity

```text
source_code
source_family
source_modes
provider
implementation_state
last_external_reference_review
```

## 2. Approved purpose

State what the source contributes, such as:

- organization discovery
- branch discovery
- organization-owned content
- customer-authorized analytics
- job and hiring evidence
- legal registration evidence
- news and event evidence
- public contact paths

State what the source must not be used to infer.

## 3. Authorization and permission basis

For each mode, define one of:

```text
PUBLIC_API
CUSTOMER_OAUTH
MEMBER_CONSENT
PARTNER_CONTRACT
LICENSED_DATASET
CUSTOMER_AUTHORIZED_IMPORT
PUBLIC_WEBSITE_WITH_ROBOTS_COMPLIANCE
MANUAL_OPERATOR_REFERENCE
```

Document prohibited acquisition methods.

## 4. User configuration

Define the validated fields accepted from the user or operator:

```text
mode
connection_reference
credential_reference
object identifiers
queries
keywords
geography
language
field profile
page limits
request budget
cost budget
freshness window
retention profile
attribution profile
review requirements
```

## 5. Accepted provider-native objects

List each object type and provider identifier.

Example:

| Native object | Native identifier | Primary role |
| --- | --- | --- |
| Organization | Provider organization ID | Organization hint |
| Post | Provider post ID | Public statement or event evidence |
| Job | Provider job ID | Hiring and capability evidence |

## 6. Canonical formatting

Map provider fields to the [Canonical Source Record Format](canonical-source-record-format.md).

Required mapping groups:

```text
native identity
entity hints
content
location
contact paths
classification
activity signals
event signals
metrics
provenance
quality
policy
```

## 7. Outcome and failure states

Define zero results, partial results, deleted objects, permission failures, rate limits, parsing failures, policy blocks, and retry behavior separately.

## 8. Retention, attribution and deletion

Define:

```text
raw payload policy
normalized-field policy
cache duration
attribution requirement
redistribution rule
model-training rule
deletion trigger
contract-termination behavior
customer deletion behavior
```

## 9. Evidence and scoring boundaries

State which evidence dimensions the source may support and which decisions it cannot make.

## 10. Security and privacy

Define credential isolation, tenant ownership, personal-data limits, consent, suppression, audit, webhook validation, and secret rotation requirements.

## 11. Example source envelope

Provide at least one redacted JSON example using the canonical envelope.

## 12. Acceptance criteria

A source document is incomplete unless it defines:

- user-input schema
- permission basis
- native objects
- field mapping
- outcome taxonomy
- retention policy
- provenance behavior
- evidence boundaries
- security requirements
- implementation and verification gates

## 13. Delivery boundary

State clearly whether the adapter is proposed, partially implemented, restricted, verified, or production-active. Documentation alone is not runtime implementation.