# Harvester Raw Source Response Preservation Standard

Status: **Proposed**  
Version: **1.0**  
Date: **5 August 2026**  
Implementation status: **Not implemented**

This standard defines the relationship between source-request minimization and long-term raw-response preservation.

The governing rule is:

> **Request only the fields required for the approved source purpose. Preserve the complete response actually returned as an immutable raw snapshot whenever retention is legally, contractually, and provider-permitted.**

Harvester must not request speculative fields merely because they may become interesting later. It must also not discard a permitted source response merely because the current extraction logic used only part of it.

## 1. Request-minimization rule

Every source request must be limited to the smallest field set, record scope, date range, geography, page count, and query breadth required for the approved Harvest Job objective.

A request may include a field only when all of the following are true:

1. The field supports an approved source purpose.
2. The source interface and authorization permit the field.
3. The field is required for discovery, verification, evidence, compliance, or an approved downstream decision.
4. Its cost, sensitivity, and retention consequences are understood.
5. Its inclusion is represented by a versioned field mask, projection, schema mapping, or request profile.

The following are prohibited:

- requesting every available field by default;
- requesting sensitive fields merely for possible future use;
- expanding a request because a keyword profile contains an unrelated term;
- collecting expensive enrichment fields before deduplication when a cheaper discovery stage is sufficient;
- silently changing field masks or response projections during a running Harvest Job.

## 2. Complete returned-response rule

When a source returns a response, Harvester should preserve the complete returned response envelope permitted by the applicable source policy.

This includes, where available and permitted:

- source class and provider;
- source mode and authorization profile;
- request identifier;
- request method and documented endpoint class;
- rendered query, field mask, projection, filters, page token, geography, and date window;
- response status and source-native outcome;
- response headers that are safe and permitted to retain;
- complete response body or exact returned bytes;
- content type, encoding, compression, and schema version;
- provider-native record and page identifiers;
- retrieval start and completion times;
- adapter, parser, query-profile, source-policy, and retention-policy versions;
- response checksum and storage-object checksum;
- tenant, Harvest Job, source run, query, page, and retry relationships;
- truncation, pagination, partial-success, warning, and error information.

Secrets, credentials, authorization tokens, session cookies, private request headers, and other security material must be removed before preservation.

## 3. Immutability and versioning

A retained raw response is append-only.

Harvester must not overwrite an earlier response when:

- the same query is executed again;
- the source record changes;
- a parser or classifier improves;
- an entity is resolved differently;
- a duplicate is identified;
- the source later contradicts or supersedes the earlier response.

Each retrieval creates a new immutable snapshot linked to the earlier source history.

```text
Source request
→ immutable raw response snapshot
→ extraction version
→ normalized observations
→ evidence candidates
→ decisions and outputs
```

A later correction creates new records. It does not rewrite the historical source response.

## 4. Responses that must be preserved

Where policy permits, preservation applies to:

- successful responses;
- empty-result responses;
- partial responses;
- paginated responses;
- warnings;
- validation errors;
- authentication and authorization failures after secret removal;
- rate-limit and quota responses;
- provider errors;
- timeout and transport outcomes represented by the adapter;
- retry responses;
- amendments, deletions, corrections, and superseding responses.

An empty response and a failed request are different historical facts and must not collapse into one state.

## 5. Permanent-by-default retention

For source content that Harvester is permitted to retain, the default retention class is:

```text
INDEFINITE_ARCHIVAL
```

The purpose is to support:

- future reprocessing with improved parsers and classifiers;
- historical comparison;
- audit and explainability;
- contradiction and supersession analysis;
- source-quality evaluation;
- recovery from normalization defects;
- reproducible decisions;
- legally permitted future Harvester use.

Indefinite retention does not make the payload automatically eligible for every future purpose.

Future use remains subject to the authorization, lawful basis, provider policy, tenant scope, purpose limitation, consent, suppression, and access rules applicable at the time of use.

## 6. Mandatory retention exceptions

Harvester must not promise literal retention “no matter what.”

Raw content must be deleted, shortened, transformed, isolated, or prevented from long-term storage when required by:

- applicable law or binding legal process;
- source-provider terms, API policy, licence, attribution, or caching limits;
- customer contract or tenant deletion obligation;
- privacy, consent withdrawal, data-subject, or suppression requirements;
- security incident containment;
- intellectual-property or confidentiality restrictions;
- a documented lack of lawful authorization;
- an approved source-specific retention profile that is stricter than this standard.

Provider-specific source models override the generic indefinite-retention default.

For example, the Google API source model states that some Google Maps content must not be stored indefinitely and that Google-specific compliance rules override generic raw-retention behavior.

## 7. Audit tombstone for mandatory deletion

When a raw response must be deleted, Harvester should retain a non-content audit tombstone where legally and contractually permitted.

The tombstone may include:

- raw snapshot identifier;
- source class and provider;
- request and response identifiers;
- Harvest Job and source-run relationships;
- collection timestamp;
- original checksum;
- content type and approximate size;
- retention-policy version;
- deletion or expiry reason;
- authority requiring deletion;
- approval and execution timestamps;
- deletion verification result.

The tombstone must not retain the prohibited response content or allow it to be reconstructed.

## 8. Raw archive and normalized data remain separate

Raw response preservation does not make every returned field canonical Harvester data.

```text
Raw response snapshot
≠ verified fact
≠ canonical entity field
≠ confirmed activity
≠ opportunity
≠ contact permission
```

Normalization, entity resolution, evidence assessment, freshness, contradiction review, provider-offering relevance, qualification, and contact policy remain separate governed processes.

The raw snapshot is the historical source record. Derived data must link back to it through explicit provenance.

## 9. Deduplication rule

Deduplication must prevent repeated responses from inflating evidence diversity, scoring, or source coverage.

It must not silently delete permitted raw snapshots.

Harvester may:

- cluster identical payloads;
- use checksums and provider identifiers;
- store repeated payload bodies through content-addressed storage;
- reference one physical immutable object from several logical response records;
- compress permitted archives;
- mark mirrors, retries, pages, and repeated imports as shared origins.

Logical history and provenance must remain complete even when physical storage is optimized.

## 10. Security and access

Raw source responses must use:

- encryption in transit and at rest;
- tenant-aware access controls where tenant data is involved;
- role- and purpose-based access;
- immutable audit logging;
- secret and credential redaction;
- integrity checks;
- malware and unsafe-file controls for downloaded content;
- backup and recovery aligned with the retention class;
- separate handling for sensitive, restricted, or quarantined payloads.

The raw archive must not become a convenient ungoverned data lake with a reassuring name.

## 11. Minimum conceptual records

```text
SourceRequest
RawSourceResponseSnapshot
RawResponseObject
RawResponseRetentionDisposition
RawResponseDeletionTombstone
DerivedObservationLink
```

### `SourceRequest`

Minimum fields:

```text
id
harvest_job_id
source_run_id
source_class
provider
source_mode
request_profile_version
field_mask_or_projection_version
query
filters
page_token
requested_at
```

### `RawSourceResponseSnapshot`

Minimum fields:

```text
id
source_request_id
provider_response_id
outcome
http_status
source_native_status
raw_object_id
response_checksum
schema_or_media_type
retrieved_at
adapter_version
parser_version
source_policy_version
retention_policy_version
retention_disposition
supersedes_snapshot_id
```

### `RawResponseRetentionDisposition`

Suggested values:

```text
INDEFINITE_ARCHIVAL
TIME_LIMITED_PROVIDER_POLICY
TIME_LIMITED_CONTRACT
TRANSIENT_PROCESSING_ONLY
QUARANTINED
LEGAL_HOLD
DELETION_REQUIRED
DELETED_WITH_TOMBSTONE
```

## 12. Acceptance criteria

- Source requests use only required approved fields.
- Field masks, projections, mappings, and query scopes are versioned.
- Complete permitted responses are preserved without requesting unnecessary fields.
- Successful, empty, partial, failed, paginated, and retry outcomes remain distinguishable.
- Raw snapshots are append-only and independently addressable.
- Reprocessing creates new derived records without rewriting source history.
- Deduplication does not inflate evidence or destroy permitted provenance.
- Provider, legal, privacy, contractual, and deletion rules override indefinite retention.
- Mandatory deletion leaves a non-reconstructive audit tombstone where permitted.
- Raw content remains separate from verified evidence and canonical data.
- Runtime implementation is not falsely claimed.

## 13. Related documents

- [Harvester Source Specification Index](README.md).
- [Source Query Template Library](../source-query-template-library.md).
- [Source-to-Signal Matrix](../source-signal-matrix.md).
- [Google API Source and Extraction Model](../../../sources/google-api-source-model.md).
- [Yandex Maps API Source and Extraction Model](../../../sources/yandex-maps-api-source-model.md).
- [LinkedIn Authorized Data Source Model](../../../sources/linkedin-authorized-data-source-model.md).
- [User Input Storage Model](../../../sources/user-input-storage-model.md).

## 14. Delivery boundary

This standard defines planned documentation and data-governance requirements. It does not implement source adapters, database schemas, object storage, encryption, retention jobs, deletion workflows, legal holds, audit tombstones, reprocessing, or releases.
