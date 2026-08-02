# NEWAX Harvester Opportunity Scoring Model v3

Status: **Normative planned architecture**  
Model family: **Opportunity intelligence**  
Model version: **v3**  
Implementation state: **Not yet implemented**  
Authority: This document defines the required opportunity-scoring behavior for the existing Harvester roadmap. It does not create a separate product roadmap or claim that the current runtime already follows v3.

Read with:

- [Harvester Standalone Product Roadmap](../ROADMAP.md)
- [Harvester Intelligence Operating Model](harvester-intelligence-operating-model.md)
- [Standalone Product and Integration Framework](standalone-product-and-integration-framework.md)

---

## 1. Purpose

Harvester exists to identify evidence-backed business-infrastructure opportunities, not merely organizations with complete contact records.

The Opportunity Scoring Model v3 evaluates:

1. Whether an organization is eligible to pursue.
2. Which required business-infrastructure capabilities are absent, weak, fragmented, limited, or strong.
3. How strategically relevant and commercially valuable the organization is.
4. Whether there is evidence of buying intent or useful timing.
5. Whether NEWAX can reach the right decision-makers.
6. How complete, current, corroborated, and trustworthy the supporting evidence is.
7. Whether identity resolution is sufficiently reliable.
8. What action should happen next.

The score must help an operator answer:

> Is this a meaningful NEWAX opportunity, why does it matter, how confident are we, and what should we do next?

It must not reduce that decision to record completeness, website presence, signal count, or one unexplained percentage.

---

## 2. Locked business principle

The strongest infrastructure-need signal is normally:

```text
Required business infrastructure is completely absent.
```

The second strongest is:

```text
Required infrastructure exists but is severely weak, unreliable, unsuitable, or outside the organization's control.
```

The full hierarchy is:

```text
1. Required infrastructure absent
2. Infrastructure severely weak
3. Infrastructure fragmented or disconnected
4. Infrastructure functional but limited
5. Infrastructure effective with minor gaps
6. Infrastructure strong, integrated, reliable, and appropriately controlled
```

However, absence is not automatically the strongest commercial opportunity.

The final opportunity depends on:

```text
Infrastructure gap severity
× business relevance
× organizational value
× strategic fit
× buying readiness
× pursuit readiness
× evidence confidence
```

A small organization missing every system may still be a lower-value opportunity than a large multi-location organization whose existing systems are failing across critical operations.

---

## 3. Non-negotiable scoring rules

### 3.1 Required absence is not the same as non-detection

Harvester must distinguish:

```text
PRESENT
ABSENT_CONFIRMED
NOT_DETECTED
NOT_INSPECTED
INSPECTION_FAILED
UNKNOWN
NOT_APPLICABLE
```

Only `ABSENT_CONFIRMED` may receive full absence credit.

The following must never be treated as confirmed absence:

- A connector was not run.
- A website could not be crawled.
- A page was blocked.
- A source returned incomplete data.
- A public website did not mention an internal system.
- A model failed to extract a capability.
- A source was stale.
- Evidence was contradictory.

`NOT_DETECTED`, `NOT_INSPECTED`, `INSPECTION_FAILED`, and `UNKNOWN` reduce coverage or confidence. They do not prove an opportunity.

### 3.2 A capability must be relevant before its absence matters

No website may be a critical gap for a customer-facing hospital, school, hotel, retailer, or professional-services firm.

No public website may be irrelevant for a dormant holding entity or a private special-purpose vehicle.

No connected telemetry may be a critical gap for a multi-site healthcare facility, industrial property portfolio, or hospitality operation.

No connected telemetry may be irrelevant for a small legal office.

Therefore:

```text
Gap contribution = condition severity × capability relevance × business impact
```

### 3.3 Unknown is not zero

```text
0 = evidence supports no meaningful opportunity in this subfactor
Unknown = Harvester lacks enough evidence to evaluate the subfactor
```

Unknown values lower coverage and may require research. They must not silently become negative evidence.

### 3.4 Qualification and compliance are gates, not bonus points

A prohibited, suppressed, permanently closed, duplicate, or otherwise blocked record must not remain competitive merely because it earned points elsewhere.

### 3.5 Opportunity, readiness, confidence, and risk remain separate

A high-value opportunity may have low pursuit readiness.

A highly reachable organization may have little infrastructure need.

A high score may still carry high risk.

A low-confidence assessment may still describe a potentially valuable lead that needs research.

### 3.6 Every material point must be explainable

Every awarded or withheld point must identify:

- Subfactor
- Grade
- Weight
- Earned points
- Evidence references
- Evidence state
- Confidence
- Freshness
- Positive drivers
- Negative drivers
- Unknowns
- Contradictions
- Model and policy version

---

## 4. Decision architecture

The v3 model uses six layers.

```text
Layer 0  Eligibility gates
Layer 1  Infrastructure capability assessment
Layer 2  Opportunity Value Score
Layer 3  Pursuit Readiness Score
Layer 4  Coverage and confidence
Layer 5  Pursuit risk and recommended action
```

The final 100-point score is composed of:

```text
Opportunity Value       75 points
Pursuit Readiness       25 points
Total                  100 points
```

Coverage, confidence, risk, and eligibility remain separate outputs.

---

# 5. Layer 0: Eligibility gates

## 5.1 Gate outcomes

```text
ELIGIBLE
REVIEW_REQUIRED
BLOCKED
```

## 5.2 Blocking conditions

A policy may block pursuit when any applicable condition is confirmed:

- Permanently closed organization
- Suppression or deletion request
- Prohibited industry or business activity
- Prohibited source or collection method
- Unauthorized use of personal information
- Tenant restriction
- Market-definition exclusion
- Geographic exclusion
- Duplicate or superseded entity
- Confirmed fraudulent or invalid entity
- Legal or compliance prohibition
- Customer-configured exclusion
- Publication restriction that prevents the intended use

## 5.3 Review-required conditions

Review may be required for:

- Conflicting identity evidence
- Ambiguous organization resolution
- Uncertain operating status
- Sensitive sector or data category
- Weak source authority
- High-value but low-confidence opportunity
- High pursuit risk
- Possible suppression conflict
- Unverified decision-maker attribution
- Material model disagreement
- Operator override request

## 5.4 Gate behavior

- Gates never award points.
- A blocked organization receives no pursuit recommendation other than `DO_NOT_PURSUE`.
- A review-required organization may retain its score for analysis, but automation must not publish or activate it until approved.
- Gate decisions are versioned and auditable.
- A score cannot override a gate.

---

# 6. Layer 1: Infrastructure capability assessment

## 6.1 Capability families

Harvester evaluates only capabilities relevant to the selected market definition, sector policy, organization type, and business objective.

Recommended capability families:

### Digital access and service delivery

- Public website
- Customer, patient, student, tenant, member, or partner portal
- Booking, appointment, admission, application, ordering, or service-request interface
- Mobile or responsive access
- Digital forms and self-service

### Enterprise software

- Core operating system
- CRM or relationship management
- ERP or resource management
- LMS or academic operations
- Practice, case, property, hospitality, retail, finance, or sector-specific system
- Document and records management
- Identity and access management

### Intelligent automation

- Workflow automation
- Approval automation
- Notifications and escalation
- Data-entry reduction
- Scheduling and routing
- Decision support
- AI-assisted processing where appropriate

### Data and operational intelligence

- Central data ownership
- Reliable reporting
- Dashboards
- Forecasting
- Auditability
- Cross-branch visibility
- Data-quality controls

### Integration infrastructure

- API or event integration
- Shared identifiers
- System-to-system synchronization
- Duplicate prevention
- Cross-department data flow
- Partner and customer integration

### Connected infrastructure

- Equipment monitoring
- Facility telemetry
- Environmental monitoring
- Energy or utility visibility
- Asset tracking
- Safety or condition alerts
- Real-time operational intelligence

### Reliability, security, and ownership

- Availability and continuity
- Backup and recovery
- Security controls
- Access governance
- Vendor dependency
- Data portability
- Infrastructure ownership
- Supportability and maintainability

## 6.2 Capability condition scale

Each applicable capability receives one condition.

| Grade | Condition | Meaning |
|---:|---|---|
| 5 | `ABSENT_CONFIRMED` | A required capability is confirmed not to exist |
| 4 | `SEVERELY_WEAK` | Present but failing, unreliable, insecure, unusable, or unsuitable |
| 3 | `FRAGMENTED` | Capability exists across disconnected tools, teams, or locations |
| 2 | `LIMITED` | Functional but inefficient, incomplete, hard to scale, or overly manual |
| 1 | `EFFECTIVE_WITH_MINOR_GAPS` | Generally effective with bounded improvement potential |
| 0 | `STRONG` | Integrated, reliable, scalable, secure, visible, and appropriately controlled |
| Unknown | `UNKNOWN` | Insufficient evidence |
| Unknown | `NOT_DETECTED` | No evidence found, but absence is not confirmed |
| Unknown | `NOT_INSPECTED` | Capability has not been evaluated |
| Unknown | `INSPECTION_FAILED` | Evaluation could not be completed |
| Excluded | `NOT_APPLICABLE` | Capability is not relevant to this organization or objective |

## 6.3 Capability relevance

Each capability receives a relevance grade:

| Grade | Relevance |
|---:|---|
| 0 | Not relevant |
| 1 | Low relevance |
| 2 | Useful but nonessential |
| 3 | Important |
| 4 | Highly important |
| 5 | Mission-critical |

A confirmed absence with relevance `0` contributes no opportunity.

## 6.4 Business-impact grade

Each confirmed gap receives an impact grade:

| Grade | Impact |
|---:|---|
| 0 | No demonstrated impact |
| 1 | Minor inconvenience |
| 2 | Recurring inefficiency |
| 3 | Material cost, delay, or service friction |
| 4 | Serious operational, revenue, compliance, or customer impact |
| 5 | Mission-critical disruption or material organizational risk |

## 6.5 Capability assessment record

Every capability assessment should retain:

```text
capability_key
capability_family
condition
condition_grade
relevance_grade
impact_grade
scope
affected_locations
affected_departments
business_processes
evidence_assertion_ids
contradicting_assertion_ids
coverage_state
confidence_dimensions
first_observed_at
last_observed_at
policy_version
model_version
assessment_method
operator_review_state
```

## 6.6 Infrastructure opportunity classes

### Class A: Greenfield infrastructure opportunity

Required infrastructure is absent.

Typical characteristics:

- No meaningful operational system
- No customer or staff portal
- No workflow automation
- No central reporting
- No integrated data foundation
- No relevant monitoring or telemetry

### Class B: Replacement and modernization opportunity

Infrastructure exists but is weak, fragile, outdated, insecure, unsupported, or unfit.

Typical characteristics:

- Frequent downtime
- Poor usability
- Weak security
- Vendor abandonment
- No ownership or portability
- Inability to support current scale
- Repeated manual correction

### Class C: Integration opportunity

Multiple systems exist but do not work together.

Typical characteristics:

- Duplicate records
- Manual data transfer
- Departmental silos
- Separate branch systems
- No shared identity
- No consolidated reporting
- Reconciliation work

### Class D: Optimization opportunity

Infrastructure works but needs better automation, visibility, efficiency, control, or scalability.

### Class E: Low-gap account

Infrastructure is strong, integrated, reliable, secure, scalable, visible, and appropriately controlled.

---

# 7. Layer 2: Opportunity Value Score

Opportunity Value answers:

> How valuable and relevant is this opportunity to NEWAX?

Maximum: **75 points**

| Dimension | Weight |
|---|---:|
| Operational need and infrastructure gaps | 30 |
| Strategic and ICP fit | 15 |
| Account value and scale | 15 |
| Buying intent and timing | 15 |
| **Total** | **75** |

---

## 7.1 Operational need and infrastructure gaps: 30 points

This is the largest dimension because NEWAX removes operational complexity by building dependable business infrastructure.

| Subfactor | Weight |
|---|---:|
| Required infrastructure completely absent | 10 |
| Existing infrastructure weakness | 6 |
| Manual work and process dependence | 4 |
| Fragmentation and integration gaps | 4 |
| Visibility and reporting gaps | 2 |
| Reliability, ownership, and control gaps | 2 |
| Demonstrated business impact | 2 |
| **Total** | **30** |

### 7.1.1 Required infrastructure completely absent: 10 points

This subfactor measures confirmed absence of capabilities that are relevant to the organization.

Suggested interpretation:

| Grade | Condition |
|---:|---|
| 0 | No relevant confirmed absence |
| 1 | One low-relevance capability absent |
| 2 | One useful but nonessential capability absent |
| 3 | One important capability absent |
| 4 | Multiple important capabilities absent |
| 5 | One or more mission-critical capabilities absent |

Rules:

- Use only confirmed absence.
- Evaluate capability relevance before scoring.
- Deduplicate overlapping gaps.
- Do not count the same missing capability once per source.
- Do not award full absence points from public non-detection of internal software.

### 7.1.2 Existing infrastructure weakness: 6 points

Signals include:

- Frequent outage or failure
- Poor performance
- Weak security
- Unsupported software
- Inaccessible or unusable interfaces
- Incomplete workflows
- High error rates
- No backup or recovery
- Vendor lock-in without portability
- Excessive maintenance burden
- Infrastructure unsuitable for current scale

| Grade | Condition |
|---:|---|
| 0 | Strong and dependable |
| 1 | Minor limitations |
| 2 | Noticeable inefficiency |
| 3 | Weak in several important areas |
| 4 | Severe weakness or unreliability |
| 5 | Business-critical infrastructure is failing |

### 7.1.3 Manual work and process dependence: 4 points

| Grade | Condition |
|---:|---|
| 0 | Core processes are appropriately automated |
| 1 | Some avoidable manual work |
| 2 | Important workflows depend on spreadsheets, messages, or re-entry |
| 3 | Multiple departments depend on manual processes |
| 4 | Core operations are predominantly manual |
| 5 | Manual dependence creates mission-critical delay, error, or risk |

### 7.1.4 Fragmentation and integration gaps: 4 points

| Grade | Condition |
|---:|---|
| 0 | Systems are appropriately integrated |
| 1 | Minor disconnected workflows |
| 2 | Several duplicate or disconnected systems |
| 3 | Major departments or branches operate in silos |
| 4 | No coherent operating infrastructure |
| 5 | Fragmentation materially threatens continuity, compliance, or service delivery |

### 7.1.5 Visibility and reporting gaps: 2 points

| Grade | Condition |
|---:|---|
| 0 | Reliable, timely operational visibility |
| 1 | Minor reporting limitations |
| 2 | Delayed or incomplete reporting |
| 3 | Important decisions rely on manual compilation |
| 4 | No dependable cross-functional visibility |
| 5 | Lack of visibility creates material operational or governance risk |

### 7.1.6 Reliability, ownership, and control gaps: 2 points

This subfactor evaluates business outcomes, not abstract ideology.

Signals include:

- Organization cannot access or export its data
- Critical systems depend on one fragile vendor
- No clear recovery ownership
- No contractual portability
- No reliable support path
- No internal visibility into system state
- Critical processes depend on credentials or infrastructure outside organizational control

| Grade | Condition |
|---:|---|
| 0 | Dependable systems with appropriate ownership and control |
| 1 | Minor dependency concerns |
| 2 | Material portability, support, or control limitations |
| 3 | High vendor or operational dependency |
| 4 | Critical data or operations are outside effective control |
| 5 | Dependency creates immediate continuity, security, or governance risk |

### 7.1.7 Demonstrated business impact: 2 points

| Grade | Condition |
|---:|---|
| 0 | No demonstrated impact |
| 1 | Minor inconvenience |
| 2 | Recurring cost, delay, or service friction |
| 3 | Material inefficiency or lost opportunity |
| 4 | Serious revenue, compliance, customer, or operational impact |
| 5 | Mission-critical disruption or material risk |

### 7.1.8 Operational-need explanation

The assessment must identify:

- Strongest confirmed gap
- Most relevant affected capability
- Business process affected
- Severity and impact
- Evidence coverage
- Contradictions
- NEWAX capability alignment
- Suggested next research action

---

## 7.2 Strategic and ICP fit: 15 points

This dimension evaluates whether the organization fits the selected market and NEWAX strategy.

| Subfactor | Weight |
|---|---:|
| Sector priority | 3 |
| Organization-type fit | 3 |
| Geography and serviceability | 2 |
| Primary NEWAX capability alignment | 3 |
| Cross-capability expansion potential | 2 |
| Strategic account value | 2 |
| **Total** | **15** |

### 7.2.1 Sector priority: 3 points

Sector priority comes from the active market definition or approved sector policy.

It must not be inferred merely because a sector is known.

### 7.2.2 Organization-type fit: 3 points

Examples:

- Hospital group rather than unrelated medical listing
- Multi-campus institution rather than an individual tutor
- Property operator rather than a one-time property listing
- Law firm rather than an individual directory entry

### 7.2.3 Geography and serviceability: 2 points

Consider:

- Delivery region
- Language
- Regulatory constraints
- Support model
- On-site requirements
- Time zone
- Partner coverage

### 7.2.4 Primary NEWAX capability alignment: 3 points

The opportunity must map to one or more capabilities:

```text
Enterprise Software
Intelligent Automation
Connected Infrastructure
```

### 7.2.5 Cross-capability expansion potential: 2 points

Examples:

- Enterprise software plus workflow automation
- Customer portal plus CRM integration
- Facility monitoring plus operational dashboards
- Core system plus long-term support and integration

### 7.2.6 Strategic account value: 2 points

Signals may include:

- Reference value
- Group ownership
- Network influence
- Multi-entity rollout
- Partnership value
- Sector credibility
- Repeatable use case

### 7.2.7 Strategic-fit prohibition

A known organization type must not automatically receive full strategic-fit points.

Classification completeness and strategic fit are different facts.

---

## 7.3 Account value and scale: 15 points

This dimension evaluates the potential economic and operational value of the account.

| Subfactor | Weight |
|---|---:|
| Sector-specific size proxy | 5 |
| Operating footprint | 3 |
| Operational complexity | 4 |
| Expansion and lifetime value | 3 |
| **Total** | **15** |

### 7.3.1 Sector-specific size proxy: 5 points

Scale must use the best available sector-relevant measures.

| Sector | Preferred scale signals |
|---|---|
| Healthcare | Beds, facilities, departments, doctors, patient volume |
| Education | Campuses, enrolment, faculty, programmes |
| Real estate | Properties, projects, agents, locations, units managed |
| Hospitality | Rooms, venues, locations, bookings |
| Retail | Stores, SKUs, warehouses, transaction volume |
| Legal | Lawyers, offices, practice areas, active matters |
| Islamic finance | Customers, branches, products, transaction volume |
| Professional services | Employees, offices, clients, recurring engagements |

When preferred measures are unavailable, branch and contact counts may be used as an explicit low-confidence fallback.

### 7.3.2 Operating footprint: 3 points

Consider:

- Locations
- Branches
- Facilities
- Service regions
- Customer reach
- Physical assets

### 7.3.3 Operational complexity: 4 points

Consider:

- Number of departments
- Number of workflows
- Number of users
- Number of systems
- Approval depth
- Data dependencies
- Regulatory obligations
- Cross-location coordination

### 7.3.4 Expansion and lifetime value: 3 points

Consider:

- Multi-phase implementation
- Rollout potential
- Recurring support
- Integration expansion
- Additional capability adoption
- Additional entities or locations
- Long-term infrastructure ownership

### 7.3.5 Scale confidence

Every size assessment must state whether it is based on:

```text
DIRECT_MEASURE
CORROBORATED_ESTIMATE
SINGLE_SOURCE_ESTIMATE
PROXY
UNKNOWN
```

---

## 7.4 Buying intent and timing: 15 points

This dimension evaluates why NEWAX should act now.

| Subfactor | Weight |
|---|---:|
| Trigger-event strength | 4 |
| Active initiative or procurement evidence | 4 |
| Urgency and deadline | 3 |
| Budget and authority readiness | 2 |
| Signal freshness and momentum | 2 |
| **Total** | **15** |

### 7.4.1 Trigger-event strength: 4 points

Examples:

- New branch or facility
- Expansion
- Hiring wave
- Funding
- Regulatory requirement
- Leadership change
- Merger or acquisition
- New service line
- Public failure or outage
- Contract expiry
- Digital service launch

### 7.4.2 Active initiative or procurement evidence: 4 points

Examples:

- Tender
- Request for proposal
- Vendor search
- Job postings tied to implementation
- Announced system initiative
- Implementation partner request
- Budget approval
- Published modernization programme

### 7.4.3 Urgency and deadline: 3 points

A time-bound requirement is stronger than a general aspiration.

The evaluator must retain the actual deadline where available.

### 7.4.4 Budget and authority readiness: 2 points

Evidence may include:

- Approved budget
- Procurement activity
- Decision-maker involvement
- Active project team
- Prior related purchase
- Public allocation

Lack of public budget evidence is normally unknown, not zero.

### 7.4.5 Signal freshness and momentum: 2 points

Freshness should decay gradually.

Default bands:

| Age | Default strength |
|---|---|
| 0 to 30 days | Full |
| 31 to 90 days | Moderate |
| 91 to 180 days | Weak |
| More than 180 days | Historical |

Signal-specific policies may override these bands.

Examples:

- Tender deadlines decay rapidly.
- A new facility may remain relevant for months.
- A leadership change may remain useful longer than a short-term hiring post.

Momentum should consider repeated independent signals without double-counting duplicates.

---

# 8. Layer 3: Pursuit Readiness Score

Pursuit Readiness answers:

> Can NEWAX pursue this opportunity intelligently and responsibly now?

Maximum: **25 points**

| Dimension | Weight |
|---|---:|
| Contactability and decision-maker access | 10 |
| Evidence quality and freshness | 10 |
| Identity confidence | 5 |
| **Total** | **25** |

---

## 8.1 Contactability and decision-maker access: 10 points

| Subfactor | Weight |
|---|---:|
| Verified primary contact channel | 3 |
| Named relevant decision-maker | 3 |
| Role authority and relevance | 2 |
| Multiple entry paths | 1 |
| Relationship or response evidence | 1 |
| **Total** | **10** |

### 8.1.1 Verified primary contact channel: 3 points

A contact method should distinguish:

```text
PRESENT
FORMAT_VALID
DELIVERABILITY_VERIFIED
RECENTLY_CONFIRMED
SUPPRESSED
BOUNCED
INVALID
UNKNOWN
```

A syntactically valid email is not the same as a verified usable channel.

### 8.1.2 Named relevant decision-maker: 3 points

A person receives credit only when linked to:

- The correct organization
- A relevant role
- Evidence supporting the attribution
- A usable contact or access path where required

### 8.1.3 Role authority and relevance: 2 points

Examples of role relevance vary by opportunity:

- Operations leadership
- Technology leadership
- Finance or procurement
- Facility management
- Academic administration
- Practice management
- Customer experience
- Executive sponsor

A named receptionist and a named chief operating officer must not receive equal authority credit.

### 8.1.4 Multiple entry paths: 1 point

Examples:

- Verified email plus phone
- Executive plus operational stakeholder
- Referral plus direct contact
- Headquarters plus branch contact

### 8.1.5 Relationship or response evidence: 1 point

Examples:

- Referral
- Prior response
- Existing customer relationship
- Partner introduction
- Previous meeting
- Approved engagement history

Communication consent remains a separate Communicator responsibility and cannot be inferred from this score.

---

## 8.2 Evidence quality and freshness: 10 points

| Subfactor | Weight |
|---|---:|
| Source authority | 2 |
| Cross-source corroboration | 2 |
| Coverage completeness | 2 |
| Evidence freshness | 2 |
| Provenance completeness | 1 |
| Contradiction status | 1 |
| **Total** | **10** |

### 8.2.1 Source authority: 2 points

Examples of stronger authority may include:

- Organization-owned website
- Official registry
- Government or regulator record
- Authorized customer dataset
- Direct operator confirmation

Source authority is claim-specific. An official website may be authoritative for an address but not for an unreported internal workflow.

### 8.2.2 Cross-source corroboration: 2 points

Independent sources may strengthen a claim.

Rules:

- Mirrors and copied directories are not independent corroboration.
- Multiple pages from the same source are not automatically independent.
- Repeated model outputs from the same evidence are not corroboration.
- Contradictory sources must remain visible.

### 8.2.3 Coverage completeness: 2 points

Coverage asks whether Harvester actually inspected the sources and capability areas required to support the conclusion.

Coverage must consider:

- Planned sources
- Completed sources
- Failed sources
- Skipped sources
- Restricted sources
- Relevant pages or records inspected
- Relevant capability areas evaluated

### 8.2.4 Evidence freshness: 2 points

Freshness is evaluated according to the claim's useful life.

Examples:

- Contact details may decay quickly.
- Legal identity may be stable.
- Current software may change over months.
- Tender timing may change within days.

### 8.2.5 Provenance completeness: 1 point

Every material claim should trace to:

```text
Opportunity conclusion
→ subfactor result
→ evidence assertion
→ evidence artifact
→ raw observation
→ source
```

### 8.2.6 Contradiction status: 1 point

The evaluator must distinguish:

```text
NO_CONTRADICTION
MINOR_CONTRADICTION
MATERIAL_CONTRADICTION
UNRESOLVED_CONTRADICTION
```

A contradiction is not erased by choosing the most convenient source.

---

## 8.3 Identity confidence: 5 points

| Subfactor | Weight |
|---|---:|
| Organization identity certainty | 2 |
| Branch and location attribution | 1 |
| Person-role attribution | 1 |
| Domain and contact ownership | 1 |
| **Total** | **5** |

### 8.3.1 Organization identity certainty: 2 points

Consider:

- Stable provider or registry identifier
- Name agreement
- Domain agreement
- Phone agreement
- Address agreement
- Geographic agreement
- Legal identity agreement

### 8.3.2 Branch and location attribution: 1 point

A branch must be linked to the correct parent organization.

### 8.3.3 Person-role attribution: 1 point

A person must be linked to the correct organization and current role.

### 8.3.4 Domain and contact ownership: 1 point

Contact methods and domains must belong to the correct entity rather than a directory, agency, former employee, franchise, or unrelated organization.

---

# 9. Standard subfactor rubric

Unless a versioned policy defines a more specific rubric, scored subfactors use a common five-grade scale.

| Grade | Meaning |
|---:|---|
| 0 | Strong negative evidence or no meaningful opportunity |
| 1 | Very weak |
| 2 | Limited |
| 3 | Adequate |
| 4 | Strong |
| 5 | Exceptional or critical |
| Unknown | Insufficient evidence |

Weighted points:

```text
earned_points = subfactor_weight × grade ÷ 5
```

Example:

```text
Operational pain severity
Weight = 6
Grade = 4
Earned points = 6 × 4 ÷ 5 = 4.8
```

Rules:

- Store unrounded points internally.
- Round only for display according to the versioned policy.
- Preserve the original grade and evidence.
- Unknown subfactors do not receive zero.
- Not-applicable subfactors are excluded from the applicable-weight denominator.
- Operator overrides require rationale and audit history.

---

# 10. Score calculation

## 10.1 Dimension score

```text
dimension_score = sum(earned points for applicable evaluated subfactors)
```

## 10.2 Opportunity Value Score

```text
operational need and infrastructure gaps  30
strategic and ICP fit                     15
account value and scale                   15
buying intent and timing                  15
                                           --
opportunity value                         75
```

## 10.3 Pursuit Readiness Score

```text
contactability and decision-maker access  10
evidence quality and freshness            10
identity confidence                        5
                                           --
pursuit readiness                         25
```

## 10.4 Opportunity Priority Score

```text
opportunity priority score = opportunity value + pursuit readiness
```

Maximum: **100**

## 10.5 Score normalization with not-applicable factors

Not-applicable subfactors should not unfairly reduce a score.

For a dimension with excluded subfactors:

```text
normalized_dimension_score =
raw_earned_points ÷ applicable_weight × published_dimension_weight
```

Unknown factors remain applicable but unevaluated. They affect coverage rather than being removed from the denominator.

## 10.6 No hidden multiplication by confidence

The displayed opportunity score must not be silently multiplied by confidence or coverage.

Instead, Harvester displays:

```text
Opportunity Priority Score
Coverage
Confidence
Risk
Eligibility
```

Decision rules use all five outputs.

---

# 11. Coverage model

Coverage measures how much of the applicable model was actually evaluated.

```text
coverage = evaluated applicable weight ÷ total applicable weight × 100
```

An evaluated subfactor must have sufficient evidence to produce a grade other than unknown.

Recommended bands:

| Coverage | Band |
|---:|---|
| 85 to 100% | High |
| 65 to 84% | Moderate |
| 40 to 64% | Low |
| Below 40% | Insufficient |

Coverage must also be available per dimension.

Example:

```text
Opportunity Priority Score: 84/100
Overall Coverage: 72%
Operational Need Coverage: 90%
Buying Intent Coverage: 35%
Decision-Maker Coverage: 60%
```

A high score with low coverage should normally produce a research action, not automatic pursuit.

---

# 12. Confidence model

Confidence remains multidimensional.

Recommended dimensions:

- Source authority
- Source reliability
- Extraction certainty
- Corroboration
- Freshness
- Coverage
- Identity certainty
- Policy fit certainty
- Opportunity inference certainty

Harvester may calculate a composite display band, but it must preserve each component.

Recommended display bands:

```text
HIGH
MEDIUM
LOW
INSUFFICIENT
```

A composite confidence band must be versioned and explainable.

---

# 13. Pursuit risk

Risk must not be hidden inside the opportunity score.

```text
LOW
MEDIUM
HIGH
BLOCKED
```

Risk factors may include:

- Compliance sensitivity
- Procurement complexity
- Payment or credit concern
- Delivery complexity
- Data sensitivity
- Integration uncertainty
- Reputational exposure
- Political exposure
- Unclear ownership
- Weak evidence
- High research cost
- High customization burden
- Unrealistic timeline
- Customer dependency risk

A high-value, high-risk opportunity remains visible but requires review.

A blocked risk condition invokes the eligibility gate.

---

# 14. Recommended-action matrix

| Opportunity value | Pursuit readiness | Typical action |
|---|---|---|
| High | High | `PURSUE_NOW` |
| High | Low | `RESEARCH_AND_ENRICH` |
| Medium | High | `TARGETED_OUTREACH` or `NURTURE` |
| Medium | Low | `MONITOR` |
| Low | High | `LOW_PRIORITY_POOL` |
| Low | Low | `DEPRIORITIZE` |
| Any | Blocked | `DO_NOT_PURSUE` |

Recommended action must also consider:

- Eligibility
- Coverage
- Confidence
- Risk
- Customer policy
- Capacity
- Reservation state
- Publication approval

Suggested action thresholds must be calibrated with real outcomes before production activation.

---

# 15. Opportunity explanation contract

Every assessment should produce a human-readable explanation.

Minimum output:

```text
Opportunity Priority Score
Opportunity Value
Pursuit Readiness
Eligibility
Coverage
Confidence
Risk
Recommended Action
Strongest Drivers
Weakest Areas
Unknowns
Contradictions
Infrastructure Opportunity Class
Primary NEWAX Capability Alignment
Required Next Evidence
Model Version
Policy Version
Evaluated At
```

Example:

```text
Opportunity Priority Score: 82/100
Opportunity Value: 66/75
Pursuit Readiness: 16/25
Eligibility: ELIGIBLE
Coverage: 81%
Confidence: HIGH
Risk: MEDIUM
Infrastructure Opportunity Class: INTEGRATION

Recommended action:
Pursue after confirming procurement authority.

Strongest drivers:
- High-value multi-location organization
- Severe manual workflow fragmentation
- Active expansion signal
- Strong fit for Enterprise Software and Intelligent Automation

Weakest areas:
- Decision-maker authority not confirmed
- Connected Infrastructure evidence incomplete

Unknowns:
- Approved budget

Contradictions:
- One source reports an LMS, while the organization website provides no portal evidence
```

---

# 16. Required domain objects

Recommended planned objects:

## 16.1 `OpportunityModelVersion`

```text
id
name
version
status
weights
rubrics
thresholds
confidence_policy
coverage_policy
risk_policy
created_by
approved_by
activated_at
retired_at
rollback_version_id
created_at
```

## 16.2 `OpportunityAssessment`

```text
id
institution_id
market_definition_id
model_version_id
policy_version_id
eligibility_status
opportunity_value_score
pursuit_readiness_score
opportunity_priority_score
overall_coverage
confidence_band
risk_band
recommended_action
infrastructure_opportunity_class
primary_capability_alignment
summary
assessed_at
supersedes_assessment_id
```

## 16.3 `OpportunityDimensionResult`

```text
id
assessment_id
dimension_key
published_weight
applicable_weight
earned_points
normalized_points
coverage
confidence
summary
```

## 16.4 `OpportunitySubfactorResult`

```text
id
dimension_result_id
subfactor_key
weight
applicability
grade
earned_points
evidence_state
confidence
rationale
positive_drivers
negative_drivers
unknowns
contradictions
freshness
assessment_method
operator_override
```

## 16.5 `InfrastructureCapabilityAssessment`

```text
id
assessment_id
capability_key
capability_family
condition
condition_grade
relevance_grade
impact_grade
scope
coverage_state
confidence
first_observed_at
last_observed_at
```

## 16.6 Evidence links

Material results should link to evidence assertions through a join object rather than embedding unverifiable prose.

```text
OpportunityResultEvidence

result_type
result_id
evidence_assertion_id
relationship
support_strength
```

Relationships may include:

```text
SUPPORTS
CONTRADICTS
QUALIFIES
SUPERSEDES
```

---

# 17. Current-to-v3 migration map

The current live `overall_score` should not be deleted before v3 is evaluated in shadow mode.

Recommended mapping:

| Current component | v3 destination |
|---|---|
| Scale | Account value and scale |
| Contactability | Contactability and decision-maker access |
| Category fit | Strategic and ICP fit, after replacing known-type logic |
| Qualification points | Eligibility gate, not points |
| Research signals | Split between infrastructure need and buying intent |
| Freshness | Split between evidence freshness and buying momentum |
| Confidence | Identity confidence plus evidence confidence |
| `size_tier` | Fallback input to account value |
| `operational_maturity_score` | Input evidence for infrastructure weakness, not a direct inverse score |
| `icp_match_score` | Input to strategic and ICP fit |
| `website_quality_tier` | One capability input within digital access |
| `service_gap_score` | Replaced by capability-level infrastructure assessments |

## 17.1 Legacy preservation

During migration, retain:

```text
legacy_overall_score
legacy_score_breakdown
v3_opportunity_priority_score
v3_opportunity_value_score
v3_pursuit_readiness_score
v3_coverage
v3_confidence
v3_risk
v3_model_version
```

This supports comparison, calibration, rollback, and audit.

---

# 18. Calibration and learning

The model must not be declared accurate merely because its weights sum to 100.

Calibration requires outcome evidence such as:

- Accepted for research
- Rejected after review
- Contact established
- Decision-maker reached
- Meeting booked
- Qualified opportunity created
- Proposal requested
- Proposal submitted
- Won
- Lost
- No response
- Bad fit
- Wrong timing
- Insufficient budget
- Duplicate
- Compliance block

## 18.1 Evaluation metrics

Recommended metrics:

- Precision among top-ranked leads
- Recall of known valuable opportunities
- Conversion by score band
- Meeting rate by action recommendation
- Win rate by infrastructure opportunity class
- Calibration error
- Sector-level performance
- Geography-level performance
- False confirmed-absence rate
- False identity-link rate
- Human override rate
- Contradiction rate
- Coverage distribution
- Cost per accepted opportunity
- Operator minutes per accepted opportunity

## 18.2 Controlled model changes

Model changes require:

```text
Proposed version
→ offline evaluation
→ bias and sector review
→ operator review
→ approval
→ shadow mode
→ staged activation
→ monitoring
→ rollback capability
```

Production weights, thresholds, and rubrics must not self-modify from outcomes.

---

# 19. Anti-gaming and integrity controls

The model must prevent artificial score inflation.

Rules:

1. Duplicate signals do not create additional independent evidence.
2. Copied directories do not count as independent corroboration.
3. One capability cannot be counted repeatedly under overlapping labels.
4. A failed inspection cannot become confirmed absence.
5. More contact records do not automatically mean more decision-maker access.
6. More branches do not automatically mean stronger strategic fit.
7. A known category does not automatically mean ICP fit.
8. A recent low-value signal does not erase stale critical evidence.
9. A score does not grant communication consent.
10. A high score does not bypass eligibility or risk review.
11. Operator overrides are explicit, reasoned, and audited.
12. Model-generated text cannot serve as its own evidence.
13. Source and model versions remain attached to every assessment.
14. Contradictions remain visible until resolved or explicitly accepted.
15. Evidence deletion or correction creates a new assessment rather than silently rewriting history.

---

# 20. Sector policy requirements

A global model provides common structure. Sector policies define relevance, scale, capability, and threshold details.

Each sector policy may define:

```text
priority
allowed organization types
excluded organization types
serviceable geographies
applicable capabilities
mission-critical capabilities
scale measures
scale fallback proxies
common pain patterns
business-impact rules
buying triggers
relevant decision-maker roles
freshness windows
risk rules
minimum evidence coverage
action thresholds
```

Sector policy must not change the locked 100-point published dimension weights without creating a new approved model version.

It may redistribute weights among subfactors within a dimension where the model version explicitly permits it.

---

# 21. Worked examples

## 21.1 Multi-campus school with absent infrastructure

Observed evidence:

- Five campuses
- No confirmed LMS
- Admissions handled through forms and messaging
- No parent portal
- Branch reporting compiled manually
- Active expansion announcement
- Named operations director
- Official website and registry corroborate identity

Expected interpretation:

```text
Infrastructure class: GREENFIELD
Operational need: Very high
Strategic fit: High
Account value: High
Buying intent: High
Pursuit readiness: High
Coverage: High
Recommended action: PURSUE_NOW
```

## 21.2 Large hospital with weak fragmented systems

Observed evidence:

- Existing hospital-management software
- Repeated downtime complaints
- Separate systems across departments
- Manual reconciliation
- No consolidated operational dashboard
- Active procurement role advertised
- Decision-maker not yet confirmed

Expected interpretation:

```text
Infrastructure class: REPLACEMENT or INTEGRATION
Operational need: Very high
Account value: Very high
Buying intent: Moderate to high
Pursuit readiness: Moderate
Recommended action: RESEARCH_AND_ENRICH
```

This opportunity may outrank a small organization with no software because business impact and account value are materially higher.

## 21.3 Small legal office with no portal

Observed evidence:

- One office
- Basic website
- No client portal detected
- No evidence that a portal is required
- No buying signal
- Generic contact form only

Expected interpretation:

```text
Portal state: NOT_DETECTED, not ABSENT_CONFIRMED
Portal relevance: Unknown or moderate
Operational need: Low confidence
Account value: Low
Recommended action: MONITOR or DEPRIORITIZE
```

## 21.4 Strong infrastructure account

Observed evidence:

- Modern integrated platform
- Strong digital access
- Reliable reporting
- Documented APIs
- Strong ownership and portability
- No meaningful current pain

Expected interpretation:

```text
Infrastructure class: LOW_GAP
Operational need: Low
Strategic fit may still be high
Opportunity value: Low unless a new trigger or expansion need exists
Recommended action: LOW_PRIORITY_POOL or MONITOR
```

---

# 22. Operator experience

The Lead Dossier should show:

```text
Opportunity Priority Score
Opportunity Value
Pursuit Readiness
Eligibility
Coverage
Confidence
Risk
Recommended Action
Infrastructure Opportunity Class
Dimension breakdown
Capability gap matrix
Evidence graph
Unknowns
Contradictions
Score history
Model version
Policy version
```

## 22.1 Capability gap matrix

Recommended columns:

| Capability | Condition | Relevance | Impact | Confidence | Evidence |
|---|---|---:|---:|---|---|
| Public website | Absent confirmed | High | Medium | High | Linked assertions |
| Customer portal | Absent confirmed | High | High | Medium | Linked assertions |
| Core operating system | Severely weak | Critical | High | High | Linked assertions |
| Workflow automation | Fragmented | High | High | Medium | Linked assertions |
| Reporting | Limited | High | Medium | High | Linked assertions |
| Connected monitoring | Unknown | Low | Unknown | Low | Research required |

## 22.2 Explanation-first display

The interface must not present only a score.

Every dimension should expose:

- Earned points and maximum
- Coverage
- Confidence
- Positive drivers
- Negative drivers
- Unknowns
- Contradictions
- Last evaluated time
- Evidence links

---

# 23. APIs and events

Planned conceptual interfaces:

```http
GET  /api/v1/opportunity-models
GET  /api/v1/opportunity-models/{model_version}
POST /api/v1/opportunity-models/{model_version}/evaluate

GET  /api/v1/institutions/{institution_id}/opportunity-assessments
GET  /api/v1/institutions/{institution_id}/opportunity-assessments/current
GET  /api/v1/opportunity-assessments/{assessment_id}
POST /api/v1/opportunity-assessments/{assessment_id}/review
POST /api/v1/opportunity-assessments/{assessment_id}/override

GET  /api/v1/institutions/{institution_id}/infrastructure-capabilities
POST /api/v1/institutions/{institution_id}/infrastructure-capabilities/evaluate
```

Suggested events:

```text
opportunity.assessment_requested
opportunity.assessment_completed
opportunity.assessment_review_required
opportunity.assessment_overridden
opportunity.score_changed
opportunity.recommendation_changed
infrastructure.capability_assessed
infrastructure.gap_confirmed
infrastructure.contradiction_detected
```

---

# 24. Implementation sequence

## Gate 1: Contracts and persistence

- Add model and policy version objects.
- Add opportunity assessment, dimension, subfactor, and capability records.
- Preserve legacy score fields.
- Add append-only assessment history.

## Gate 2: Evidence-linked capability assessment

- Define capability taxonomy.
- Add condition, relevance, impact, and detection states.
- Require evidence links.
- Prevent non-detection from becoming absence.

## Gate 3: Deterministic v3 evaluator

- Implement versioned weights and rubrics.
- Produce value, readiness, coverage, confidence, risk, and recommendation.
- Add explanation contract.

## Gate 4: Shadow-mode evaluation

- Run v3 beside the legacy score.
- Do not change daily selection yet.
- Compare rankings and human decisions.

## Gate 5: Calibration

- Evaluate by sector, geography, opportunity class, and score band.
- Review false absence, false identity, and low-coverage high-score cases.
- Approve thresholds.

## Gate 6: Selection integration

- Replace legacy-score-only ranking with a governed selection policy.
- Use eligibility, recommendation, value, readiness, confidence, coverage, and risk.
- Snapshot the exact assessment at reservation time.

## Gate 7: Governed activation

- Approve model version.
- Activate in stages.
- Monitor outcomes and overrides.
- Retain rollback to the previous version.

---

# 25. Verification scenarios

The v3 implementation is not complete until tests prove that:

1. Confirmed absence of a mission-critical relevant capability receives stronger need credit than a minor weakness.
2. Non-detection never receives confirmed-absence credit.
3. Inspection failure lowers coverage rather than proving absence.
4. Not-applicable capabilities do not reduce the score.
5. Unknown factors remain distinct from zero.
6. A blocked lead cannot be activated despite a high score.
7. A review-required lead cannot publish automatically.
8. A large weak-system account may outrank a small no-system account when value and impact justify it.
9. A known organization type does not automatically receive strategic-fit credit.
10. Qualification affects eligibility rather than adding points.
11. Duplicate signals do not inflate the score.
12. Copied sources do not count as independent corroboration.
13. A named irrelevant contact does not receive decision-maker credit.
14. Contact suppression prevents channel activation.
15. Identity ambiguity lowers readiness or requires review.
16. Contradictory evidence remains visible.
17. Score, coverage, confidence, risk, and eligibility are returned separately.
18. Every material point traces to evidence.
19. Every assessment records model and policy versions.
20. Operator overrides preserve the original assessment.
21. Legacy and v3 results can run side by side.
22. Selection snapshots the exact assessment used.
23. Outcome feedback creates new evidence and does not rewrite the assessment history.
24. A model version can be rolled back safely.
25. Sector policies cannot silently alter locked published weights.
26. Connected Infrastructure remains an explicit capability family and is never removed merely because public evidence is difficult to collect.
27. A score cannot be interpreted as consent, identity truth, or guaranteed conversion.

---

# 26. Acceptance criteria

The model is production-ready only when:

- The v3 schema and evaluator are implemented.
- Every dimension and subfactor is versioned.
- Infrastructure capability relevance is sector-aware.
- Confirmed absence is evidence-backed.
- Unknown, not detected, not inspected, failed, and not applicable remain distinct.
- Opportunity Value and Pursuit Readiness remain separately visible.
- Coverage and confidence are calculated and explained.
- Risk remains separate.
- Eligibility gates are enforced.
- Daily selection no longer ranks solely by the legacy overall score.
- Human reviewers can inspect evidence and contradictions.
- Shadow-mode comparison is complete.
- Calibration meets approved thresholds.
- Sector and geography performance have been evaluated.
- Security, privacy, compliance, and audit requirements pass.
- Exact-head tests and CI pass without unresolved issues.

---

# 27. Locked model definition

> NEWAX Harvester Opportunity Scoring Model v3 identifies the strongest evidence-backed business-infrastructure opportunities by prioritizing confirmed absence and severe weakness of relevant infrastructure, then evaluating strategic fit, organizational value, buying timing, pursuit readiness, evidence quality, and identity confidence. Eligibility, coverage, confidence, and risk remain separate from the score, every material point remains explainable, and the customer remains in control of what is pursued or published.
