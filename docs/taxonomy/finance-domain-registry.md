# Harvester Finance Product and Service Domain Registry

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file defines the controlled product and service domain registry for `BS-007 Finance`.

Authority: [ROADMAP](../ROADMAP.md), [Intelligence Operating Model](../architecture/harvester-intelligence-operating-model.md), [Services and Opportunity Model](../SERVICES.md), and [Broad Sector Registry](broad-sector-registry.md).

## 1. Locked selection model

```text
Finance
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

This registry contains **109 canonical domains** in **7 families**.

| Family | Name | Count |
| --- | --- | --- |
| `FIN-BNK` | Banking and financing | 17 |
| `FIN-PAY` | Payments and money movement | 15 |
| `FIN-INV` | Investment and capital markets | 16 |
| `FIN-TAK` | Takaful and protection | 12 |
| `FIN-ACC` | Accounting, audit and tax | 16 |
| `FIN-RISK` | Risk, compliance and governance | 15 |
| `FIN-DIG` | Financial technology and operations systems | 18 |

## 3. Governing rules

- Domain selection is multi-select.
- Every selected domain receives an independent activity group.
- Only approved domain–activity combinations proceed to service selection.
- Only active provider offerings may generate service-gap or opportunity assessments.
- Keywords discover evidence; they do not prove need.
- Canonical IDs remain stable when labels or aliases change.
- Completed harvest jobs retain the registry and mapping versions used when they ran.

## 4. Canonical domain registry

### 4.1 Banking and financing

| Code | Domain |
| --- | --- |
| `FIN-BNK-001` | Islamic Banking |
| `FIN-BNK-002` | Retail Banking |
| `FIN-BNK-003` | Corporate Banking |
| `FIN-BNK-004` | Commercial Banking |
| `FIN-BNK-005` | SME Banking |
| `FIN-BNK-006` | Microfinance |
| `FIN-BNK-007` | Islamic Microfinance |
| `FIN-BNK-008` | Development Finance |
| `FIN-BNK-009` | Trade Finance |
| `FIN-BNK-010` | Project Finance |
| `FIN-BNK-011` | Consumer Finance |
| `FIN-BNK-012` | Asset Finance |
| `FIN-BNK-013` | Ijarah and Leasing |
| `FIN-BNK-014` | Housing Finance |
| `FIN-BNK-015` | Agricultural Finance |
| `FIN-BNK-016` | Supply-Chain Finance |
| `FIN-BNK-017` | Factoring and Receivables Finance |

### 4.2 Payments and money movement

| Code | Domain |
| --- | --- |
| `FIN-PAY-001` | Payment Gateways |
| `FIN-PAY-002` | Digital Wallets |
| `FIN-PAY-003` | Merchant Acquiring |
| `FIN-PAY-004` | Point-of-Sale Payments |
| `FIN-PAY-005` | Mobile Payments |
| `FIN-PAY-006` | Bank Transfers |
| `FIN-PAY-007` | Real-Time Payments |
| `FIN-PAY-008` | Remittances |
| `FIN-PAY-009` | Currency Exchange |
| `FIN-PAY-010` | Cross-Border Payments |
| `FIN-PAY-011` | Payment Aggregation |
| `FIN-PAY-012` | Bill Payment Services |
| `FIN-PAY-013` | Payroll Disbursement |
| `FIN-PAY-014` | Government Payment Services |
| `FIN-PAY-015` | Payment Fraud Prevention |

### 4.3 Investment and capital markets

| Code | Domain |
| --- | --- |
| `FIN-INV-001` | Islamic Investment Management |
| `FIN-INV-002` | Asset Management |
| `FIN-INV-003` | Mutual Funds |
| `FIN-INV-004` | Pension Funds |
| `FIN-INV-005` | Private Equity |
| `FIN-INV-006` | Venture Capital |
| `FIN-INV-007` | Real Estate Investment |
| `FIN-INV-008` | Sukuk |
| `FIN-INV-009` | Equity Brokerage |
| `FIN-INV-010` | Commodity Brokerage |
| `FIN-INV-011` | Capital Markets Advisory |
| `FIN-INV-012` | Wealth Management |
| `FIN-INV-013` | Portfolio Management |
| `FIN-INV-014` | Custody Services |
| `FIN-INV-015` | Fund Administration |
| `FIN-INV-016` | Investment Research |

### 4.4 Takaful and protection

| Code | Domain |
| --- | --- |
| `FIN-TAK-001` | Family Takaful |
| `FIN-TAK-002` | General Takaful |
| `FIN-TAK-003` | Health Takaful |
| `FIN-TAK-004` | Motor Takaful |
| `FIN-TAK-005` | Property Takaful |
| `FIN-TAK-006` | Marine Takaful |
| `FIN-TAK-007` | Agricultural Takaful |
| `FIN-TAK-008` | Microtakaful |
| `FIN-TAK-009` | Takaful Brokerage |
| `FIN-TAK-010` | Takaful Claims Administration |
| `FIN-TAK-011` | Takaful Distribution |
| `FIN-TAK-012` | Risk Survey and Assessment |

### 4.5 Accounting, audit and tax

| Code | Domain |
| --- | --- |
| `FIN-ACC-001` | Accounting Services |
| `FIN-ACC-002` | Bookkeeping |
| `FIN-ACC-003` | Financial Reporting |
| `FIN-ACC-004` | Management Accounting |
| `FIN-ACC-005` | External Audit |
| `FIN-ACC-006` | Internal Audit |
| `FIN-ACC-007` | Forensic Accounting |
| `FIN-ACC-008` | Tax Advisory |
| `FIN-ACC-009` | Tax Compliance |
| `FIN-ACC-010` | Payroll Accounting |
| `FIN-ACC-011` | Cost Accounting |
| `FIN-ACC-012` | Treasury Operations |
| `FIN-ACC-013` | Accounts Payable Services |
| `FIN-ACC-014` | Accounts Receivable Services |
| `FIN-ACC-015` | Revenue Assurance |
| `FIN-ACC-016` | Financial Controls |

### 4.6 Risk, compliance and governance

| Code | Domain |
| --- | --- |
| `FIN-RISK-001` | Shariah Governance |
| `FIN-RISK-002` | Financial Crime Compliance |
| `FIN-RISK-003` | Anti-Money-Laundering |
| `FIN-RISK-004` | Know Your Customer |
| `FIN-RISK-005` | Sanctions Screening |
| `FIN-RISK-006` | Credit Risk Management |
| `FIN-RISK-007` | Market Risk Management |
| `FIN-RISK-008` | Operational Risk Management |
| `FIN-RISK-009` | Enterprise Risk Management |
| `FIN-RISK-010` | Fraud Detection |
| `FIN-RISK-011` | Regulatory Reporting |
| `FIN-RISK-012` | Capital and Liquidity Management |
| `FIN-RISK-013` | Model Risk Management |
| `FIN-RISK-014` | Governance, Risk and Compliance |
| `FIN-RISK-015` | Financial Due Diligence |

### 4.7 Financial technology and operations systems

| Code | Domain |
| --- | --- |
| `FIN-DIG-001` | Core Banking Systems |
| `FIN-DIG-002` | Islamic Banking Systems |
| `FIN-DIG-003` | Loan and Financing Origination |
| `FIN-DIG-004` | Financing Management Systems |
| `FIN-DIG-005` | Payment Processing Platforms |
| `FIN-DIG-006` | Digital Banking Platforms |
| `FIN-DIG-007` | Treasury Management Systems |
| `FIN-DIG-008` | Accounting Software |
| `FIN-DIG-009` | Enterprise Resource Planning for Finance |
| `FIN-DIG-010` | Billing and Invoicing Systems |
| `FIN-DIG-011` | Collection Management Systems |
| `FIN-DIG-012` | Reconciliation Systems |
| `FIN-DIG-013` | Regulatory Reporting Systems |
| `FIN-DIG-014` | Risk Analytics |
| `FIN-DIG-015` | Fraud Management Systems |
| `FIN-DIG-016` | Customer Onboarding and eKYC |
| `FIN-DIG-017` | Finance Data and Analytics |
| `FIN-DIG-018` | Open Banking and API Platforms |

## 5. First-release presentation shortlist

Islamic Banking, Corporate Banking, SME Banking, Islamic Microfinance, Trade Finance, Project Finance, Ijarah and Leasing, Housing Finance, Payment Gateways, Digital Wallets, Merchant Acquiring, Remittances, Currency Exchange, Islamic Investment Management, Asset Management, Sukuk, Wealth Management, Family Takaful, General Takaful, Accounting Services, External Audit, Internal Audit, Tax Advisory, Bookkeeping, Shariah Governance, AML and KYC, Credit Risk, Fraud Detection, Regulatory Reporting, Core Banking Systems, Islamic Banking Systems, Financing Origination, Payment Processing, Digital Banking Platforms, Accounting Software, Billing and Invoicing, Collection Management, Customer Onboarding and eKYC, Finance Data and Analytics.

Grouped display labels never replace canonical domain IDs in storage, evidence, APIs, or completed jobs.

## 6. Domain-specific activity examples

- **Islamic banking:** Onboarding, Financing, Servicing accounts, Processing payments, Reporting
- **Accounting and audit:** Recording, Reconciling, Auditing, Reporting, Advising
- **Payments:** Processing, Settling, Reconciling, Monitoring fraud, Integrating merchants
- **Takaful:** Underwriting, Issuing, Collecting contributions, Managing claims, Distributing

Selections for one domain must not be copied into another domain.

## 7. Cross-sector reuse examples

| Domain | Additional sectors | Example activities |
| --- | --- | --- |
| Agricultural finance | Food and Agriculture | Financing; risk assessment; collections |
| Real estate investment | Real Estate | Investing; managing; reporting |
| Financial technology | Technology | Developing; integrating; hosting |
| Takaful claims | Healthcare; Retail | Assessing; processing; settling |

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

- The shortlist and all 109 canonical domains are accessible.
- Multiple domains can be selected.
- Every domain has a separate activity group.
- Domain–activity combinations can be enabled, disabled, paused, and prioritized.
- Cross-sector mappings reuse canonical domain identity.
- The same target is not duplicated across overlapping classifications.
- Every opportunity retains its sector, domain, activity, offering, evidence, decision, and version path.
- Unselected services and unsupported gaps cannot influence discovery, scoring, export, publication, or outreach.

## 10. Delivery boundary

This registry is **defined** but is not **implemented**, **integrated**, **CI Green**, or **complete** until schema, migrations, APIs, interface, mappings, validation, tests, and release controls are verified.
