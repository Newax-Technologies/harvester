# NEWAX Harvester LinkedIn Authorized Data Source Model

Status: **Normative planned source architecture**  
Source family: **LinkedIn authorized organization, member-consented, partner, imported, and operator-referenced data**  
Document version: **v1**  
Implementation state: **Authorized API architecture is planned; the existing stealth crawler is a quarantined legacy component and is not an approved production source**  
Last external-reference review: **2026-08-03**  

Authority: This document defines how NEWAX Harvester may discover, receive, verify, retain, explain, score, and use LinkedIn-related information. It does not create a second roadmap and does not claim that the current runtime already follows this model.

Read with:

- [Harvester Standalone Product Roadmap](../ROADMAP.md)
- [Harvester Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md)
- [NEWAX Harvester Opportunity Scoring Model v3](../architecture/opportunity-scoring-model-v3.md)
- [Standalone Product and Integration Framework](../architecture/standalone-product-and-integration-framework.md)
- [Google API Source and Extraction Model](google-api-source-model.md)
- [Yandex Maps API Source and Extraction Model](yandex-maps-api-source-model.md)

Official references reviewed for this version:

- LinkedIn User Agreement: <https://www.linkedin.com/legal/user-agreement>
- LinkedIn prohibited software and extensions: <https://www.linkedin.com/help/linkedin/answer/a1341387/prohibited-software-and-extensions>
- LinkedIn automated activity policy: <https://www.linkedin.com/help/linkedin/answer/a1340567/automated-activity-on-linkedin>
- LinkedIn crawling terms: <https://www.linkedin.com/legal/crawling-terms>
- Getting access to LinkedIn APIs: <https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access>
- Community Management overview: <https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview>
- Community Management application review: <https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review>
- Sales Navigator Application Platform: <https://learn.microsoft.com/en-us/linkedin/sales/>

---

## 1. Purpose

LinkedIn can provide valuable evidence about organizations, professional roles, company activity, growth, hiring, leadership changes, and customer-authorized page performance.

LinkedIn cannot be treated as an unrestricted public prospect database.

This document answers:

1. Which LinkedIn source modes Harvester may support.
2. Which modes require OAuth, customer authorization, partner approval, or manual operator input.
3. How LinkedIn organization data differs from LinkedIn member data.
4. How customer-owned Company Page posts and analytics may enter Harvester.
5. How a consenting member may connect their own identity.
6. How approved Sales Navigator integrations may be used if partner access becomes available.
7. How customer-authorized imports should be governed.
8. How operator references should remain bounded.
9. How the current LinkedIn stealth crawler must be quarantined and retired.
10. How LinkedIn evidence may influence Opportunity Scoring Model v3.
11. How AI-derived role, pain, intent, and outreach hypotheses must be controlled.
12. Which privacy, consent, retention, deletion, security, and audit controls are required.
13. What must be implemented and verified before production activation.

The goal is not to copy LinkedIn into Harvester.

The goal is to use authorized LinkedIn capabilities as bounded evidence sources inside a customer-controlled business-infrastructure system.

---

## 2. Locked source boundary

Harvester recognizes five approved LinkedIn source modes:

```text
LINKEDIN_ORGANIZATION_AUTHORIZED
LINKEDIN_MEMBER_CONSENTED
LINKEDIN_SALES_NAVIGATOR_PARTNER
LINKEDIN_AUTHORIZED_IMPORT
LINKEDIN_OPERATOR_REFERENCE
```

Harvester also recognizes one temporary legacy component state:

```text
LINKEDIN_LEGACY_RESTRICTED_CRAWLER
```

The legacy restricted crawler is not an approved source mode.

It exists only to:

- Make the current repository state explicit.
- Preserve migration and forensic context.
- Prevent hidden continued use.
- Support controlled removal planning.
- Avoid pretending the code never existed.

API approval delay does not convert prohibited browser automation into an authorized interim source.

---

## 3. Provider-rule baseline

LinkedIn states that it does not permit third-party crawlers, bots, browser extensions, scripts, or other automated methods that scrape, copy, or automate activity on LinkedIn.

LinkedIn's User Agreement also prohibits:

- Copying login cookies.
- Using another person's account.
- Scraping profiles or other LinkedIn data.
- Circumventing access controls or use limits.
- Automating messages, connections, reactions, comments, or other engagement.
- Copying or distributing LinkedIn information without the required consent.

LinkedIn's crawling terms state that automated crawling requires express permission.

Therefore:

```text
Public visibility
≠ permission for automated collection
```

and:

```text
Customer login
≠ authorization to automate LinkedIn through that customer's browser session
```

---

## 4. Source-mode overview

| Mode | Primary use | Authorization basis | Prospect discovery | Durable storage |
|---|---|---|---|---|
| `LINKEDIN_ORGANIZATION_AUTHORIZED` | Customer-administered Company Page data and analytics | OAuth plus approved API product and Page-admin authority | No general platform search | Only within approved API terms |
| `LINKEDIN_MEMBER_CONSENTED` | Consenting member's own identity and permitted profile data | Member OAuth consent | No arbitrary member search | Only consented fields and approved purposes |
| `LINKEDIN_SALES_NAVIGATOR_PARTNER` | Approved CRM and Sales Navigator workflows | LinkedIn partner approval and customer authorization | Only contract-approved capabilities | Contract-specific |
| `LINKEDIN_AUTHORIZED_IMPORT` | Customer-owned or licensed LinkedIn-related records | Customer or provider authorization | Depends on imported source rights | According to import license and privacy policy |
| `LINKEDIN_OPERATOR_REFERENCE` | Human-reviewed URL or bounded assertion | Manual research policy | Manual only | Minimal reference and operator assertion |
| `LINKEDIN_LEGACY_RESTRICTED_CRAWLER` | Migration context only | Contested account automation | Prohibited as production acquisition | No new production persistence |

---

# 5. `LINKEDIN_ORGANIZATION_AUTHORIZED`

## 5.1 Purpose

This mode connects a LinkedIn Company Page that the customer or authorized operator administers.

It is the preferred LinkedIn API path for customer-owned organization activity and analytics.

## 5.2 Access requirements

Typical requirements include:

- Registered legal organization.
- LinkedIn developer application.
- Verified business email.
- Verified organization website and domain.
- Privacy policy.
- LinkedIn Page associated with the same organization.
- Super-admin verification of the application.
- Approved Community Management use case.
- Development-tier approval.
- Standard-tier technical review when required.
- OAuth authorization by an appropriately privileged member.

## 5.3 Availability limits

Community Management is a vetted product.

Development access is not automatic.

Default development-tier request limits may be materially lower than production needs and must be read from current LinkedIn documentation before deployment.

## 5.4 Permitted organization data

Depending on approved scopes and API versions, this mode may support:

- Organization ID and URN.
- Organization name.
- Vanity name.
- Organization website.
- Locations.
- Organization type.
- Logo or approved media reference.
- Company Page posts.
- Comments and reactions.
- Follower statistics.
- Page views and clicks.
- Organic post statistics.
- Video statistics.
- Organization notifications.

Harvester must request only the fields required by the approved use case.

## 5.5 Organization authorization record

Recommended object:

```text
LinkedInOrganizationConnection
```

Fields:

```text
id
tenant_id
organization_id
organization_urn
linkedin_page_url
vanity_name
authorizing_member_id
authorizing_member_urn
verified_admin_role
approved_product
approved_scopes
access_tier
api_version
access_token_secret_ref
refresh_token_secret_ref
token_expires_at
connected_at
last_verified_at
revoked_at
status
```

## 5.6 Connection states

```text
PENDING_VERIFICATION
ACTIVE
TOKEN_EXPIRING
REAUTHORIZATION_REQUIRED
REVOKED
INSUFFICIENT_ROLE
API_PRODUCT_UNAVAILABLE
SCOPE_REJECTED
SUSPENDED
```

## 5.7 Organization observations

Every retrieved object should retain:

```text
connection_id
linkedin_object_type
linkedin_object_id
organization_urn
api_version
requested_fields
retrieved_at
provider_updated_at
permission_scope
source_payload_policy
retention_policy
response_hash
```

## 5.8 Posts

Authorized organization posts may support:

- Expansion announcements.
- New branch announcements.
- Product or service launches.
- Technology programme announcements.
- Hiring campaigns.
- Partnerships.
- Operational changes.
- Event activity.
- Customer-service updates.

Posts remain organization-authored claims.

They may be promotional and should be corroborated where material.

## 5.9 Page and post analytics

Authorized analytics may support:

- Page views.
- Page clicks.
- Follower growth.
- Audience geography.
- Audience seniority or function where permitted.
- Post impressions.
- Post clicks.
- Reactions.
- Comments.
- Shares.
- Video views and watch time.

These metrics are most useful for customer-owned business intelligence.

They are not a general cold-prospect data source.

## 5.10 Scoring use

Authorized organization data may support:

```text
Account Value and Scale
Buying Intent and Timing
Evidence Quality and Freshness
Strategic and ICP Fit
```

Examples:

| Authorized signal | Potential v3 use |
|---|---|
| Sustained follower growth | Supporting activity or market-reach evidence |
| New location announcement | Expansion trigger |
| Hiring technology leadership | Buying-timing hypothesis |
| System-launch announcement | Active initiative evidence |
| High page engagement | Supporting audience-demand context |

Follower count, impressions, and reactions must not directly become opportunity points without a versioned interpretation policy.

---

# 6. `LINKEDIN_MEMBER_CONSENTED`

## 6.1 Purpose

This mode allows an individual member to authenticate and consent to sharing permitted information about themselves.

## 6.2 Appropriate uses

- Sign in to Harvester.
- Verify operator identity.
- Connect a customer representative to an organization.
- Verify a customer-provided contact record.
- Populate the consenting member's own profile fields.
- Support consented employee-directory workflows.

## 6.3 Prohibited interpretation

A consenting member's token does not authorize Harvester to retrieve arbitrary profiles, contacts, connections, colleagues, followers, or prospects.

## 6.4 Consent record

Recommended object:

```text
LinkedInMemberConsent
```

Fields:

```text
id
tenant_id
member_id
member_urn
subject_user_id
consent_version
approved_scopes
approved_purposes
consented_at
expires_at
revoked_at
deletion_requested_at
status
```

## 6.5 Consent states

```text
ACTIVE
EXPIRED
REVOKED
DELETION_PENDING
DELETED
SCOPE_REDUCED
REAUTHORIZATION_REQUIRED
```

## 6.6 Permitted member data

Depending on open permissions, approved product, and consent:

- Name.
- Profile picture.
- Primary email.
- Headline.
- Profile URL or approved identifier.
- Current workplace.
- Recent education.
- Verified identity attributes where supported.

Only fields actually returned under the approved scope may be stored.

## 6.7 Person-role verification

A consented current-workplace claim may support:

```text
Person identity
Organization association
Current role
Role freshness
```

It does not prove:

- Procurement authority.
- Budget authority.
- Active buying intent.
- Infrastructure pain.
- Consent to marketing messages.

## 6.8 Scoring use

Member-consented data may support:

```text
Contactability and Decision-Maker Access
Identity Confidence
Evidence Quality
```

Any authority grade must be based on role relevance and corroboration, not merely seniority language.

---

# 7. `LINKEDIN_SALES_NAVIGATOR_PARTNER`

## 7.1 Purpose

This mode represents a future approved integration with the Sales Navigator Application Platform or successor partner product.

## 7.2 Current availability

At the last external review, LinkedIn stated that it was not accepting new Sales Navigator API partners.

Harvester must treat this mode as:

```text
PLANNED_PARTNER_DEPENDENCY
```

It must not be used as a prerequisite for core Harvester operation.

## 7.3 Potential future capabilities

Subject to partner approval and contract:

- CRM record validation.
- Approved lead and account matching.
- Sales Navigator links.
- Matched profile display.
- Account and lead alerts.
- Partner-approved search experience.
- Customer-authorized CRM synchronization.

## 7.4 Contract-first behavior

No endpoint, field, cache policy, or workflow may be assumed before:

- Partner approval.
- Signed product agreement.
- Approved scopes.
- Approved customer experience.
- Data-storage review.
- Security review.
- Technical sign-off.

## 7.5 Product independence

Harvester must remain useful without Sales Navigator.

```text
Sales Navigator unavailable
→ Harvester continues through other approved sources
```

---

# 8. `LINKEDIN_AUTHORIZED_IMPORT`

## 8.1 Purpose

This mode imports LinkedIn-related records that a customer or licensed provider is authorized to supply.

## 8.2 Accepted sources

Examples may include:

- Customer CRM export.
- Approved Sales Navigator CRM synchronization export.
- Customer-maintained contact list.
- Customer employee directory.
- Consent-backed professional-contact records.
- Licensed business-data provider.
- Manually reviewed spreadsheet.

## 8.3 Required declaration

Every import must declare:

```text
source_reference
data_owner
authorization_basis
license_reference
permitted_purposes
prohibited_purposes
exported_at
retention_period
deletion_policy
contacting_basis
customer_attestation
```

## 8.4 Import record

Recommended object:

```text
LinkedInAuthorizedImport
```

Fields:

```text
id
tenant_id
source_reference
file_reference
checksum
data_owner
license_reference
authorization_basis
permitted_purposes
retention_days
imported_at
imported_by
record_count
accepted_count
rejected_count
status
```

## 8.5 Imported person record

Recommended fields:

```text
external_record_id
linkedin_profile_url
linkedin_member_identifier
full_name
headline
current_company
current_role
location
email
phone
recorded_at
source_updated_at
consent_or_business_basis
suppression_status
```

Missing values remain unknown.

## 8.6 Import validation

Reject or review records when:

- Authorization basis is missing.
- License terms are unknown.
- Data owner cannot be identified.
- Source reference is absent.
- Retention rules are absent.
- Contacting basis is absent where required.
- The record contains sensitive or excessive personal data.
- The profile URL is malformed.
- Organization attribution conflicts with stronger evidence.

## 8.7 Deduplication

Imported LinkedIn URLs or identifiers are provider references.

They should be linked to Harvester person candidates through resolution, not adopted as canonical identity without corroboration.

---

# 9. `LINKEDIN_OPERATOR_REFERENCE`

## 9.1 Purpose

This mode stores a bounded LinkedIn reference reviewed or supplied by a human operator.

## 9.2 Allowed reference fields

```text
linkedin_profile_url
linkedin_organization_url
reference_type
observed_at
observed_by
research_purpose
operator_note
```

## 9.3 Operator assertions

An operator may separately assert:

- Person appears associated with organization.
- Person appears to hold a named role.
- Company Page appears to be official.
- A visible announcement may warrant independent research.

Operator assertions must remain distinct from provider facts.

## 9.4 Prohibited automation

The operator-reference mode does not authorize Harvester to:

- Open the URL automatically.
- Capture the page automatically.
- Extract profile sections.
- Download HTML.
- Take automated screenshots.
- Harvest search results.
- Traverse connections.
- Send messages.
- Send connection requests.

## 9.5 Manual-research provenance

Recommended fields:

```text
assertion_id
operator_id
reference_url
assertion_type
assertion_text
observed_at
confidence
corroboration_required
review_state
```

---

# 10. `LINKEDIN_LEGACY_RESTRICTED_CRAWLER`

## 10.1 Current repository reality

The repository currently contains LinkedIn browser-automation code that:

- Stores login cookies.
- Restores browser session state.
- Uses a browser automation framework.
- Applies anti-detection techniques.
- Simulates human behavior.
- Uses action budgets.
- Supports proxies.
- Detects and reacts to CAPTCHA challenges.
- Visits member profile URLs.
- Extracts profile fields.
- Persists raw profile payloads.
- Sends extracted profile data into an AI research workflow.

This component is currently represented by files including:

```text
src/lead_harvester/sources/linkedin_stealth.py
src/lead_harvester/sources/account_farm.py
src/lead_harvester/sources/session_manager.py
src/lead_harvester/sources/device_profile.py
src/lead_harvester/sources/human_emulator.py
```

## 10.2 Classification

The component is classified:

```text
LEGACY
CONTESTED
RESTRICTED
NOT_APPROVED_FOR_PRODUCTION
PENDING_REPLACEMENT
```

It is not classified as an approved source merely because the code exists.

## 10.3 Temporary retention purpose

The code may remain temporarily in the repository only for:

- Migration planning.
- Test-history preservation.
- Data-lineage review.
- Removal sequencing.
- Replacement comparison.
- Security review.

## 10.4 Required restrictions

Until removal or explicit written LinkedIn authorization:

```text
Production execution: BLOCKED
Scheduled execution: BLOCKED
Multi-account farming: BLOCKED
CAPTCHA solving: BLOCKED
Proxy-based evasion: BLOCKED
Fingerprint spoofing: BLOCKED
Automated login: BLOCKED
Cookie copying between users: BLOCKED
Profile scraping: BLOCKED
LinkedIn search scraping: BLOCKED
Message automation: BLOCKED
Connection automation: BLOCKED
Reaction automation: BLOCKED
Post automation outside approved APIs: BLOCKED
```

## 10.5 Feature freeze

No new capability should be added to the legacy crawler.

Prohibited enhancements include:

- Stronger stealth.
- New proxy rotation.
- CAPTCHA bypass.
- Larger account farms.
- Faster profile extraction.
- Search-result harvesting.
- Connection graph extraction.
- Message sequencing.
- Anti-detection tuning.

## 10.6 Kill switch

Recommended configuration:

```text
LINKEDIN_LEGACY_CRAWLER_ENABLED=false
```

The production build should require all of the following before any legacy execution path is even reachable:

```text
non_production_environment
explicit_security_exception
explicit_legal_exception
named_operator
bounded test dataset
no messaging
no connection activity
no CAPTCHA solving
no proxy evasion
no persistent production output
```

This exception framework documents risk. It does not imply provider permission.

## 10.7 Data already collected

Existing LinkedIn raw records require review.

Required actions:

1. Identify every `SourceType.LINKEDIN` raw record.
2. Record acquisition method.
3. Identify any derived institutions, people, findings, signals, briefs, drafts, and score effects.
4. Determine retention and deletion requirements.
5. Quarantine unsupported data.
6. Re-verify important facts through approved sources.
7. Remove unsupported score contributions.
8. Preserve only lawful audit metadata where appropriate.

## 10.8 Migration states

```text
UNREVIEWED_LEGACY_DATA
QUARANTINED
INDEPENDENTLY_VERIFIED
AUTHORIZED_BY_IMPORT
AUTHORIZED_BY_CONSENT
DELETION_REQUIRED
DELETED
```

## 10.9 Removal trigger

The legacy crawler should be removed from operational code when one or more replacement paths cover the required use cases:

- Community Management approval.
- Member-consented identity flow.
- Authorized import workflow.
- Operator-reference workflow.
- Approved Sales Navigator partnership.
- Licensed professional-data provider.

Approval for one mode does not automatically authorize all other LinkedIn uses.

---

# 11. Current AI Research Brain audit

## 11.1 Current behavior

The current Research Brain accepts LinkedIn profile fields such as:

- Profile URL.
- Name.
- Headline.
- Company.
- Location.
- About text.
- Experience.
- Education.
- Recent activity.

It asks an AI model to produce:

- Lead score.
- Decision-maker classification.
- Pain points.
- Buying signals.
- Outreach angle.
- Email draft.
- LinkedIn connection note.
- Executive summary.

It persists profile fields as facts and model outputs as inferences.

It also turns inferred pain points and buying signals into individual signal records.

## 11.2 Core weakness

A professional profile rarely proves organizational pain, budget, procurement activity, infrastructure absence, or current buying intent.

A model can generate plausible interpretations that sound specific while remaining unsupported.

## 11.3 Required replacement contract

The analysis must separate:

```text
OBSERVED_FACT
DERIVED_CLASSIFICATION
OPPORTUNITY_HYPOTHESIS
OUTREACH_SUGGESTION
```

Example:

```text
Observed fact:
The profile states “Director of Operations at ABC Hospital.”

Derived classification:
The role may be operationally relevant.

Opportunity hypothesis:
The person may influence workflow or systems decisions.

Not established:
Budget authority, current pain, active project, buying intent, or consent to outreach.
```

## 11.4 Confidence correction

The model must not assign a fixed confidence such as `0.85` to every generated pain point or buying signal.

Confidence should reflect:

- Source authorization.
- Field freshness.
- Directness of the statement.
- Organization attribution.
- Role attribution.
- Corroboration.
- Contradictions.
- Inference distance.

## 11.5 AI inference record

Recommended fields:

```text
id
source_observation_ids
inference_type
inference_text
observed_support
unsupported_assumptions
confidence_dimensions
contradictions
model_version
prompt_version
created_at
review_state
```

## 11.6 Score boundary

AI-generated hypotheses must not directly earn Opportunity Scoring Model v3 points unless the scoring policy explicitly allows that inference type and required corroboration is present.

---

# 12. LinkedIn and Opportunity Scoring Model v3

## 12.1 Strategic and ICP fit

Permitted LinkedIn organization evidence may support:

- Organization type.
- Industry.
- Locations.
- Organization description.
- Group relationships.
- Business focus.

It must not automatically determine ICP fit merely because the provider classified the organization.

## 12.2 Account value and scale

Supporting indicators may include:

- Organization size category where permitted.
- Location growth.
- Hiring growth.
- Follower growth.
- Activity growth.
- Multi-market presence.

Follower count is not revenue, employee count, or operational complexity.

## 12.3 Buying intent and timing

This is LinkedIn's strongest potential contribution.

Useful authorized or independently verified signals include:

- New facility announcement.
- New market entry.
- Technology-leadership hiring.
- Operations-leadership hiring.
- Procurement hiring.
- System-launch announcement.
- Integration initiative.
- Automation initiative.
- Data programme.
- Merger or acquisition.
- Funding event.
- Expansion announcement.
- New service line.

Each signal must retain:

```text
signal_type
source_mode
source_object_id
published_at
retrieved_at
organization_urn
claim
confidence
corroboration
freshness_policy
```

## 12.4 Contactability and decision-maker access

Permitted member evidence may support:

- Person name.
- Current role.
- Current organization.
- Role relevance.
- Profile reference.

It does not automatically support:

- Verified email.
- Verified phone.
- Procurement authority.
- Budget authority.
- Communication consent.

## 12.5 Infrastructure gaps

LinkedIn information may create research hypotheses about:

- Hiring for digital systems.
- Announced modernization.
- Manual-process complaints in organization-authored posts.
- System outages publicly acknowledged by the organization.

LinkedIn must not independently confirm:

- No website.
- No CRM.
- No ERP.
- No LMS.
- No workflow automation.
- No Connected Infrastructure.
- Data fragmentation.
- System weakness.
- Manual dependence.

Those conclusions require capability-specific evidence.

## 12.6 Evidence quality

Default authority hierarchy:

```text
Approved API object from authorized organization
> consented member claim
> customer-authorized import
> operator-reviewed reference
> unsupported third-party copy
> legacy scraped record
```

Legacy scraped data should not improve evidence confidence merely because extraction was technically successful.

---

# 13. Communication and consent boundary

LinkedIn identity evidence does not grant communication consent.

Harvester keeps separate:

```text
Professional identity
Organization association
Contact channel
Marketing basis
Communication consent
Suppression status
```

A LinkedIn profile URL is not consent to:

- Send an email.
- Send a LinkedIn message.
- Send a connection request.
- Add the person to a campaign.
- Enrich private contact details.

Communication decisions remain governed by Communicator and applicable law.

---

# 14. Privacy and personal-data controls

## 14.1 Data minimization

Store only fields required for an approved purpose.

Do not collect broad profile histories merely because an API or import makes them available.

## 14.2 Purpose limitation

Every source connection and import must declare:

```text
approved_purpose
approved_fields
approved_processing
approved_retention
approved_destinations
```

## 14.3 Tenant isolation

Member tokens, organization tokens, imported records, derived insights, and deletion requests must remain tenant-isolated.

## 14.4 Sensitive data

Harvester should not intentionally derive or store sensitive personal traits from LinkedIn content unless a separate lawful, necessary, approved workflow exists.

Prohibited default inferences include:

- Religion.
- Health status.
- Ethnicity.
- Political belief.
- Sexual orientation.
- Trade-union membership.
- Family status.

## 14.5 Retention

Retention must be source-mode specific.

```text
Authorized API data
→ provider terms plus tenant policy

Consented member data
→ consent and privacy policy

Authorized import
→ import license and customer instruction

Operator reference
→ minimal operational retention

Legacy scraped data
→ quarantine and deletion review
```

## 14.6 Deletion

Deletion must propagate to:

- Raw observations.
- Normalized person candidates.
- Organization links.
- Search indexes.
- Research findings.
- Signals.
- Account briefs.
- Drafts.
- Score contributions.
- Exports.
- Outbox payloads where legally possible.
- Backup-expiry policy.

---

# 15. Credential and token security

## 15.1 OAuth secrets

Store:

- Client secret in secret management.
- Access tokens encrypted.
- Refresh tokens encrypted.
- Scope list separately.
- Expiration timestamps.
- Revocation state.

Never expose tokens to frontend logs or analytics.

## 15.2 Least privilege

Request only scopes necessary for the approved use case.

## 15.3 Token rotation

Support:

- Expiration.
- Refresh.
- Revocation.
- Customer disconnect.
- Scope reduction.
- Provider invalidation.

## 15.4 Audit

Audit:

- Who connected the account.
- Which organization was authorized.
- Which scopes were granted.
- Which endpoints were called.
- Which data was stored.
- Which data was exported.
- When authorization was revoked.

---

# 16. Failure model

Recommended source outcomes:

```text
SUCCEEDED
NO_DATA
PARTIAL
AUTHORIZATION_REQUIRED
AUTHORIZATION_REVOKED
INSUFFICIENT_SCOPE
INSUFFICIENT_ADMIN_ROLE
API_PRODUCT_NOT_APPROVED
RATE_LIMITED
TOKEN_EXPIRED
INVALID_REQUEST
PROVIDER_UNAVAILABLE
RETENTION_BLOCKED
DELETION_REQUIRED
LEGACY_SOURCE_BLOCKED
```

An API failure must not become evidence that a person, role, post, or organization does not exist.

---

# 17. Source transition and lineage

When a legacy record is replaced by an approved source:

```text
Legacy profile record
→ approved API observation or authorized import
→ identity resolution
→ independent verification
→ new evidence assertions
→ v3 score re-evaluation
→ legacy contribution removed
```

Preserve source-transition metadata:

```text
legacy_record_id
replacement_source_mode
replacement_record_id
verified_at
verified_by
facts_reconfirmed
facts_rejected
derived_records_updated
```

---

# 18. Operator experience

The Lead Dossier should show LinkedIn information by source mode.

Example:

```text
LinkedIn Organization
Status: Authorized
Organization URN: ...
Authorized by: Customer Page administrator
Scopes: ...
Last synchronized: ...

LinkedIn Member
Status: Consented
Role: Director of Operations
Organization association confidence: High
Communication consent: Not granted

Legacy LinkedIn Data
Status: Quarantined
Used in score: No
Replacement required: Yes
```

The interface must not display all LinkedIn-derived values as equally authoritative.

---

# 19. Planned domain objects

Recommended objects:

```text
LinkedInConnectionPolicy
LinkedInOrganizationConnection
LinkedInMemberConsent
LinkedInAuthorizedImport
LinkedInOperatorReference
LinkedInProviderObservation
LinkedInOrganizationActivity
LinkedInAnalyticsObservation
LinkedInPersonRoleAssertion
LinkedInLegacyDataReview
LinkedInSourceTransition
```

## 19.1 `LinkedInConnectionPolicy`

```text
id
version
approved_modes
approved_products
approved_scopes
field_allowlist
retention_policy
deletion_policy
export_policy
scoring_policy
legacy_crawler_policy
approved_by
activated_at
retired_at
```

## 19.2 `LinkedInProviderObservation`

```text
id
tenant_id
source_mode
connection_id
provider_object_type
provider_object_id
organization_urn
member_urn
retrieved_at
provider_updated_at
api_version
permission_scope
payload_policy
response_hash
expires_at
```

## 19.3 `LinkedInPersonRoleAssertion`

```text
id
person_candidate_id
institution_id
role_title
role_category
role_relevance
role_authority_hypothesis
source_observation_id
assertion_type
confidence
valid_from
valid_to
review_state
```

## 19.4 `LinkedInLegacyDataReview`

```text
id
raw_record_id
acquisition_method
review_status
provider_permission_status
personal_data_categories
derived_record_count
score_dependency
replacement_required
deletion_required
reviewed_by
reviewed_at
```

---

# 20. Planned APIs

Conceptual Harvester APIs:

```http
GET  /api/v1/linkedin/policy

POST /api/v1/linkedin/organizations/connect
GET  /api/v1/linkedin/organizations/connections
GET  /api/v1/linkedin/organizations/connections/{id}
POST /api/v1/linkedin/organizations/connections/{id}/reauthorize
DELETE /api/v1/linkedin/organizations/connections/{id}
POST /api/v1/linkedin/organizations/connections/{id}/sync

POST /api/v1/linkedin/members/connect
GET  /api/v1/linkedin/members/consents
DELETE /api/v1/linkedin/members/consents/{id}

POST /api/v1/linkedin/imports
GET  /api/v1/linkedin/imports/{id}

POST /api/v1/linkedin/operator-references
GET  /api/v1/linkedin/operator-references/{id}

GET  /api/v1/linkedin/legacy/reviews
POST /api/v1/linkedin/legacy/reviews/{id}/quarantine
POST /api/v1/linkedin/legacy/reviews/{id}/verify
POST /api/v1/linkedin/legacy/reviews/{id}/delete
```

There should be no production endpoint that starts the legacy stealth crawler.

---

# 21. Events

Suggested events:

```text
linkedin.organization_connection_created
linkedin.organization_connection_revoked
linkedin.organization_sync_completed
linkedin.organization_sync_failed
linkedin.member_consent_created
linkedin.member_consent_revoked
linkedin.authorized_import_completed
linkedin.operator_reference_created
linkedin.legacy_record_quarantined
linkedin.legacy_record_verified
linkedin.legacy_record_deleted
linkedin.source_transition_completed
linkedin.score_recalculation_requested
```

---

# 22. API approval strategy

## 22.1 Phase 1

Implement immediately:

```text
LINKEDIN_MEMBER_CONSENTED
LINKEDIN_AUTHORIZED_IMPORT
LINKEDIN_OPERATOR_REFERENCE
legacy-data quarantine
```

These do not depend on unrestricted prospect search.

## 22.2 Phase 2

Apply for Community Management development access using a customer-owned organization analytics use case.

Required readiness:

- NEWAX legal organization details.
- Business-domain email.
- Verified NEWAX website.
- Privacy policy.
- LinkedIn Company Page.
- Page super-admin verification.
- Clear product screenshots or prototype.
- Explicit customer-authorization flow.
- Data-retention explanation.
- Deletion flow.
- Scope-minimization explanation.

## 22.3 Recommended application framing

Use:

> NEWAX Harvester enables organizations to connect and analyze their own LinkedIn Company Pages, preserve authorized business-activity evidence, measure organization and content performance, and connect those signals to customer-owned business infrastructure and operational intelligence.

Do not frame the application as:

- A LinkedIn scraper.
- A mass prospect harvester.
- A profile extraction service.
- A connection-automation tool.
- A message-automation tool.
- A CAPTCHA-resistant browser system.

## 22.4 Phase 3

After development-tier approval:

- Implement only approved endpoints.
- Validate rate limits.
- Run security review.
- Build customer authorization UI.
- Prepare standard-tier screencast.
- Apply for standard tier where required.

## 22.5 Sales Navigator

Monitor partner availability.

Do not delay Harvester core delivery waiting for Sales Navigator access.

---

# 23. Implementation sequence

## Gate 0: Freeze the legacy crawler

- Add an explicit disabled-by-default configuration gate.
- Remove production scheduling.
- Block CAPTCHA-solving integration.
- Block proxy-evasion configuration.
- Block production persistence from the legacy path.
- Prevent new feature work.

## Gate 1: Legacy data inventory

- Enumerate LinkedIn raw records.
- Trace derived institutions, people, findings, signals, briefs, and score effects.
- Quarantine unsupported records.
- Create remediation queues.

## Gate 2: Source-mode contracts

- Add source-mode enums.
- Add authorization, consent, and import objects.
- Add versioned LinkedIn connection policy.

## Gate 3: Member-consented flow

- Implement OAuth.
- Store minimal member fields.
- Support revocation and deletion.
- Verify tenant isolation.

## Gate 4: Authorized imports

- Add LinkedIn-specific declarations.
- Validate authorization and retention.
- Resolve imported people and organizations.

## Gate 5: Operator references

- Add bounded URL references.
- Add manual assertion provenance.
- Block automated fetching.

## Gate 6: Community Management application

- Prepare developer application.
- Verify legal and domain requirements.
- Submit use case.

## Gate 7: Authorized organization connector

- Implement approved scopes only.
- Add organization and analytics observations.
- Add rate-limit handling.
- Add token revocation.

## Gate 8: Scoring integration

- Map approved evidence into v3 subfactors.
- Prevent unsupported profile inferences from earning points.
- Recalculate legacy-affected scores.

## Gate 9: Legacy retirement

- Remove unreachable crawler commands.
- Remove account-farm scheduling.
- Remove stealth and CAPTCHA dependencies.
- Delete unsupported session cookies.
- Close legacy data remediation.

## Gate 10: Partner extensions

- Add Sales Navigator integration only after approval.
- Keep partner-specific data contracts isolated.

---

# 24. Verification scenarios

The LinkedIn source model is not complete until tests prove that:

1. Organization authorization requires an approved product and valid OAuth connection.
2. A member token cannot retrieve arbitrary third-party profiles.
3. Revoked organization authorization stops synchronization.
4. Revoked member consent stops processing and triggers deletion rules.
5. Organization and member tokens remain tenant-isolated.
6. Only approved scopes are requested.
7. Only approved fields are stored.
8. Community Management data is not used for general prospect search.
9. Sales Navigator mode remains disabled without partner approval.
10. Authorized imports require a source reference.
11. Authorized imports require a declared authorization basis.
12. Authorized imports require retention rules.
13. Operator references do not trigger automated page fetching.
14. Operator references remain distinct from provider facts.
15. The legacy crawler is disabled by default.
16. Production cannot start the legacy crawler.
17. Scheduled jobs cannot start the legacy crawler.
18. CAPTCHA solving is blocked.
19. Proxy-evasion configuration is blocked.
20. Fingerprint-spoofing execution is blocked.
21. Multi-account farming is blocked.
22. Automated LinkedIn messaging is blocked.
23. Automated connection requests are blocked.
24. Existing legacy records can be inventoried.
25. Existing legacy records can be quarantined.
26. Existing legacy-derived score contributions can be identified.
27. Quarantined records do not contribute to v3 scoring.
28. Independently verified facts create new evidence rather than relabeling legacy data.
29. Provider facts remain separate from AI inferences.
30. Role relevance does not automatically become procurement authority.
31. Seniority does not automatically become budget authority.
32. A profile headline does not create a pain point.
33. A job title does not create buying intent.
34. AI hypotheses record unsupported assumptions.
35. AI confidence is not fixed at one constant value.
36. Organization-authored posts remain claims requiring appropriate corroboration.
37. Follower count does not directly become account value.
38. Post reactions do not directly become buying intent.
39. LinkedIn identity does not grant communication consent.
40. Suppression applies to LinkedIn-related outreach channels.
41. Personal-data deletion propagates to derived findings.
42. Personal-data deletion propagates to score contributions.
43. Token secrets never appear in logs.
44. OAuth failures remain distinct from absence.
45. API rate limits create typed outcomes.
46. An unavailable API product does not fail the entire Harvester workflow.
47. Sales Navigator unavailability does not block core lead generation.
48. Legacy data replacement preserves lineage.
49. LinkedIn source mode appears in the Lead Dossier.
50. Users can see whether data is authorized, consented, imported, manual, or legacy.
51. Customer Page analytics remain customer-owned and tenant-isolated.
52. Exports respect LinkedIn source restrictions.
53. Source transitions request score recalculation.
54. API-version changes require connector review.
55. Provider-term changes can disable a source mode.
56. Exact-head CI and security checks pass without unresolved issues.

---

# 25. Acceptance criteria

The LinkedIn source model is production-ready only when:

- The five approved source modes are represented explicitly.
- The legacy crawler is represented separately as restricted.
- Production execution of the legacy crawler is blocked.
- Existing LinkedIn records are inventoried.
- Unsupported records are quarantined or deleted.
- Member-consented OAuth is implemented with revocation and deletion.
- Authorized imports require verifiable source declarations.
- Operator references remain manual and bounded.
- Community Management access has been approved before organization APIs are activated.
- Only approved API scopes and fields are used.
- Sales Navigator remains optional and disabled without approval.
- Provider facts, operator assertions, and AI inferences remain distinct.
- AI-generated pain and intent hypotheses cannot silently earn score points.
- Opportunity Scoring Model v3 uses only permitted, explainable evidence.
- Communication consent remains separate.
- Tenant isolation, security, privacy, retention, and deletion controls pass review.
- Provider-version and policy changes are monitored.
- Exact-head CI and security checks pass without unresolved issues.

---

# 26. Locked source definition

> NEWAX Harvester uses LinkedIn only through authorized organization connections, member consent, approved partner integrations, customer-authorized imports, and bounded operator references. The existing stealth crawler remains a quarantined legacy component for migration and audit continuity, not an approved interim production source. LinkedIn evidence may support organization activity, professional identity, role relevance, growth, and buying-timing hypotheses, but it cannot independently prove infrastructure absence, pain, budget, procurement authority, communication consent, or opportunity. Every LinkedIn-derived fact, assertion, and inference remains permission-aware, tenant-isolated, provenance-linked, revocable, deletable, and subordinate to Harvester's evidence and scoring controls.
