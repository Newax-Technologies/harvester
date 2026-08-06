# Harvester Finance Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **109** canonical domains in `BS-007 Finance` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-007-AP-001` | `ACT-FIN-001`; `ACT-FIN-002`; `ACT-FIN-005`; `ACT-FIN-023`; `ACT-QLT-010` | `ACT-FIN-003`; `ACT-FIN-004`; `ACT-COM-026`; `ACT-FIN-006`; `ACT-FIN-024`; `ACT-FIN-022` | `ACT-FIN-025`; `ACT-COM-012`; `ACT-FIN-010` |
| `BS-007-AP-002` | `ACT-FIN-006`; `ACT-FIN-032`; `ACT-FIN-031`; `ACT-COM-026`; `ACT-QLT-010` | `ACT-FIN-007`; `ACT-FIN-008`; `ACT-FIN-009`; `ACT-QLT-023`; `ACT-QLT-025`; `ACT-OPS-018` | `ACT-DIG-016`; `ACT-DIG-013` |
| `BS-007-AP-003` | `ACT-FIN-006`; `ACT-FIN-032`; `ACT-FIN-031`; `ACT-COM-026`; `ACT-QLT-010` | `ACT-FIN-007`; `ACT-FIN-008`; `ACT-FIN-009`; `ACT-QLT-023`; `ACT-QLT-025` | `ACT-DIG-016`; `ACT-DIG-013`; `ACT-OPS-018` |
| `BS-007-AP-004` | `ACT-FIN-006`; `ACT-FIN-032`; `ACT-FIN-031`; `ACT-COM-026`; `ACT-QLT-010`; `ACT-FIN-002`; `ACT-FIN-023` | `ACT-FIN-007`; `ACT-FIN-008`; `ACT-FIN-009`; `ACT-QLT-023`; `ACT-QLT-025`; `ACT-FIN-022` | `ACT-DIG-016`; `ACT-DIG-013`; `ACT-OPS-018`; `ACT-FIN-024`; `ACT-FIN-025` |
| `BS-007-AP-005` | `ACT-FIN-010`; `ACT-FIN-011`; `ACT-FIN-035`; `ACT-QLT-010`; `ACT-DIG-008` | `ACT-FIN-012`; `ACT-FIN-028`; `ACT-PRF-002`; `ACT-PRF-008`; `ACT-QLT-013` | `ACT-FIN-026`; `ACT-FIN-013`; `ACT-COM-020` |
| `BS-007-AP-006` | `ACT-FIN-010`; `ACT-FIN-011`; `ACT-FIN-035`; `ACT-QLT-010`; `ACT-DIG-008`; `ACT-RND-001`; `ACT-RND-007` | `ACT-FIN-012`; `ACT-FIN-028`; `ACT-PRF-002`; `ACT-PRF-008`; `ACT-QLT-013`; `ACT-DIG-007`; `ACT-EDU-014` | `ACT-FIN-026`; `ACT-FIN-013`; `ACT-COM-020`; `ACT-PRF-001`; `ACT-RND-006` |
| `BS-007-AP-007` | `ACT-FIN-014`; `ACT-FIN-013`; `ACT-FIN-015`; `ACT-QLT-013`; `ACT-QLT-010` | `ACT-COM-026`; `ACT-FIN-006`; `ACT-DIG-008`; `ACT-OPS-018` | `ACT-FIN-010`; `ACT-QLT-023`; `ACT-DIG-015` |
| `BS-007-AP-008` | `ACT-FIN-014`; `ACT-FIN-013`; `ACT-FIN-015`; `ACT-QLT-013`; `ACT-QLT-010`; `ACT-COM-001`; `ACT-COM-002` | `ACT-COM-026`; `ACT-FIN-006`; `ACT-DIG-008`; `ACT-OPS-018`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-FIN-010`; `ACT-QLT-023`; `ACT-DIG-015`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-007-AP-009` | `ACT-FIN-016`; `ACT-FIN-017`; `ACT-FIN-022`; `ACT-FIN-021`; `ACT-QLT-010` | `ACT-FIN-019`; `ACT-FIN-020`; `ACT-FIN-018`; `ACT-FIN-031`; `ACT-PRF-002` | `ACT-PRF-021`; `ACT-DIG-009`; `ACT-PRF-008` |
| `BS-007-AP-010` | `ACT-FIN-016`; `ACT-FIN-017`; `ACT-FIN-022`; `ACT-FIN-021`; `ACT-QLT-010`; `ACT-FIN-002`; `ACT-FIN-023` | `ACT-FIN-019`; `ACT-FIN-020`; `ACT-FIN-018`; `ACT-FIN-031`; `ACT-PRF-002`; `ACT-COM-026` | `ACT-PRF-021`; `ACT-DIG-009`; `ACT-PRF-008`; `ACT-FIN-024`; `ACT-FIN-025` |
| `BS-007-AP-011` | `ACT-FIN-016`; `ACT-FIN-017`; `ACT-FIN-022`; `ACT-FIN-021`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-FIN-019`; `ACT-FIN-020`; `ACT-FIN-018`; `ACT-FIN-031`; `ACT-PRF-002`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-PRF-021`; `ACT-DIG-009`; `ACT-PRF-008`; `ACT-EDU-002`; `ACT-LEG-013` |
| `BS-007-AP-012` | `ACT-QLT-013`; `ACT-QLT-010`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-QLT-023` | `ACT-QLT-024`; `ACT-QLT-025`; `ACT-QLT-026`; `ACT-FIN-023`; `ACT-DIG-008`; `ACT-LEG-020` | `ACT-LEG-013`; `ACT-EDU-002`; `ACT-DIG-005`; `ACT-DIG-007` |
| `BS-007-AP-013` | `ACT-QLT-013`; `ACT-QLT-010`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-QLT-023`; `ACT-FIN-002`; `ACT-FIN-023` | `ACT-QLT-024`; `ACT-QLT-025`; `ACT-QLT-026`; `ACT-DIG-008`; `ACT-COM-026`; `ACT-FIN-022`; `ACT-LEG-020` | `ACT-LEG-013`; `ACT-EDU-002`; `ACT-DIG-005`; `ACT-DIG-007`; `ACT-FIN-024`; `ACT-FIN-025` |
| `BS-007-AP-014` | `ACT-QLT-013`; `ACT-QLT-010`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-QLT-023` | `ACT-QLT-024`; `ACT-QLT-025`; `ACT-QLT-026`; `ACT-FIN-023`; `ACT-DIG-008` | `ACT-LEG-013`; `ACT-EDU-002`; `ACT-DIG-005`; `ACT-DIG-007` |
| `BS-007-AP-015` | `ACT-QLT-013`; `ACT-QLT-010`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-QLT-023`; `ACT-FIN-002`; `ACT-FIN-023` | `ACT-QLT-024`; `ACT-QLT-025`; `ACT-QLT-026`; `ACT-DIG-008`; `ACT-COM-026`; `ACT-FIN-022` | `ACT-LEG-013`; `ACT-EDU-002`; `ACT-DIG-005`; `ACT-DIG-007`; `ACT-FIN-024`; `ACT-FIN-025` |
| `BS-007-AP-016` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-FIN-002`; `ACT-FIN-023` | `ACT-FIN-006`; `ACT-DIG-005`; `ACT-QLT-023`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-QLT-010`; `ACT-COM-026`; `ACT-FIN-022` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-010`; `ACT-DIG-013`; `ACT-FIN-024`; `ACT-FIN-025` |
| `BS-007-AP-017` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-FIN-006`; `ACT-FIN-031` | `ACT-DIG-005`; `ACT-QLT-023`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-QLT-010`; `ACT-OPS-018` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-010`; `ACT-DIG-013`; `ACT-FIN-007`; `ACT-FIN-009` |
| `BS-007-AP-018` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005` | `ACT-FIN-006`; `ACT-DIG-005`; `ACT-QLT-023`; `ACT-DIG-007`; `ACT-OPS-017` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-010`; `ACT-DIG-013` |
| `BS-007-AP-019` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-FIN-016`; `ACT-FIN-022` | `ACT-FIN-006`; `ACT-DIG-005`; `ACT-QLT-023`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-FIN-021`; `ACT-FIN-019`; `ACT-QLT-010` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-010`; `ACT-DIG-013`; `ACT-FIN-018`; `ACT-PRF-021` |
| `BS-007-AP-020` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-QLT-010`; `ACT-QLT-013` | `ACT-FIN-006`; `ACT-DIG-005`; `ACT-QLT-023`; `ACT-DIG-007`; `ACT-OPS-017`; `ACT-QLT-005`; `ACT-QLT-021`; `ACT-LEG-020` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-010`; `ACT-DIG-013`; `ACT-EDU-002`; `ACT-LEG-013` |

## 3. Domain assignments

### 3.1 Banking and financing

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-BNK-001` | Islamic Banking | `BS-007-AP-001` |
| `FIN-BNK-002` | Retail Banking | `BS-007-AP-001` |
| `FIN-BNK-003` | Corporate Banking | `BS-007-AP-001` |
| `FIN-BNK-004` | Commercial Banking | `BS-007-AP-001` |
| `FIN-BNK-005` | SME Banking | `BS-007-AP-001` |
| `FIN-BNK-006` | Microfinance | `BS-007-AP-001` |
| `FIN-BNK-007` | Islamic Microfinance | `BS-007-AP-001` |
| `FIN-BNK-008` | Development Finance | `BS-007-AP-001` |
| `FIN-BNK-009` | Trade Finance | `BS-007-AP-001` |
| `FIN-BNK-010` | Project Finance | `BS-007-AP-001` |
| `FIN-BNK-011` | Consumer Finance | `BS-007-AP-001` |
| `FIN-BNK-012` | Asset Finance | `BS-007-AP-001` |
| `FIN-BNK-013` | Ijarah and Leasing | `BS-007-AP-001` |
| `FIN-BNK-014` | Housing Finance | `BS-007-AP-001` |
| `FIN-BNK-015` | Agricultural Finance | `BS-007-AP-001` |
| `FIN-BNK-016` | Supply-Chain Finance | `BS-007-AP-001` |
| `FIN-BNK-017` | Factoring and Receivables Finance | `BS-007-AP-001` |

### 3.2 Payments and money movement

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-PAY-001` | Payment Gateways | `BS-007-AP-002` |
| `FIN-PAY-002` | Digital Wallets | `BS-007-AP-002` |
| `FIN-PAY-003` | Merchant Acquiring | `BS-007-AP-003` |
| `FIN-PAY-004` | Point-of-Sale Payments | `BS-007-AP-002` |
| `FIN-PAY-005` | Mobile Payments | `BS-007-AP-002` |
| `FIN-PAY-006` | Bank Transfers | `BS-007-AP-004` |
| `FIN-PAY-007` | Real-Time Payments | `BS-007-AP-002` |
| `FIN-PAY-008` | Remittances | `BS-007-AP-002` |
| `FIN-PAY-009` | Currency Exchange | `BS-007-AP-002` |
| `FIN-PAY-010` | Cross-Border Payments | `BS-007-AP-002` |
| `FIN-PAY-011` | Payment Aggregation | `BS-007-AP-002` |
| `FIN-PAY-012` | Bill Payment Services | `BS-007-AP-002` |
| `FIN-PAY-013` | Payroll Disbursement | `BS-007-AP-003` |
| `FIN-PAY-014` | Government Payment Services | `BS-007-AP-002` |
| `FIN-PAY-015` | Payment Fraud Prevention | `BS-007-AP-002` |

### 3.3 Investment and capital markets

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-INV-001` | Islamic Investment Management | `BS-007-AP-005` |
| `FIN-INV-002` | Asset Management | `BS-007-AP-005` |
| `FIN-INV-003` | Mutual Funds | `BS-007-AP-005` |
| `FIN-INV-004` | Pension Funds | `BS-007-AP-005` |
| `FIN-INV-005` | Private Equity | `BS-007-AP-005` |
| `FIN-INV-006` | Venture Capital | `BS-007-AP-005` |
| `FIN-INV-007` | Real Estate Investment | `BS-007-AP-005` |
| `FIN-INV-008` | Sukuk | `BS-007-AP-005` |
| `FIN-INV-009` | Equity Brokerage | `BS-007-AP-005` |
| `FIN-INV-010` | Commodity Brokerage | `BS-007-AP-005` |
| `FIN-INV-011` | Capital Markets Advisory | `BS-007-AP-005` |
| `FIN-INV-012` | Wealth Management | `BS-007-AP-005` |
| `FIN-INV-013` | Portfolio Management | `BS-007-AP-005` |
| `FIN-INV-014` | Custody Services | `BS-007-AP-005` |
| `FIN-INV-015` | Fund Administration | `BS-007-AP-005` |
| `FIN-INV-016` | Investment Research | `BS-007-AP-006` |

### 3.4 Takaful and protection

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-TAK-001` | Family Takaful | `BS-007-AP-007` |
| `FIN-TAK-002` | General Takaful | `BS-007-AP-007` |
| `FIN-TAK-003` | Health Takaful | `BS-007-AP-007` |
| `FIN-TAK-004` | Motor Takaful | `BS-007-AP-007` |
| `FIN-TAK-005` | Property Takaful | `BS-007-AP-007` |
| `FIN-TAK-006` | Marine Takaful | `BS-007-AP-007` |
| `FIN-TAK-007` | Agricultural Takaful | `BS-007-AP-007` |
| `FIN-TAK-008` | Microtakaful | `BS-007-AP-007` |
| `FIN-TAK-009` | Takaful Brokerage | `BS-007-AP-007` |
| `FIN-TAK-010` | Takaful Claims Administration | `BS-007-AP-007` |
| `FIN-TAK-011` | Takaful Distribution | `BS-007-AP-008` |
| `FIN-TAK-012` | Risk Survey and Assessment | `BS-007-AP-007` |

### 3.5 Accounting, audit and tax

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-ACC-001` | Accounting Services | `BS-007-AP-009` |
| `FIN-ACC-002` | Bookkeeping | `BS-007-AP-009` |
| `FIN-ACC-003` | Financial Reporting | `BS-007-AP-010` |
| `FIN-ACC-004` | Management Accounting | `BS-007-AP-009` |
| `FIN-ACC-005` | External Audit | `BS-007-AP-009` |
| `FIN-ACC-006` | Internal Audit | `BS-007-AP-009` |
| `FIN-ACC-007` | Forensic Accounting | `BS-007-AP-009` |
| `FIN-ACC-008` | Tax Advisory | `BS-007-AP-009` |
| `FIN-ACC-009` | Tax Compliance | `BS-007-AP-011` |
| `FIN-ACC-010` | Payroll Accounting | `BS-007-AP-009` |
| `FIN-ACC-011` | Cost Accounting | `BS-007-AP-009` |
| `FIN-ACC-012` | Treasury Operations | `BS-007-AP-009` |
| `FIN-ACC-013` | Accounts Payable Services | `BS-007-AP-009` |
| `FIN-ACC-014` | Accounts Receivable Services | `BS-007-AP-009` |
| `FIN-ACC-015` | Revenue Assurance | `BS-007-AP-009` |
| `FIN-ACC-016` | Financial Controls | `BS-007-AP-010` |

### 3.6 Risk, compliance and governance

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-RISK-001` | Shariah Governance | `BS-007-AP-012` |
| `FIN-RISK-002` | Financial Crime Compliance | `BS-007-AP-013` |
| `FIN-RISK-003` | Anti-Money-Laundering | `BS-007-AP-014` |
| `FIN-RISK-004` | Know Your Customer | `BS-007-AP-014` |
| `FIN-RISK-005` | Sanctions Screening | `BS-007-AP-014` |
| `FIN-RISK-006` | Credit Risk Management | `BS-007-AP-015` |
| `FIN-RISK-007` | Market Risk Management | `BS-007-AP-014` |
| `FIN-RISK-008` | Operational Risk Management | `BS-007-AP-014` |
| `FIN-RISK-009` | Enterprise Risk Management | `BS-007-AP-014` |
| `FIN-RISK-010` | Fraud Detection | `BS-007-AP-014` |
| `FIN-RISK-011` | Regulatory Reporting | `BS-007-AP-012` |
| `FIN-RISK-012` | Capital and Liquidity Management | `BS-007-AP-014` |
| `FIN-RISK-013` | Model Risk Management | `BS-007-AP-014` |
| `FIN-RISK-014` | Governance, Risk and Compliance | `BS-007-AP-012` |
| `FIN-RISK-015` | Financial Due Diligence | `BS-007-AP-015` |

### 3.7 Financial technology and operations systems

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `FIN-DIG-001` | Core Banking Systems | `BS-007-AP-016` |
| `FIN-DIG-002` | Islamic Banking Systems | `BS-007-AP-016` |
| `FIN-DIG-003` | Loan and Financing Origination | `BS-007-AP-016` |
| `FIN-DIG-004` | Financing Management Systems | `BS-007-AP-016` |
| `FIN-DIG-005` | Payment Processing Platforms | `BS-007-AP-017` |
| `FIN-DIG-006` | Digital Banking Platforms | `BS-007-AP-016` |
| `FIN-DIG-007` | Treasury Management Systems | `BS-007-AP-018` |
| `FIN-DIG-008` | Accounting Software | `BS-007-AP-019` |
| `FIN-DIG-009` | Enterprise Resource Planning for Finance | `BS-007-AP-016` |
| `FIN-DIG-010` | Billing and Invoicing Systems | `BS-007-AP-018` |
| `FIN-DIG-011` | Collection Management Systems | `BS-007-AP-018` |
| `FIN-DIG-012` | Reconciliation Systems | `BS-007-AP-018` |
| `FIN-DIG-013` | Regulatory Reporting Systems | `BS-007-AP-020` |
| `FIN-DIG-014` | Risk Analytics | `BS-007-AP-018` |
| `FIN-DIG-015` | Fraud Management Systems | `BS-007-AP-018` |
| `FIN-DIG-016` | Customer Onboarding and eKYC | `BS-007-AP-018` |
| `FIN-DIG-017` | Finance Data and Analytics | `BS-007-AP-016` |
| `FIN-DIG-018` | Open Banking and API Platforms | `BS-007-AP-016` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
