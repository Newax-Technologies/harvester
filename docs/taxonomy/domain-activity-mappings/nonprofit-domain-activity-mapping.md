# Harvester Nonprofit Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **92** canonical domains in `BS-016 Nonprofit` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-016-AP-001` | `ACT-PUB-011`; `ACT-PUB-012`; `ACT-PUB-009`; `ACT-PUB-022`; `ACT-PUB-023` | `ACT-PUB-020`; `ACT-PUB-030`; `ACT-PUB-017`; `ACT-MKT-013`; `ACT-DIG-008` | `ACT-PUB-015`; `ACT-PUB-021`; `ACT-PUB-032` |
| `BS-016-AP-002` | `ACT-PUB-011`; `ACT-PUB-012`; `ACT-PUB-009`; `ACT-PUB-022`; `ACT-PUB-023`; `ACT-EDU-002` | `ACT-PUB-020`; `ACT-PUB-030`; `ACT-PUB-017`; `ACT-MKT-013`; `ACT-DIG-008`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-PUB-015`; `ACT-PUB-021`; `ACT-PUB-032`; `ACT-RND-017`; `ACT-DIG-015` |
| `BS-016-AP-003` | `ACT-PUB-012`; `ACT-PUB-013`; `ACT-PUB-014`; `ACT-PUB-009`; `ACT-PUB-022` | `ACT-PUB-011`; `ACT-PUB-010`; `ACT-MKT-013`; `ACT-DIG-008` | `ACT-PUB-017`; `ACT-PUB-015`; `ACT-OPS-024` |
| `BS-016-AP-004` | `ACT-PUB-012`; `ACT-PUB-013`; `ACT-PUB-014`; `ACT-PUB-009`; `ACT-PUB-022` | `ACT-PUB-011`; `ACT-PUB-010`; `ACT-MKT-013`; `ACT-DIG-008`; `ACT-PUB-023` | `ACT-PUB-017`; `ACT-PUB-015`; `ACT-OPS-024` |
| `BS-016-AP-005` | `ACT-PUB-012`; `ACT-PUB-013`; `ACT-PUB-014`; `ACT-PUB-009`; `ACT-PUB-022`; `ACT-EDU-002` | `ACT-PUB-011`; `ACT-PUB-010`; `ACT-MKT-013`; `ACT-DIG-008`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-PUB-017`; `ACT-PUB-015`; `ACT-OPS-024`; `ACT-RND-017`; `ACT-DIG-015` |
| `BS-016-AP-006` | `ACT-PUB-012`; `ACT-PUB-013`; `ACT-PUB-014`; `ACT-PUB-009`; `ACT-PUB-022`; `ACT-COM-001`; `ACT-COM-002` | `ACT-PUB-011`; `ACT-PUB-010`; `ACT-MKT-013`; `ACT-DIG-008`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-PUB-017`; `ACT-PUB-015`; `ACT-OPS-024`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-016-AP-007` | `ACT-PUB-009`; `ACT-PUB-019`; `ACT-PUB-023`; `ACT-PUB-031`; `ACT-PUB-025` | `ACT-PUB-011`; `ACT-PUB-022`; `ACT-PUB-032`; `ACT-DIG-008` | `ACT-PUB-015`; `ACT-RND-006`; `ACT-PUB-010` |
| `BS-016-AP-008` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008`; `ACT-HLT-024`; `ACT-HLT-017` | `ACT-EDU-002`; `ACT-RND-001`; `ACT-QLT-015`; `ACT-PUB-011` | `ACT-PUB-015`; `ACT-PUB-010`; `ACT-PUB-017` |
| `BS-016-AP-009` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008` | `ACT-EDU-002`; `ACT-RND-001`; `ACT-HLT-024`; `ACT-QLT-015` | `ACT-PUB-011`; `ACT-PUB-015`; `ACT-PUB-010` |
| `BS-016-AP-010` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008`; `ACT-HLT-009`; `ACT-HLT-008` | `ACT-EDU-002`; `ACT-RND-001`; `ACT-HLT-024`; `ACT-QLT-015`; `ACT-HLT-010`; `ACT-HLT-023` | `ACT-PUB-011`; `ACT-PUB-015`; `ACT-PUB-010`; `ACT-HLT-014` |
| `BS-016-AP-011` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008`; `ACT-HLT-007`; `ACT-HLT-008` | `ACT-EDU-002`; `ACT-RND-001`; `ACT-HLT-024`; `ACT-QLT-015`; `ACT-HLT-010`; `ACT-HLT-023` | `ACT-PUB-011`; `ACT-PUB-015`; `ACT-PUB-010`; `ACT-HLT-014` |
| `BS-016-AP-012` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008`; `ACT-HLT-024`; `ACT-HLT-017` | `ACT-EDU-002`; `ACT-RND-001`; `ACT-QLT-015` | `ACT-PUB-011`; `ACT-PUB-015`; `ACT-PUB-010` |
| `BS-016-AP-013` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008`; `ACT-EDU-002` | `ACT-RND-001`; `ACT-HLT-024`; `ACT-QLT-015`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007`; `ACT-PUB-011` | `ACT-PUB-015`; `ACT-PUB-010`; `ACT-RND-017`; `ACT-DIG-015`; `ACT-PUB-017` |
| `BS-016-AP-014` | `ACT-PUB-009`; `ACT-MKT-013`; `ACT-PUB-023`; `ACT-PUB-022`; `ACT-DIG-008`; `ACT-RND-001`; `ACT-RND-007` | `ACT-EDU-002`; `ACT-HLT-024`; `ACT-QLT-015`; `ACT-DIG-007`; `ACT-EDU-014` | `ACT-PUB-011`; `ACT-PUB-015`; `ACT-PUB-010`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-016-AP-015` | `ACT-PUB-018`; `ACT-PUB-025`; `ACT-PUB-009`; `ACT-EDU-024`; `ACT-DIG-008` | `ACT-EDU-002`; `ACT-PUB-015`; `ACT-PUB-011`; `ACT-MKT-013` | `ACT-QLT-006`; `ACT-QLT-007`; `ACT-EDU-014` |
| `BS-016-AP-016` | `ACT-PUB-010`; `ACT-FIN-028`; `ACT-PUB-023`; `ACT-PRF-008`; `ACT-DIG-008` | `ACT-PUB-011`; `ACT-PUB-012`; `ACT-PUB-032`; `ACT-PUB-022` | `ACT-FIN-010`; `ACT-PUB-015`; `ACT-RND-006` |
| `BS-016-AP-017` | `ACT-PUB-010`; `ACT-FIN-028`; `ACT-PUB-023`; `ACT-PRF-008`; `ACT-DIG-008`; `ACT-FIN-010`; `ACT-FIN-011` | `ACT-PUB-011`; `ACT-PUB-012`; `ACT-PUB-032`; `ACT-PUB-022`; `ACT-QLT-010` | `ACT-PUB-015`; `ACT-RND-006`; `ACT-FIN-012`; `ACT-PRF-002` |
| `BS-016-AP-018` | `ACT-PUB-010`; `ACT-FIN-028`; `ACT-PUB-023`; `ACT-PRF-008`; `ACT-DIG-008`; `ACT-RND-001`; `ACT-RND-007` | `ACT-PUB-011`; `ACT-PUB-012`; `ACT-PUB-032`; `ACT-PUB-022`; `ACT-DIG-007`; `ACT-EDU-014` | `ACT-FIN-010`; `ACT-PUB-015`; `ACT-RND-006`; `ACT-PRF-001` |
| `BS-016-AP-019` | `ACT-PUB-010`; `ACT-FIN-028`; `ACT-PUB-023`; `ACT-PRF-008`; `ACT-DIG-008`; `ACT-EDU-002` | `ACT-PUB-011`; `ACT-PUB-012`; `ACT-PUB-032`; `ACT-PUB-022`; `ACT-EDU-001`; `ACT-EDU-005`; `ACT-EDU-007` | `ACT-FIN-010`; `ACT-PUB-015`; `ACT-RND-006`; `ACT-RND-017`; `ACT-DIG-015` |
| `BS-016-AP-020` | `ACT-PRF-022`; `ACT-PUB-011`; `ACT-PUB-012`; `ACT-DIG-008`; `ACT-QLT-010` | `ACT-PUB-017`; `ACT-PUB-018`; `ACT-DIG-005`; `ACT-OPS-017`; `ACT-DIG-009` | `ACT-PRF-021`; `ACT-EDU-002`; `ACT-DIG-010` |
| `BS-016-AP-021` | `ACT-PRF-022`; `ACT-PUB-011`; `ACT-PUB-012`; `ACT-DIG-008`; `ACT-QLT-010`; `ACT-FIN-016`; `ACT-FIN-022` | `ACT-PUB-017`; `ACT-PUB-018`; `ACT-DIG-005`; `ACT-OPS-017`; `ACT-DIG-009`; `ACT-FIN-021`; `ACT-FIN-019` | `ACT-PRF-021`; `ACT-EDU-002`; `ACT-DIG-010`; `ACT-FIN-018` |
| `BS-016-AP-022` | `ACT-PRF-022`; `ACT-PUB-011`; `ACT-PUB-012`; `ACT-DIG-008`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-PUB-017`; `ACT-PUB-018`; `ACT-DIG-005`; `ACT-OPS-017`; `ACT-DIG-009`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-PRF-021`; `ACT-EDU-002`; `ACT-DIG-010`; `ACT-LEG-013` |
| `BS-016-AP-023` | `ACT-PRF-022`; `ACT-PUB-011`; `ACT-PUB-012`; `ACT-DIG-008`; `ACT-QLT-010`; `ACT-RND-018`; `ACT-OPS-004` | `ACT-PUB-017`; `ACT-PUB-018`; `ACT-DIG-005`; `ACT-OPS-017`; `ACT-DIG-009`; `ACT-OPS-005`; `ACT-DIG-002` | `ACT-PRF-021`; `ACT-EDU-002`; `ACT-DIG-010`; `ACT-OPS-007`; `ACT-DIG-007` |

## 3. Domain assignments

### 3.1 Charity, relief and humanitarian work

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-CHA-001` | General Charities | `BS-016-AP-001` |
| `NPO-CHA-002` | Humanitarian Relief | `BS-016-AP-001` |
| `NPO-CHA-003` | Disaster Relief | `BS-016-AP-001` |
| `NPO-CHA-004` | Food Assistance | `BS-016-AP-001` |
| `NPO-CHA-005` | Shelter and Housing Assistance | `BS-016-AP-001` |
| `NPO-CHA-006` | Medical Relief | `BS-016-AP-001` |
| `NPO-CHA-007` | Education Assistance | `BS-016-AP-002` |
| `NPO-CHA-008` | Orphan Support | `BS-016-AP-001` |
| `NPO-CHA-009` | Refugee and Displacement Support | `BS-016-AP-001` |
| `NPO-CHA-010` | Emergency Cash Assistance | `BS-016-AP-001` |
| `NPO-CHA-011` | Water and Sanitation Programs | `BS-016-AP-001` |
| `NPO-CHA-012` | Winterization and Seasonal Relief | `BS-016-AP-001` |

### 3.2 Faith-based giving and institutions

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-FAI-001` | Zakat Organizations | `BS-016-AP-003` |
| `NPO-FAI-002` | Waqf Institutions | `BS-016-AP-003` |
| `NPO-FAI-003` | Sadaqah and Charity Platforms | `BS-016-AP-004` |
| `NPO-FAI-004` | Mosque and Religious Charities | `BS-016-AP-003` |
| `NPO-FAI-005` | Religious Education Charities | `BS-016-AP-005` |
| `NPO-FAI-006` | Pilgrim Welfare Organizations | `BS-016-AP-003` |
| `NPO-FAI-007` | Faith-Based Development Organizations | `BS-016-AP-003` |
| `NPO-FAI-008` | Qurbani and Food Distribution Programs | `BS-016-AP-006` |
| `NPO-FAI-009` | Islamic Endowment Management | `BS-016-AP-003` |

### 3.3 Development and community programs

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-DEV-001` | Community Development | `BS-016-AP-007` |
| `NPO-DEV-002` | Rural Development | `BS-016-AP-007` |
| `NPO-DEV-003` | Urban Community Programs | `BS-016-AP-007` |
| `NPO-DEV-004` | Livelihood Development | `BS-016-AP-007` |
| `NPO-DEV-005` | Skills and Employment Programs | `BS-016-AP-007` |
| `NPO-DEV-006` | Microenterprise Support | `BS-016-AP-007` |
| `NPO-DEV-007` | Women's Empowerment | `BS-016-AP-007` |
| `NPO-DEV-008` | Youth Development | `BS-016-AP-007` |
| `NPO-DEV-009` | Disability Inclusion | `BS-016-AP-007` |
| `NPO-DEV-010` | Senior Support | `BS-016-AP-007` |
| `NPO-DEV-011` | Child Protection | `BS-016-AP-007` |
| `NPO-DEV-012` | Social Cohesion | `BS-016-AP-007` |
| `NPO-DEV-013` | Peacebuilding and Conflict Resolution | `BS-016-AP-007` |
| `NPO-DEV-014` | Civic Participation | `BS-016-AP-007` |

### 3.4 Health, education and environment nonprofits

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-HLT-001` | Public Health NGOs | `BS-016-AP-008` |
| `NPO-HLT-002` | Maternal and Child Health | `BS-016-AP-009` |
| `NPO-HLT-003` | Mental Health Support | `BS-016-AP-010` |
| `NPO-HLT-004` | Disability Rehabilitation | `BS-016-AP-011` |
| `NPO-HLT-005` | Health Awareness and Screening | `BS-016-AP-012` |
| `NPO-HLT-006` | Education NGOs | `BS-016-AP-013` |
| `NPO-HLT-007` | Scholarship Foundations | `BS-016-AP-009` |
| `NPO-HLT-008` | Literacy Programs | `BS-016-AP-009` |
| `NPO-HLT-009` | Research and Policy Organizations | `BS-016-AP-014` |
| `NPO-HLT-010` | Environmental Conservation | `BS-016-AP-009` |
| `NPO-HLT-011` | Climate Action | `BS-016-AP-009` |
| `NPO-HLT-012` | Wildlife Protection | `BS-016-AP-009` |
| `NPO-HLT-013` | Animal Welfare | `BS-016-AP-009` |

### 3.5 Membership and professional organizations

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-MEM-001` | Trade Associations | `BS-016-AP-015` |
| `NPO-MEM-002` | Chambers of Commerce | `BS-016-AP-015` |
| `NPO-MEM-003` | Professional Bodies | `BS-016-AP-015` |
| `NPO-MEM-004` | Industry Councils | `BS-016-AP-015` |
| `NPO-MEM-005` | Cooperatives | `BS-016-AP-015` |
| `NPO-MEM-006` | Alumni Associations | `BS-016-AP-015` |
| `NPO-MEM-007` | Community Associations | `BS-016-AP-015` |
| `NPO-MEM-008` | Sports Associations | `BS-016-AP-015` |
| `NPO-MEM-009` | Cultural Associations | `BS-016-AP-015` |
| `NPO-MEM-010` | Patient Associations | `BS-016-AP-015` |
| `NPO-MEM-011` | Advocacy Coalitions | `BS-016-AP-015` |
| `NPO-MEM-012` | Standards Organizations | `BS-016-AP-015` |

### 3.6 Foundations, philanthropy and grantmaking

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-FND-001` | Private Foundations | `BS-016-AP-016` |
| `NPO-FND-002` | Corporate Foundations | `BS-016-AP-016` |
| `NPO-FND-003` | Family Foundations | `BS-016-AP-016` |
| `NPO-FND-004` | Community Foundations | `BS-016-AP-016` |
| `NPO-FND-005` | Grantmaking Organizations | `BS-016-AP-016` |
| `NPO-FND-006` | Donor-Advised Funds | `BS-016-AP-017` |
| `NPO-FND-007` | Social Investment Funds | `BS-016-AP-017` |
| `NPO-FND-008` | Research Foundations | `BS-016-AP-018` |
| `NPO-FND-009` | Education Foundations | `BS-016-AP-019` |
| `NPO-FND-010` | Healthcare Foundations | `BS-016-AP-016` |
| `NPO-FND-011` | Arts and Culture Foundations | `BS-016-AP-016` |
| `NPO-FND-012` | Endowment Management | `BS-016-AP-016` |

### 3.7 Nonprofit operations and technology

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `NPO-OPS-001` | Fundraising and Donations | `BS-016-AP-020` |
| `NPO-OPS-002` | Donor Management | `BS-016-AP-020` |
| `NPO-OPS-003` | Grant Management | `BS-016-AP-020` |
| `NPO-OPS-004` | Program and Project Management | `BS-016-AP-020` |
| `NPO-OPS-005` | Beneficiary Registration | `BS-016-AP-020` |
| `NPO-OPS-006` | Case Management | `BS-016-AP-020` |
| `NPO-OPS-007` | Volunteer Management | `BS-016-AP-020` |
| `NPO-OPS-008` | Membership Management | `BS-016-AP-020` |
| `NPO-OPS-009` | Event and Campaign Management | `BS-016-AP-020` |
| `NPO-OPS-010` | Impact Measurement | `BS-016-AP-020` |
| `NPO-OPS-011` | Monitoring and Evaluation | `BS-016-AP-020` |
| `NPO-OPS-012` | Financial and Fund Accounting | `BS-016-AP-021` |
| `NPO-OPS-013` | Compliance and Reporting | `BS-016-AP-022` |
| `NPO-OPS-014` | Safeguarding Management | `BS-016-AP-020` |
| `NPO-OPS-015` | Nonprofit CRM Systems | `BS-016-AP-023` |
| `NPO-OPS-016` | Donation Platforms | `BS-016-AP-023` |
| `NPO-OPS-017` | Volunteer Platforms | `BS-016-AP-023` |
| `NPO-OPS-018` | Beneficiary Portals | `BS-016-AP-023` |
| `NPO-OPS-019` | Nonprofit Data and Analytics | `BS-016-AP-020` |
| `NPO-OPS-020` | Field Operations and Mobile Data Collection | `BS-016-AP-020` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
