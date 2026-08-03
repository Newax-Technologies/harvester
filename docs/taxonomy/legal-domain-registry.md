# Harvester Legal Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-006 Legal`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Legal
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

This registry contains **97 canonical domains** in **6 families**.

| Family | Name | Count |
| --- | --- | --- |
| `LEG-PRA` | Legal practice areas | 23 |
| `LEG-DIS` | Disputes and representation | 16 |
| `LEG-PER` | Personal and family legal services | 12 |
| `LEG-REG` | Regulatory, compliance and governance | 14 |
| `LEG-OPS` | Legal operations and support | 18 |
| `LEG-DIG` | Legal technology and information | 14 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Legal practice areas

| Code | Domain |
| --- | --- |
| `LEG-PRA-001` | Corporate and Commercial Law |
| `LEG-PRA-002` | Company Formation and Corporate Secretarial Law |
| `LEG-PRA-003` | Contract Law |
| `LEG-PRA-004` | Banking and Finance Law |
| `LEG-PRA-005` | Islamic Finance Law |
| `LEG-PRA-006` | Tax Law |
| `LEG-PRA-007` | Employment and Labour Law |
| `LEG-PRA-008` | Intellectual Property Law |
| `LEG-PRA-009` | Technology and Data Law |
| `LEG-PRA-010` | Privacy and Data Protection Law |
| `LEG-PRA-011` | Competition and Antitrust Law |
| `LEG-PRA-012` | Real Estate and Property Law |
| `LEG-PRA-013` | Construction Law |
| `LEG-PRA-014` | Energy and Infrastructure Law |
| `LEG-PRA-015` | Healthcare and Life Sciences Law |
| `LEG-PRA-016` | Education Law |
| `LEG-PRA-017` | Environmental Law |
| `LEG-PRA-018` | Maritime and Shipping Law |
| `LEG-PRA-019` | Aviation Law |
| `LEG-PRA-020` | Customs and Trade Law |
| `LEG-PRA-021` | Insurance and Takaful Law |
| `LEG-PRA-022` | Public Procurement Law |
| `LEG-PRA-023` | Constitutional and Administrative Law |

### 4.2 Disputes and representation

| Code | Domain |
| --- | --- |
| `LEG-DIS-001` | Civil Litigation |
| `LEG-DIS-002` | Commercial Litigation |
| `LEG-DIS-003` | Criminal Defence |
| `LEG-DIS-004` | Family Litigation |
| `LEG-DIS-005` | Employment Disputes |
| `LEG-DIS-006` | Tax Disputes |
| `LEG-DIS-007` | Property Disputes |
| `LEG-DIS-008` | Construction Disputes |
| `LEG-DIS-009` | Banking Disputes |
| `LEG-DIS-010` | Intellectual Property Disputes |
| `LEG-DIS-011` | Arbitration |
| `LEG-DIS-012` | Mediation |
| `LEG-DIS-013` | Alternative Dispute Resolution |
| `LEG-DIS-014` | Appellate Practice |
| `LEG-DIS-015` | Regulatory Investigations |
| `LEG-DIS-016` | White-Collar and Financial Crime |

### 4.3 Personal and family legal services

| Code | Domain |
| --- | --- |
| `LEG-PER-001` | Family Law |
| `LEG-PER-002` | Marriage and Divorce Law |
| `LEG-PER-003` | Child Custody and Guardianship |
| `LEG-PER-004` | Inheritance and Succession |
| `LEG-PER-005` | Wills and Estate Planning |
| `LEG-PER-006` | Immigration Law |
| `LEG-PER-007` | Citizenship and Nationality |
| `LEG-PER-008` | Consumer Protection |
| `LEG-PER-009` | Personal Injury |
| `LEG-PER-010` | Medical Negligence |
| `LEG-PER-011` | Human Rights Law |
| `LEG-PER-012` | Legal Aid |

### 4.4 Regulatory, compliance and governance

| Code | Domain |
| --- | --- |
| `LEG-REG-001` | Corporate Compliance |
| `LEG-REG-002` | Regulatory Compliance |
| `LEG-REG-003` | Anti-Money-Laundering Compliance |
| `LEG-REG-004` | Know-Your-Customer Compliance |
| `LEG-REG-005` | Sanctions Compliance |
| `LEG-REG-006` | Shariah Governance Support |
| `LEG-REG-007` | Licensing and Registration |
| `LEG-REG-008` | Board and Governance Advisory |
| `LEG-REG-009` | Policy Drafting |
| `LEG-REG-010` | Internal Investigations |
| `LEG-REG-011` | Whistleblowing and Ethics Programs |
| `LEG-REG-012` | Legal Risk Management |
| `LEG-REG-013` | Contract Compliance |
| `LEG-REG-014` | Third-Party Due Diligence |

### 4.5 Legal operations and support

| Code | Domain |
| --- | --- |
| `LEG-OPS-001` | Legal Research |
| `LEG-OPS-002` | Legal Drafting |
| `LEG-OPS-003` | Contract Drafting |
| `LEG-OPS-004` | Contract Review |
| `LEG-OPS-005` | Document Review |
| `LEG-OPS-006` | Due Diligence |
| `LEG-OPS-007` | Legal Translation |
| `LEG-OPS-008` | Court Filing and Process Services |
| `LEG-OPS-009` | Notary and Attestation |
| `LEG-OPS-010` | Trademark and Patent Filing |
| `LEG-OPS-011` | Company Registration Services |
| `LEG-OPS-012` | Legal Document Management |
| `LEG-OPS-013` | Matter and Case Management |
| `LEG-OPS-014` | Legal Billing and Timekeeping |
| `LEG-OPS-015` | E-Discovery |
| `LEG-OPS-016` | Litigation Support |
| `LEG-OPS-017` | Legal Staffing and Outsourcing |
| `LEG-OPS-018` | Expert Witness Services |

### 4.6 Legal technology and information

| Code | Domain |
| --- | --- |
| `LEG-DIG-001` | Case Management Systems |
| `LEG-DIG-002` | Matter Management Systems |
| `LEG-DIG-003` | Contract Lifecycle Management |
| `LEG-DIG-004` | Legal CRM Systems |
| `LEG-DIG-005` | Client Portals |
| `LEG-DIG-006` | Document Automation |
| `LEG-DIG-007` | Legal Knowledge Management |
| `LEG-DIG-008` | Legal Research Platforms |
| `LEG-DIG-009` | Compliance Management Systems |
| `LEG-DIG-010` | E-Discovery Platforms |
| `LEG-DIG-011` | Digital Signature and Execution |
| `LEG-DIG-012` | Court and Hearing Management |
| `LEG-DIG-013` | Legal Analytics |
| `LEG-DIG-014` | Intellectual Property Management Systems |

## 5. First-release presentation shortlist

Corporate and Commercial Law, Contract Law, Banking and Finance Law, Islamic Finance Law, Tax Law, Employment Law, Intellectual Property Law, Technology and Data Law, Privacy and Data Protection, Real Estate Law, Construction Law, Healthcare Law, Civil Litigation, Commercial Litigation, Criminal Defence, Family Law, Arbitration, Mediation, Corporate Compliance, AML and KYC Compliance, Licensing and Registration, Legal Research, Contract Drafting, Contract Review, Due Diligence, Court Filing, Notary and Attestation, Company Registration Services, Case Management Systems, Matter Management Systems, Contract Lifecycle Management, Legal CRM Systems, Client Portals, Document Automation, Compliance Management Systems, Legal Analytics.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Law firms:** Advising, Representing, Drafting, Reviewing, Filing, Negotiating
- **Litigation practices:** Investigating, Pleading, Managing evidence, Appearing, Appealing
- **Compliance providers:** Assessing, Monitoring, Reporting, Training, Remediating
- **Legal technology:** Developing, Licensing, Implementing, Integrating, Supporting

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Healthcare law | Healthcare | Advising; licensing; compliance |
| Construction law | Construction; Real Estate | Drafting; disputes; claims |
| Financial compliance | Finance | Assessing; monitoring; reporting |
| Legal technology | Technology | Developing; implementing; hosting |

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

- The shortlist and all 97 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
