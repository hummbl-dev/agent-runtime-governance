# Programmatic Tool Calling and Multi-Agent Execution Governance — Draft v0.1

## Status

**Draft / experimental.** Not for production use. Provider-neutral governance
for model-authored programs that coordinate tool calls and parallel multi-agent
execution.

## Design principle

When intermediate orchestration is compressed or hidden from the primary
conversation, governance must be preserved. Authority, tool permissions,
evidence, cost limits, cancellation, and review must not be bypassed by
moving orchestration inside a model-authored program or a multi-agent fan-out.

---

## 1. Programmatic tool-execution contract

### 1.1 Initiating principal and authorized objective

Every generated program must declare:

- `initiating_principal`: who authorized the program
- `authorized_objective`: what the program is authorized to do
- `authority_chain`: traceable to root principal

### 1.2 Generated-program identity/hash

- `program_id`: unique identifier
- `program_hash`: cryptographic hash of the generated program
- `program_source`: which model/agent generated the program
- `program_timestamp`: when the program was generated

### 1.3 Runtime/sandbox declaration

- `runtime_type`: `in_memory` | `sandboxed` | `native`
- `sandbox_config`: isolation level, network policy, filesystem policy
- `runtime_version`: version of the runtime executing the program

### 1.4 Allowed tools and per-tool scopes

- `allowed_tools`: list of tools the program may invoke
- `per_tool_scopes`: per-tool scope restrictions
- Tools not on the allowlist are prohibited

### 1.5 Permissions

| Permission | Values |
|------------|--------|
| Network | `none` | `local_only` | `owned_endpoints` | `open` |
| Filesystem | `none` | `read` | `read_write` |
| Subprocess | `none` | `allowed_with_confirmation` |
| Code execution | `none` | `sandboxed` | `native` |

### 1.6 Input and intermediate-data boundaries

- `input_boundary`: what data the program may access
- `intermediate_data_boundary`: what intermediate data may be retained
- `output_boundary`: what data the program may output

### 1.7 Retained versus discarded intermediate results

- `retained_intermediate`: results retained for audit
- `discarded_intermediate`: results discarded (with policy reason)
- Discarded results must NOT include evidence needed for audit
- Tool-result compression must NOT become evidence deletion

### 1.8 Secret/credential prohibition

- Secrets and credentials are prohibited in generated programs by default
- Explicit gated access requires:
  - Named secret
  - Per-secret authorization
  - Audit trail of access

### 1.9 Resource limits

| Limit | Description |
|-------|-------------|
| `max_steps` | Maximum number of program steps |
| `max_duration` | Maximum wall-clock duration |
| `max_tokens` | Maximum token consumption |
| `max_cost` | Maximum monetary cost |
| `max_memory` | Maximum memory usage |
| `max_output_size` | Maximum output size |

### 1.10 Stop/cancel behavior

- Programs must be stoppable at any step
- Cancellation must be immediate
- Partial results must be marked as partial
- Cancellation produces a receipt

### 1.11 Replay posture

- `deterministic`: program can be replayed with identical results
- `best_effort`: program may produce different results on replay
- Non-deterministic programs must be marked

### 1.12 Failure and partial-result handling

- Failures produce failure receipts
- Partial results are marked as partial
- Failed required branches must NOT be silently dropped
- Programs must NOT claim completion if required branches failed

### 1.13 Validation and receipt requirements

Every program execution must produce a receipt with:
- Program identity and hash
- Initiating principal
- Tools invoked and scopes
- Intermediate decisions
- Resource consumption
- Failures and partial results
- Final output

---

## 2. Multi-agent execution contract

### 2.1 Orchestrator identity and authority

- `orchestrator_id`: unique identifier
- `orchestrator_authority`: authority chain to root principal
- `orchestrator_model`: model used by the orchestrator

### 2.2 Subagent role and objective

- `subagent_id`: unique identifier
- `subagent_role`: role in the multi-agent execution
- `subagent_objective`: what the subagent is authorized to do
- `subagent_model`: model used by the subagent

### 2.3 Inherited versus reduced permissions

- Subagents inherit orchestrator permissions by default
- Subagents may have REDUCED permissions (never expanded)
- Permission reduction must be explicit
- No subagent may have more authority than the orchestrator

### 2.4 Concurrency/fan-out limits

- `max_concurrency`: maximum parallel subagents
- `max_fan_out`: maximum total subagents spawned
- Exceeding limits produces a violation

### 2.5 Shared versus isolated context

- `context_sharing`: `shared` | `isolated` | `selective`
- Shared context: all subagents see the same context
- Isolated context: each subagent has its own context
- Selective context: specific fields are shared

### 2.6 Communication topology

- `topology`: `star` | `mesh` | `pipeline` | `tree`
- Star: orchestrator communicates with each subagent
- Mesh: subagents may communicate with each other
- Pipeline: subagents are chained
- Tree: subagents may spawn sub-subagents (within limits)

### 2.7 Source/evidence attribution per subagent

- Every subagent output must include source attribution
- Evidence must be class-marked: `[OBS]`, `[INF]`, `[SEC]`, `[GAP]`, `[VERIFIED]`
- Subagent outputs without provenance must be rejected

### 2.8 Conflict and contradiction handling

- When subagents conflict, the orchestrator must:
  1. Record the conflict
  2. Record both positions
  3. Not silently drop either position
  4. Either resolve with evidence or escalate

### 2.9 Synthesis responsibility

- The orchestrator is responsible for synthesis
- Synthesis must cite subagent outputs
- Synthesis must not introduce claims not supported by subagent evidence
- Synthesis must record uncertainty

### 2.10 Cancellation propagation

- Cancellation must propagate to all subagents
- Each subagent must receive a cancellation signal
- Subagents must produce cancellation receipts
- Partial cancellation (some but not all) must be detected

### 2.11 Timeout and straggler handling

- `subagent_timeout`: per-subagent timeout
- Stragglers (subagents that exceed timeout) must be:
  1. Marked as timed out
  2. Their partial results (if any) must be marked as partial
  3. The orchestrator must decide: wait, proceed, or fail

### 2.12 Result acceptance/rejection

- The orchestrator may accept or reject subagent results
- Rejection must include a reason
- Accepted results must include provenance
- Rejected results must be recorded (not deleted)

### 2.13 Resource accounting

- Resource consumption is tracked per subagent
- Total resource consumption is the sum of all subagents
- Resource limits apply to the total, not per subagent

### 2.14 Final human or policy gate

- High-stakes synthesis requires a human or policy gate
- The gate reviews: synthesis, conflicts, uncertainty, resource usage
- The gate may accept, reject, or request revision

---

## 3. Observability and audit

### Inspectable records

| Record | Required |
|--------|----------|
| Generated orchestration program or safe digest/reference | yes |
| Tool invocations and scopes | yes |
| Material intermediate decisions | yes |
| Discarded-data policy | yes |
| Subagent graph | yes |
| Per-agent outputs and evidence references | yes |
| Contradictions and unresolved uncertainty | yes |
| Resource consumption | yes |
| Safety/policy denials | yes |
| Final synthesis and acceptance posture | yes |

### Summarizable vs. must-remain-available

| Data | Summarizable? |
|------|--------------|
| Tool invocations | no — must remain available |
| Intermediate decisions | no — must remain available |
| Subagent outputs | summarizable with provenance link to full output |
| Resource consumption | summarizable with per-agent breakdown available |
| Contradictions | no — must remain available |
| Safety denials | no — must remain available |

Tool-result compression must NOT become evidence deletion or authority
laundering.

---

## 4. Route and economics hooks

Fields consumable by `model-routing-as-code` and `autoresearch-pipeline`:

| Field | Description |
|-------|-------------|
| `route_type` | `single_agent` | `multi_agent` |
| `subagent_count` | Number of subagents |
| `subagent_classes` | Classes of subagents |
| `reasoning_tier` | Reasoning/effort tier (provider-neutral) |
| `predicted_cost` | Predicted cost (if measurable) |
| `actual_cost` | Actual cost |
| `latency` | Wall-clock latency |
| `accepted_outcome` | Whether the outcome was accepted |
| `retry_burden` | Number of retries/rework |
| `capability_failures` | Capability and safety failures |

Provider-specific tiers (`max`, `ultra`, etc.) are NOT promoted in this
repository.

---

## 5. Threat and failure fixtures

| Fixture | Scenario |
|---------|----------|
| `undeclared-tool-call.json` | Generated program calls an undeclared tool |
| `evidence-filtering.json` | Intermediate filtering drops contradicting evidence |
| `permission-escalation.json` | Subagent attempts to escalate permissions |
| `excessive-fan-out.json` | Orchestrator spawns excessive fan-out |
| `subagent-conflict.json` | Two subagents conflict materially |
| `partial-cancellation.json` | Cancellation reaches some but not all subagents |
| `subagent-timeout.json` | One subagent times out after others complete |
| `secret-in-intermediate.json` | Secret appears in an intermediate tool result |
| `nondeterministic-mutation.json` | Generated program performs nondeterministic mutation |
| `budget-exceeded.json` | Cost or duration budget is exceeded |
| `no-provenance.json` | Subagent output is accepted without provenance |
| `false-completion.json` | Orchestrator claims completion despite failed required branch |
| `duplicate-action.json` | Parallel agents duplicate the same external action |
| `unknown-retention.json` | ZDR or retention claim is unknown or unavailable |

---

## Non-goals

- No provider-specific implementation
- No promotion of provider-specific tiers
- No live external mutations
- No new canon or merge authorization from this issue alone

## Unresolved questions

1. Should the programmatic tool-execution contract be a JSON Schema?
2. How should non-deterministic programs be handled in replay?
3. What is the minimum required observability for a single-agent program?
4. How should cross-provider multi-agent execution be represented?

## Rollback instructions

This is a specification document. Rollback = revert the commit. No runtime
impact.

## Related

- `hummbl-dev/agent-runtime-governance#12` — this issue
- `hummbl-dev/hummbl-dev#156` and `#158` — company routing plan
- `hummbl-dev/model-routing-as-code#8` and `#9` — model-routing policy
- `hummbl-dev/autoresearch-pipeline#31` — routing benchmark
- `hummbl-dev/hummbl-dev#152` — comparative runtime program
