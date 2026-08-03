# Harvester Nonprofit Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-016 Nonprofit`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Nonprofit
→ select one or more domains
→ configure a separate activity group for each domain
→ approve domain–activity combinations
→ attach services the provider actually offers
→ configure keywords and evidence
→ assess supported opportunities
→ qualify leads
```

Selecting this sector does not select every domain or activity. Activities do not propagate between domains. Cross-sector reuse preserves one canonical domain identity and does not duplicate organizations, evidence, opportunities, or scores.

## 2. Registry summary

This registry contains **92 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `NPO-CHA` | Charity, relief and humanitarian work | 12 |
| `NPO-FAI` | Faith-based giving and institutions | 9 |
| `NPO-DEV` | Development and community programs | 14 |
| `NPO-HLT` | Health, education and environment nonprofits | 13 |
| `NPO-MEM` | Membership and professional organizations | 12 |
| `NPO-FND` | Foundations, philanthropy and grantmaking | 12 |
| `NPO-OPS` | Nonprofit operations and technology | 20 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Charity, relief and humanitarian work

| Code | Domain |
| --- | --- |
| `NPO-CHA-001` | General Charities |
| `NPO-CHA-002` | Humanitarian Relief |
| `NPO-CHA-003` | Disaster Relief |
| `NPO-CHA-004` | Food Assistance |
| `NPO-CHA-005` | Shelter and Housing Assistance |
| `NPO-CHA-006` | Medical Relief |
| `NPO-CHA-007` | Education Assistance |
| `NPO-CHA-008` | Orphan Support |
| `NPO-CHA-009` | Refugee and Displacement Support |
| `NPO-CHA-010` | Emergency Cash Assistance |
| `NPO-CHA-011` | Water and Sanitation Programs |
| `NPO-CHA-012` | Winterization and Seasonal Relief |

### 4.2 Faith-based giving and institutions

| Code | Domain |
| --- | --- |
| `NPO-FAI-001` | Zakat Organizations |
| `NPO-FAI-002` | Waqf Institutions |
| `NPO-FAI-003` | Sadaqah and Charity Platforms |
| `NPO-FAI-004` | Mosque and Religious Charities |
| `NPO-FAI-005` | Religious Education Charities |
| `NPO-FAI-006` | Pilgrim Welfare Organizations |
| `NPO-FAI-007` | Faith-Based Development Organizations |
| `NPO-FAI-008` | Qurbani and Food Distribution Programs |
| `NPO-FAI-009` | Islamic Endowment Management |

### 4.3 Development and community programs

| Code | Domain |
| --- | --- |
| `NPO-DEV-001` | Community Development |
| `NPO-DEV-002` | Rural Development |
| `NPO-DEV-003` | Urban Community Programs |
| `NPO-DEV-004` | Livelihood Development |
| `NPO-DEV-005` | Skills and Employment Programs |
| `NPO-DEV-006` | Microenterprise Support |
| `NPO-DEV-007` | Women's Empowerment |
| `NPO-DEV-008` | Youth Development |
| `NPO-DEV-009` | Disability Inclusion |
| `NPO-DEV-010` | Senior Support |
| `NPO-DEV-011` | Child Protection |
| `NPO-DEV-012` | Social Cohesion |
| `NPO-DEV-013` | Peacebuilding and Conflict Resolution |
| `NPO-DEV-014` | Civic Participation |

### 4.4 Health, education and environment nonprofits

| Code | Domain |
| --- | --- |
| `NPO-HLT-001` | Public Health NGOs |
| `NPO-HLT-002` | Maternal and Child Health |
| `NPO-HLT-003` | Mental Health Support |
| `NPO-HLT-004` | Disability Rehabilitation |
| `NPO-HLT-005` | Health Awareness and Screening |
| `NPO-HLT-006` | Education NGOs |
| `NPO-HLT-007` | Scholarship Foundations |
| `NPO-HLT-008` | Literacy Programs |
| `NPO-HLT-009` | Research and Policy Organizations |
| `NPO-HLT-010` | Environmental Conservation |
| `NPO-HLT-011` | Climate Action |
| `NPO-HLT-012` | Wildlife Protection |
| `NPO-HLT-013` | Animal Welfare |

### 4.5 Membership and professional organizations

| Code | Domain |
| --- | --- |
| `NPO-MEM-001` | Trade Associations |
| `NPO-MEM-002` | Chambers of Commerce |
| `NPO-MEM-003` | Professional Bodies |
| `NPO-MEM-004` | Industry Councils |
| `NPO-MEM-005` | Cooperatives |
| `NPO-MEM-006` | Alumni Associations |
| `NPO-MEM-007` | Community Associations |
| `NPO-MEM-008` | Sports Associations |
| `NPO-MEM-009` | Cultural Associations |
| `NPO-MEM-010` | Patient Associations |
| `NPO-MEM-011` | Advocacy Coalitions |
| `NPO-MEM-012` | Standards Organizations |

### 4.6 Foundations, philanthropy and grantmaking

| Code | Domain |
| --- | --- |
| `NPO-FND-001` | Private Foundations |
| `NPO-FND-002` | Corporate Foundations |
| `NPO-FND-003` | Family Foundations |
| `NPO-FND-004` | Community Foundations |
| `NPO-FND-005` | Grantmaking Organizations |
| `NPO-FND-006` | Donor-Advised Funds |
| `NPO-FND-007` | Social Investment Funds |
| `NPO-FND-008` | Research Foundations |
| `NPO-FND-009` | Education Foundations |
| `NPO-FND-010` | Healthcare Foundations |
| `NPO-FND-011` | Arts and Culture Foundations |
| `NPO-FND-012` | Endowment Management |

### 4.7 Nonprofit operations and technology

| Code | Domain |
| --- | --- |
| `NPO-OPS-001` | Fundraising and Donations |
| `NPO-OPS-002` | Donor Management |
| `NPO-OPS-003` | Grant Management |
| `NPO-OPS-004` | Program and Project Management |
| `NPO-OPS-005` | Beneficiary Registration |
| `NPO-OPS-006` | Case Management |
| `NPO-OPS-007` | Volunteer Management |
| `NPO-OPS-008` | Membership Management |
| `NPO-OPS-009` | Event and Campaign Management |
| `NPO-OPS-010` | Impact Measurement |
| `NPO-OPS-011` | Monitoring and Evaluation |
| `NPO-OPS-012` | Financial and Fund Accounting |
| `NPO-OPS-013` | Compliance and Reporting |
| `NPO-OPS-014` | Safeguarding Management |
| `NPO-OPS-015` | Nonprofit CRM Systems |
| `NPO-OPS-016` | Donation Platforms |
| `NPO-OPS-017` | Volunteer Platforms |
| `NPO-OPS-018` | Beneficiary Portals |
| `NPO-OPS-019` | Nonprofit Data and Analytics |
| `NPO-OPS-020` | Field Operations and Mobile Data Collection |

## 5. First-release presentation shortlist

General Charities, Humanitarian Relief, Disaster Relief, Food Assistance, Medical Relief, Education Assistance, Orphan Support, Refugee Support, Zakat Organizations, Waqf Institutions, Faith-Based Charities, Community Development, Livelihood Programs, Skills and Employment, Women's Empowerment, Youth Development, Disability Inclusion, Child Protection, Public Health NGOs, Education NGOs, Scholarship Foundations, Environmental Conservation, Animal Welfare, Trade Associations, Chambers of Commerce, Professional Bodies, Cooperatives, Private Foundations, Corporate Foundations, Grantmaking Organizations, Fundraising and Donations, Donor Management, Grant Management, Beneficiary Registration, Volunteer Management, Impact Measurement, Monitoring and Evaluation, Nonprofit CRM, Donation Platforms, Field Data Collection.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Charities:** Fundraising, Registering beneficiaries, Delivering aid, Monitoring, Reporting
- **Associations:** Recruiting members, Collecting dues, Advocating, Certifying, Organizing events
- **Foundations:** Grantmaking, Due diligence, Monitoring grants, Measuring impact, Reporting
- **Nonprofit platforms:** Collecting donations, Managing donors, Coordinating volunteers, Publishing impact

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Medical relief | Healthcare | Screening; treating; distributing supplies |
| Education NGOs | Education | Teaching; funding; monitoring |
| Waqf institutions | Finance; Real Estate | Managing assets; distributing benefits |
| Humanitarian logistics | Logistics; Government | Warehousing; transporting; delivering |

## 8. Required domain metadata

```text
id
code
name
description
domain_type
family_code
status
version
aliases
sector_mappings
allowed_activity_ids
recommended_activity_ids
qualification_guidance
exclusion_guidance
created_at
updated_at
```

## 9. Acceptance criteria

- The shortlist and all 92 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
