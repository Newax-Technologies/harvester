# Harvester Energy Domain–Activity Applicability Mapping

Status: **Proposed**  
Version: **1.0**  
Date: **3 August 2026**  
Implementation status: **Not implemented**

This file explicitly maps all **94** canonical domains in `BS-013 Energy` to domain-specific activity profiles. Activity codes resolve to the [Canonical Business Activity Registry](../activity-registry.md).

## 1. Locked behaviour

- Every domain has one explicit default activity profile.
- Activity profiles are reusable definitions, but selecting an activity for one domain never activates it for another domain.
- `CORE`, `COMMON`, and `OPTIONAL` are presentation defaults, not evidence that a target performs the activity.
- Activities absent from a profile are `NOT_APPLICABLE` by default.
- Users approve every domain–activity combination before provider-service eligibility, evidence assessment, opportunity scoring, or lead generation.

## 2. Activity profiles

| Profile | Core activity codes | Common activity codes | Optional activity codes |
| --- | --- | --- | --- |
| `BS-013-AP-001` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004` |
| `BS-013-AP-002` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-RND-009`; `ACT-OPS-001` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008`; `ACT-PUB-007` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004`; `ACT-PRD-016`; `ACT-COM-012`; `ACT-DIG-009` |
| `BS-013-AP-003` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-RND-009`; `ACT-OPS-001` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004`; `ACT-PRD-016`; `ACT-COM-012` |
| `BS-013-AP-004` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-OPS-010` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008`; `ACT-PUB-007` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004`; `ACT-DIG-009` |
| `BS-013-AP-005` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-END-001`; `ACT-END-002` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008`; `ACT-END-008`; `ACT-END-012` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004`; `ACT-END-004`; `ACT-END-005` |
| `BS-013-AP-006` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-PRD-016`; `ACT-QLT-001` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008`; `ACT-LOG-001`; `ACT-COM-001` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004`; `ACT-SRC-008`; `ACT-OPS-013` |
| `BS-013-AP-007` | `ACT-OPS-008`; `ACT-OPS-009`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-COM-001`; `ACT-COM-002` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-QLT-002`; `ACT-QLT-015`; `ACT-DIG-008`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-OPS-027`; `ACT-OPS-022`; `ACT-COM-004`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-013-AP-008` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-OPS-001`; `ACT-OPS-002`; `ACT-OPS-012` | `ACT-PRD-016`; `ACT-SRC-014`; `ACT-OPS-011`; `ACT-OPS-017`; `ACT-COM-004` | `ACT-FIN-002`; `ACT-COM-012`; `ACT-END-006` |
| `BS-013-AP-009` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-OPS-001`; `ACT-OPS-002`; `ACT-OPS-012`; `ACT-OPS-010`; `ACT-OPS-011` | `ACT-PRD-016`; `ACT-SRC-014`; `ACT-OPS-017`; `ACT-COM-004`; `ACT-QLT-014`; `ACT-PUB-007` | `ACT-FIN-002`; `ACT-COM-012`; `ACT-END-006`; `ACT-OPS-027`; `ACT-DIG-009` |
| `BS-013-AP-010` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-OPS-001`; `ACT-OPS-002`; `ACT-OPS-012`; `ACT-OPS-014`; `ACT-OPS-015` | `ACT-PRD-016`; `ACT-SRC-014`; `ACT-OPS-011`; `ACT-OPS-017`; `ACT-COM-004`; `ACT-SRC-015` | `ACT-FIN-002`; `ACT-COM-012`; `ACT-END-006`; `ACT-OPS-019`; `ACT-OPS-013` |
| `BS-013-AP-011` | `ACT-RND-009`; `ACT-PRF-024`; `ACT-OPS-001`; `ACT-OPS-002`; `ACT-OPS-012`; `ACT-LOG-001`; `ACT-LOG-003` | `ACT-PRD-016`; `ACT-SRC-014`; `ACT-OPS-011`; `ACT-OPS-017`; `ACT-COM-004`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024` | `ACT-FIN-002`; `ACT-COM-012`; `ACT-END-006`; `ACT-DIG-009`; `ACT-LOG-027` |
| `BS-013-AP-012` | `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-LOG-023`; `ACT-QLT-014` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-OPS-024`; `ACT-QLT-021`; `ACT-PUB-007` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034` |
| `BS-013-AP-013` | `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-LOG-023`; `ACT-QLT-014`; `ACT-COM-001`; `ACT-COM-002` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-OPS-024`; `ACT-QLT-021`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016`; `ACT-PUB-007` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-013-AP-014` | `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-LOG-023`; `ACT-QLT-014` | `ACT-PRF-024`; `ACT-OPS-002`; `ACT-OPS-024`; `ACT-QLT-021` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034` |
| `BS-013-AP-015` | `ACT-PRD-006`; `ACT-PRD-009`; `ACT-PRD-008`; `ACT-LOG-013`; `ACT-COM-001`; `ACT-OPS-010`; `ACT-OPS-011` | `ACT-LOG-001`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-004`; `ACT-OPS-012`; `ACT-PUB-007` | `ACT-SRC-008`; `ACT-END-009`; `ACT-OPS-022`; `ACT-OPS-027`; `ACT-DIG-009` |
| `BS-013-AP-016` | `ACT-PRD-006`; `ACT-PRD-009`; `ACT-PRD-008`; `ACT-LOG-013`; `ACT-COM-001` | `ACT-LOG-001`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-004` | `ACT-SRC-008`; `ACT-END-009`; `ACT-OPS-022` |
| `BS-013-AP-017` | `ACT-PRD-006`; `ACT-PRD-009`; `ACT-PRD-008`; `ACT-LOG-013`; `ACT-COM-001`; `ACT-COM-002` | `ACT-LOG-001`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-004`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-SRC-008`; `ACT-END-009`; `ACT-OPS-022`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-013-AP-018` | `ACT-PRD-006`; `ACT-PRD-009`; `ACT-PRD-008`; `ACT-LOG-013`; `ACT-COM-001`; `ACT-COM-002`; `ACT-OPS-010` | `ACT-LOG-001`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-004`; `ACT-LOG-006`; `ACT-COM-016`; `ACT-OPS-012`; `ACT-PUB-007` | `ACT-SRC-008`; `ACT-END-009`; `ACT-OPS-022`; `ACT-LOG-002`; `ACT-COM-017`; `ACT-OPS-027` |
| `BS-013-AP-019` | `ACT-PRD-006`; `ACT-PRD-009`; `ACT-PRD-008`; `ACT-LOG-013`; `ACT-COM-001`; `ACT-RND-001`; `ACT-RND-007` | `ACT-LOG-001`; `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-004`; `ACT-DIG-007`; `ACT-DIG-008`; `ACT-EDU-014`; `ACT-OPS-012` | `ACT-SRC-008`; `ACT-END-009`; `ACT-OPS-022`; `ACT-PRF-001`; `ACT-RND-006`; `ACT-OPS-027` |
| `BS-013-AP-020` | `ACT-PRD-006`; `ACT-PRD-009`; `ACT-PRD-008`; `ACT-LOG-013`; `ACT-COM-001`; `ACT-LOG-001`; `ACT-LOG-003` | `ACT-QLT-014`; `ACT-QLT-015`; `ACT-COM-004`; `ACT-LOG-005`; `ACT-LOG-007`; `ACT-LOG-024` | `ACT-SRC-008`; `ACT-END-009`; `ACT-OPS-022`; `ACT-DIG-009`; `ACT-LOG-027` |
| `BS-013-AP-021` | `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-PUB-007` | `ACT-PRD-008`; `ACT-QLT-001`; `ACT-QLT-015`; `ACT-FIN-029`; `ACT-QLT-014` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034` |
| `BS-013-AP-022` | `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-PUB-007`; `ACT-END-001`; `ACT-END-002` | `ACT-PRD-008`; `ACT-QLT-001`; `ACT-QLT-015`; `ACT-FIN-029`; `ACT-END-008`; `ACT-END-012`; `ACT-QLT-014` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034`; `ACT-END-004`; `ACT-END-005` |
| `BS-013-AP-023` | `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-PUB-007` | `ACT-PRD-008`; `ACT-QLT-001`; `ACT-QLT-015`; `ACT-FIN-029` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034` |
| `BS-013-AP-024` | `ACT-OPS-008`; `ACT-OPS-010`; `ACT-OPS-011`; `ACT-OPS-012`; `ACT-PUB-007`; `ACT-COM-001`; `ACT-COM-002` | `ACT-PRD-008`; `ACT-QLT-001`; `ACT-QLT-015`; `ACT-FIN-029`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016`; `ACT-QLT-014` | `ACT-OPS-027`; `ACT-DIG-009`; `ACT-OPS-034`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-013-AP-025` | `ACT-PRF-003`; `ACT-PRF-001`; `ACT-RND-009`; `ACT-OPS-004`; `ACT-OPS-011` | `ACT-QLT-005`; `ACT-PRF-024`; `ACT-OPS-026`; `ACT-DIG-008` | `ACT-FIN-002`; `ACT-EDU-002`; `ACT-DIG-009` |
| `BS-013-AP-026` | `ACT-PRF-003`; `ACT-PRF-001`; `ACT-RND-009`; `ACT-OPS-004`; `ACT-OPS-011`; `ACT-RND-001`; `ACT-RND-007` | `ACT-QLT-005`; `ACT-PRF-024`; `ACT-OPS-026`; `ACT-DIG-008`; `ACT-DIG-007`; `ACT-EDU-014` | `ACT-FIN-002`; `ACT-EDU-002`; `ACT-DIG-009`; `ACT-RND-006` |
| `BS-013-AP-027` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005` | `ACT-OPS-011`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-010` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-022` |
| `BS-013-AP-028` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-COM-001`; `ACT-COM-002` | `ACT-OPS-011`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-010`; `ACT-LOG-001`; `ACT-LOG-006`; `ACT-COM-016` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-022`; `ACT-LOG-002`; `ACT-COM-017` |
| `BS-013-AP-029` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-OPS-010`; `ACT-OPS-011` | `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-010`; `ACT-OPS-012`; `ACT-QLT-014`; `ACT-PUB-007` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-022`; `ACT-OPS-027` |
| `BS-013-AP-030` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-OPS-012`; `ACT-OPS-014` | `ACT-OPS-011`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-010`; `ACT-SRC-015` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-022`; `ACT-OPS-019`; `ACT-OPS-013` |
| `BS-013-AP-031` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-PRD-016`; `ACT-QLT-001` | `ACT-OPS-011`; `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-DIG-010`; `ACT-LOG-001`; `ACT-COM-001` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-022`; `ACT-SRC-008`; `ACT-OPS-013` |
| `BS-013-AP-032` | `ACT-RND-018`; `ACT-DIG-001`; `ACT-DIG-002`; `ACT-OPS-004`; `ACT-OPS-005`; `ACT-DIG-010`; `ACT-QLT-013` | `ACT-DIG-007`; `ACT-DIG-009`; `ACT-OPS-017`; `ACT-QLT-005`; `ACT-DIG-011`; `ACT-QLT-022`; `ACT-OPS-012`; `ACT-QLT-014` | `ACT-OPS-007`; `ACT-DIG-003`; `ACT-DIG-022`; `ACT-PRF-022`; `ACT-EDU-002`; `ACT-OPS-027` |

## 3. Domain assignments

### 3.1 Power generation

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-GEN-001` | Thermal Power Generation | `BS-013-AP-001` |
| `ENE-GEN-002` | Hydroelectric Power | `BS-013-AP-002` |
| `ENE-GEN-003` | Solar Power Generation | `BS-013-AP-003` |
| `ENE-GEN-004` | Wind Power Generation | `BS-013-AP-003` |
| `ENE-GEN-005` | Biomass and Biogas Power | `BS-013-AP-004` |
| `ENE-GEN-006` | Waste-to-Energy | `BS-013-AP-005` |
| `ENE-GEN-007` | Cogeneration and Combined Heat and Power | `BS-013-AP-001` |
| `ENE-GEN-008` | Captive Power Plants | `BS-013-AP-006` |
| `ENE-GEN-009` | Distributed Generation | `BS-013-AP-007` |
| `ENE-GEN-010` | Microgrids | `BS-013-AP-004` |
| `ENE-GEN-011` | Backup and Emergency Power | `BS-013-AP-001` |
| `ENE-GEN-012` | Independent Power Producers | `BS-013-AP-001` |

### 3.2 Renewable-energy products and services

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-REN-001` | Solar Panels | `BS-013-AP-008` |
| `ENE-REN-002` | Solar Inverters | `BS-013-AP-008` |
| `ENE-REN-003` | Solar Batteries | `BS-013-AP-008` |
| `ENE-REN-004` | Solar Mounting Systems | `BS-013-AP-008` |
| `ENE-REN-005` | Solar Water Heating | `BS-013-AP-009` |
| `ENE-REN-006` | Wind Turbines | `BS-013-AP-008` |
| `ENE-REN-007` | Small Hydro Systems | `BS-013-AP-008` |
| `ENE-REN-008` | Biogas Systems | `BS-013-AP-009` |
| `ENE-REN-009` | Renewable-Energy Engineering | `BS-013-AP-008` |
| `ENE-REN-010` | Solar EPC Services | `BS-013-AP-008` |
| `ENE-REN-011` | Renewable-Energy Operations and Maintenance | `BS-013-AP-010` |
| `ENE-REN-012` | Energy Storage Systems | `BS-013-AP-011` |
| `ENE-REN-013` | Electric Vehicle Charging | `BS-013-AP-009` |
| `ENE-REN-014` | Renewable-Energy Financing | `BS-013-AP-008` |

### 3.3 Electricity networks and utility operations

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-GRD-001` | Electricity Transmission | `BS-013-AP-012` |
| `ENE-GRD-002` | Electricity Distribution | `BS-013-AP-013` |
| `ENE-GRD-003` | Grid Operations | `BS-013-AP-012` |
| `ENE-GRD-004` | Substations | `BS-013-AP-014` |
| `ENE-GRD-005` | Smart Grid Systems | `BS-013-AP-012` |
| `ENE-GRD-006` | Metering and Smart Meters | `BS-013-AP-014` |
| `ENE-GRD-007` | Utility Billing | `BS-013-AP-012` |
| `ENE-GRD-008` | Outage Management | `BS-013-AP-014` |
| `ENE-GRD-009` | Demand-Side Management | `BS-013-AP-014` |
| `ENE-GRD-010` | Power Quality Management | `BS-013-AP-014` |
| `ENE-GRD-011` | Grid Protection and Control | `BS-013-AP-012` |
| `ENE-GRD-012` | Rural Electrification | `BS-013-AP-014` |
| `ENE-GRD-013` | Utility Customer Services | `BS-013-AP-012` |

### 3.4 Fuel, petroleum and gas

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-FUE-001` | Oil and Gas Exploration | `BS-013-AP-015` |
| `ENE-FUE-002` | Oil and Gas Production | `BS-013-AP-015` |
| `ENE-FUE-003` | Petroleum Refining | `BS-013-AP-016` |
| `ENE-FUE-004` | Fuel Distribution | `BS-013-AP-017` |
| `ENE-FUE-005` | Fuel Retail Stations | `BS-013-AP-016` |
| `ENE-FUE-006` | LPG Distribution | `BS-013-AP-017` |
| `ENE-FUE-007` | Natural Gas Transmission | `BS-013-AP-015` |
| `ENE-FUE-008` | Natural Gas Distribution | `BS-013-AP-018` |
| `ENE-FUE-009` | Industrial Gas Supply | `BS-013-AP-019` |
| `ENE-FUE-010` | Lubricants | `BS-013-AP-016` |
| `ENE-FUE-011` | Fuel Storage Terminals | `BS-013-AP-020` |
| `ENE-FUE-012` | Pipeline Operations | `BS-013-AP-016` |
| `ENE-FUE-013` | Petroleum Logistics | `BS-013-AP-016` |
| `ENE-FUE-014` | Gas Metering | `BS-013-AP-015` |

### 3.5 Water and essential utilities

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-WAT-001` | Water Supply | `BS-013-AP-021` |
| `ENE-WAT-002` | Water Treatment | `BS-013-AP-021` |
| `ENE-WAT-003` | Wastewater Treatment | `BS-013-AP-022` |
| `ENE-WAT-004` | Sewerage Operations | `BS-013-AP-023` |
| `ENE-WAT-005` | Desalination | `BS-013-AP-023` |
| `ENE-WAT-006` | Water Distribution Networks | `BS-013-AP-024` |
| `ENE-WAT-007` | Water Metering | `BS-013-AP-021` |
| `ENE-WAT-008` | Irrigation Utilities | `BS-013-AP-023` |
| `ENE-WAT-009` | District Cooling | `BS-013-AP-023` |
| `ENE-WAT-010` | District Heating | `BS-013-AP-023` |
| `ENE-WAT-011` | Utility Asset Management | `BS-013-AP-021` |
| `ENE-WAT-012` | Utility Field Services | `BS-013-AP-021` |

### 3.6 Energy services and efficiency

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-EFF-001` | Energy Audits | `BS-013-AP-025` |
| `ENE-EFF-002` | Energy Management | `BS-013-AP-025` |
| `ENE-EFF-003` | Building Energy Management | `BS-013-AP-025` |
| `ENE-EFF-004` | Industrial Energy Management | `BS-013-AP-026` |
| `ENE-EFF-005` | Energy Service Companies | `BS-013-AP-025` |
| `ENE-EFF-006` | Power-Factor Correction | `BS-013-AP-025` |
| `ENE-EFF-007` | Energy-Efficient Lighting | `BS-013-AP-025` |
| `ENE-EFF-008` | HVAC Efficiency | `BS-013-AP-025` |
| `ENE-EFF-009` | Carbon and Emissions Management | `BS-013-AP-025` |
| `ENE-EFF-010` | Sustainability Reporting | `BS-013-AP-025` |
| `ENE-EFF-011` | Energy Procurement | `BS-013-AP-025` |
| `ENE-EFF-012` | Demand Response | `BS-013-AP-025` |
| `ENE-EFF-013` | Energy Performance Contracting | `BS-013-AP-025` |

### 3.7 Energy technology and operations systems

| Domain code | Domain | Activity profile |
| --- | --- | --- |
| `ENE-DIG-001` | Energy Management Systems | `BS-013-AP-027` |
| `ENE-DIG-002` | Supervisory Control and Data Acquisition | `BS-013-AP-027` |
| `ENE-DIG-003` | Meter Data Management | `BS-013-AP-027` |
| `ENE-DIG-004` | Advanced Metering Infrastructure | `BS-013-AP-027` |
| `ENE-DIG-005` | Distributed Energy Resource Management | `BS-013-AP-028` |
| `ENE-DIG-006` | Energy Trading and Settlement | `BS-013-AP-027` |
| `ENE-DIG-007` | Utility Customer Information Systems | `BS-013-AP-029` |
| `ENE-DIG-008` | Asset Performance Management | `BS-013-AP-027` |
| `ENE-DIG-009` | Predictive Maintenance | `BS-013-AP-030` |
| `ENE-DIG-010` | Grid Analytics | `BS-013-AP-029` |
| `ENE-DIG-011` | Renewable Plant Monitoring | `BS-013-AP-031` |
| `ENE-DIG-012` | Battery Management Systems | `BS-013-AP-027` |
| `ENE-DIG-013` | Field-Service Management | `BS-013-AP-027` |
| `ENE-DIG-014` | Geographic Information Systems for Utilities | `BS-013-AP-027` |
| `ENE-DIG-015` | Energy IoT and Telemetry | `BS-013-AP-027` |
| `ENE-DIG-016` | Utility Cybersecurity | `BS-013-AP-032` |

## 4. Delivery boundary

This mapping is a controlled documentation dataset. It does not implement runtime taxonomy tables, APIs, interface controls, activity detection, evidence assessment, scoring, or releases.
