# AI Model Gateway and Evaluation

Status: **Normative planned architecture**  
Version: **1.0**  
Date: **6 August 2026**  
Implementation status: **Planned; current direct OpenAI-compatible research calls remain partial**

## 1. Purpose

This document defines the only approved runtime path for model-assisted work in Harvester.

AI may assist research, extraction, classification, synthesis, drafting, and prioritization. It does not own identity, permissions, source rights, consent, suppression, deletion, retention, billing, audit, or final high-impact decisions.

## 2. Deterministic boundary

The following remain deterministic and policy-controlled:

- authentication and session security;
- authorization and tenant isolation;
- source-policy execution gates;
- credential access;
- exact identifiers;
- retention and deletion;
- consent and suppression;
- billing and quota enforcement;
- workflow state transitions;
- export and publication authority;
- evidence and audit creation;
- cryptography and signing;
- legal-basis and terms approval.

A model output cannot override these controls.

## 3. Appropriate AI tasks

Initial task classes:

```text
DOCUMENT_CLASSIFICATION
STRUCTURED_EXTRACTION
ENTITY_MATCH_RECOMMENDATION
TAXONOMY_MAPPING_RECOMMENDATION
ROLE_NORMALIZATION
SIGNAL_CLASSIFICATION
PAIN_AND_NEED_EXTRACTION
MARKET_SYNTHESIS
COMPETITOR_SUMMARY
ACCOUNT_DOSSIER_DRAFT
REPORT_DRAFT
TRANSLATION
MESSAGE_ANALYSIS
OUTREACH_DRAFT
CREATIVE_ANALYSIS
QUALITY_REVIEW
CONTRADICTION_DISCOVERY
```

Each task has a separate contract, evidence requirement, data-class policy, output schema, evaluation set, cost ceiling, and human-review rule.

## 4. AI task contract

```text
AITaskDefinition

id
stable_code
version
purpose
allowed_data_classes
forbidden_data_classes
required_evidence_types
input_schema
output_schema
confidence_dimensions
preferred_model_classes
fallback_policy
maximum_cost
maximum_latency
human_review_policy
retention_policy
status
```

Activated task definitions are immutable.

## 5. Provider registry

```text
AIProvider

id
stable_code
provider_type
api_base_reference
commercial_status
supported_regions
data_processing_terms_reference
retention_summary
training_use_summary
security_review_state
status
verified_at
```

Initial provider families may include OpenAI, Anthropic, xAI, Perplexity, approved self-hosted models, and isolated agent runtimes.

Provider availability does not imply approval for every tenant, data class, region, or task.

## 6. Model registry

```text
AIModelVersion

id
provider_id
provider_model_id
capabilities
context_limit
structured_output_support
tool_support
vision_support
input_price_reference
output_price_reference
cached_input_price_reference
region_support
release_date
deprecation_date
verified_at
status
```

Prices, limits, and availability are live registry data. They are not permanent application constants.

## 7. Routing policy

```text
AIRoutingPolicyVersion

id
tenant_id
workspace_id
task_definition_id
allowed_models
preferred_order
quality_threshold
cost_ceiling
latency_ceiling
region_requirement
fallback_behavior
human_review_policy
status
```

Routing considers:

- task capability;
- allowed data classes;
- tenant and client policy;
- region and processing terms;
- evidence requirements;
- quality and evaluation results;
- latency;
- cost;
- provider health;
- context size;
- structured-output reliability.

## 8. Execution sequence

```text
Feature request
→ resolve AI task definition
→ classify input data
→ tenant and client policy check
→ source-rights and purpose check
→ redact or tokenize restricted values
→ select provider and model
→ enforce cost and latency limits
→ execute through gateway
→ validate structured output
→ verify evidence references
→ run task-specific quality checks
→ apply human-review policy
→ persist execution, output, cost, and evaluation
```

No application module calls a provider SDK directly after the gateway is introduced.

## 9. Execution record

```text
AIExecution

id
tenant_id
workspace_id
task_definition_version
routing_policy_version
provider_id
model_version_id
prompt_version_id
input_reference
redaction_manifest
started_at
completed_at
status
input_tokens
cached_input_tokens
output_tokens
searches
provider_cost
internal_cost_allocation
latency_ms
error_class
```

Prompt and response bodies follow task and data retention policy. Sensitive data is not copied into general logs.

## 10. Prompt registry

```text
PromptVersion

id
task_definition_id
version
system_instruction
template
required_variables
output_schema_version
created_by
approved_by
activated_at
retired_at
```

Prompt changes are versioned, reviewed, benchmarked, and rollback-capable.

## 11. Structured output

Model output must validate against a task-owned schema before it reaches business logic.

Invalid output is:

- rejected;
- retried according to policy;
- routed to a fallback model when permitted;
- or sent to review.

It must not be converted into silent defaults and marked successful.

## 12. Evidence grounding

Evidence-grounded tasks require outputs to reference exact Harvester evidence identifiers.

The gateway validates:

- referenced evidence exists;
- the tenant and workspace may access it;
- the evidence supports the output type;
- excerpts and locators are available where required;
- the model did not cite unrelated or inaccessible evidence.

A model-generated sentence without supporting evidence remains an inference or draft, not a fact.

## 13. Confidence

Harvester does not assign one decorative confidence percentage to all model outputs.

Relevant dimensions may include:

```text
source_authority
extraction_certainty
identity_confidence
corroboration
freshness
coverage
task_evaluation_score
model_agreement
review_state
```

Model self-confidence is not accepted as calibrated evidence confidence.

## 14. Human review

Mandatory review applies to:

- ambiguous entity resolution;
- regulated healthcare or education use;
- person-level enrichment and attribution;
- high-value or high-risk opportunity recommendations;
- campaign audience publication;
- automated outreach preparation where customer policy requires it;
- competitor allegations;
- material client-facing claims;
- model disagreement above the approved threshold;
- policy exceptions and overrides.

Review decisions record evidence, model and prompt versions, rationale, actor, and timestamp.

## 15. Evaluation datasets

```text
AIEvaluationDataset

id
task_definition_id
version
sector_pack_version
locale_pack_version
cases
sensitivity_classification
created_at
approved_at
```

Cases include:

- known positive;
- known negative;
- ambiguous;
- contradictory;
- stale;
- incomplete coverage;
- duplicate origin;
- locale and transliteration variants;
- prompt-injection content;
- sensitive-sector edge cases;
- source mismatch;
- malformed provider responses.

## 16. Evaluation metrics

Task-specific metrics may include:

- precision and recall;
- schema-valid output rate;
- evidence faithfulness;
- unsupported-claim rate;
- citation correctness;
- entity-match accuracy;
- classification accuracy;
- human override rate;
- policy violation rate;
- cost per accepted result;
- latency;
- provider failure rate;
- drift from approved baseline.

## 17. Release and drift

A model or prompt version cannot become active solely because it is newer.

Release follows:

```text
candidate
→ offline evaluation
→ security and policy review
→ shadow execution
→ bounded tenant rollout
→ metric comparison
→ approval
→ active version
```

Drift or provider changes may pause the model and restore the last approved version.

## 18. Cost governance

Every AI execution is attributed to tenant, workspace, client, project, task, model, provider, and output.

Controls include:

- per-run budget;
- per-project budget;
- per-tenant budget;
- maximum cost per accepted entity;
- maximum cost per qualified opportunity;
- batch processing;
- caching;
- duplicate-request prevention;
- low-cost routing;
- circuit breakers;
- approval above thresholds.

## 19. Provider-specific roles

Provider roles are policies, not hard-coded assumptions.

Examples:

- reasoning and structured extraction;
- long-document review;
- web-grounded research;
- social or current-context analysis where licensed access permits;
- local or customer-controlled processing;
- model comparison and quality review.

## 20. Agent runtime boundary

Agent runtimes such as OpenClaw are execution tools, not shared multi-tenant security boundaries.

They may be used only:

- inside a tenant-isolated worker or cell;
- with bounded tools and credentials;
- through the same task, policy, evidence, cost, and audit controls;
- without persistent cross-tenant memory;
- without authority to publish, contact, delete, or change policy unless an explicit deterministic workflow grants that action.

## 21. Prompt injection and hostile content

External content is untrusted input.

Controls include:

- separation of instructions and evidence;
- tool allowlists;
- URL and file validation;
- no secret exposure to content-processing tasks;
- output-schema enforcement;
- evidence-reference validation;
- suspicious-instruction detection;
- sandboxing for document and browser tasks;
- human review for high-impact outputs.

## 22. Migration from current ResearchBrain

1. Register the existing LinkedIn-profile analysis as a restricted legacy task.
2. Remove direct provider construction from business modules.
3. Introduce gateway, task, provider, model, prompt, routing, execution, and cost records.
4. Replace uniform confidence values with dimensioned evidence and model metadata.
5. Separate factual extractions, inferences, draft outreach, and opportunity recommendations.
6. Disable the task unless its source acquisition path is independently approved.
7. Backfill existing findings with legacy prompt and model metadata where reconstructable.
8. Mark unreconstructable model executions as legacy and non-reproducible.

## 23. Required tests

Tests must prove:

1. forbidden data classes cannot reach a provider;
2. tenant policy controls model eligibility;
3. invalid structured output is never marked successful;
4. evidence-grounded outputs cannot cite inaccessible or unrelated records;
5. provider failure respects retry, fallback, and cost policy;
6. model changes do not activate without evaluation and approval;
7. direct provider SDK use outside the gateway is rejected by architecture checks;
8. agent tools cannot cross tenant or action boundaries;
9. sensitive content does not enter general logs;
10. every accepted output remains attributable to task, prompt, model, provider, evidence, and cost.

## 24. Locked rule

> AI may accelerate interpretation and drafting. Harvester's evidence, policy, deterministic controls, and accountable people decide what becomes operational truth or action.
