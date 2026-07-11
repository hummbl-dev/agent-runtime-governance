# Programmatic Tool Calling and Multi-Agent Execution Governance v0.1

**Status: CANDIDATE SPEC — PROVIDER-NEUTRAL — NO LIVE EXECUTION**

Issue: hummbl-dev/agent-runtime-governance#12

## Purpose

Provider-neutral governance for:
1. Model-authored programs that coordinate tool calls and filter/process intermediate results
2. Parallel multi-agent execution where one request spawns concurrent subagents

## Programmatic tool-execution contract

See `programmatic-tool-execution.schema.json` for the JSON Schema.

Key fields:
- Initiating principal and authorized objective
- Generated-program identity/hash
- Runtime/sandbox declaration
- Allowed tools and per-tool scopes
- Network, filesystem, subprocess, code-execution, secret permissions
- Input and intermediate-data boundaries
- Retained vs discarded intermediate results
- Maximum steps, duration, tokens, cost, memory, output size
- Stop/cancel behavior
- Failure and partial-result handling
- Validation and receipt requirements

## Multi-agent execution contract

See `multi-agent-execution.schema.json` for the JSON Schema.

Key fields:
- Orchestrator identity and authority
- Subagent roles, objectives, inherited vs reduced permissions
- Concurrency/fan-out limits
- Shared vs isolated context
- Communication topology
- Source/evidence attribution per subagent
- Conflict and contradiction handling
- Cancellation propagation
- Timeout and straggler handling
- Resource accounting
- Final human or policy gate

**No subagent may gain authority merely because another agent delegated to it.**

## Evidence and observability model

Inspectable records required for:
- Generated orchestration program or safe digest/reference
- Tool invocations and scopes
- Material intermediate decisions
- Discarded-data policy enforcement
- Subagent graph
- Per-agent outputs and evidence references
- Contradictions and unresolved uncertainty
- Resource consumption
- Safety/policy denials
- Final synthesis and acceptance posture

Tool-result compression must not become evidence deletion or authority laundering.

## Route and economics hooks

Fields consumable by `model-routing-as-code` and `autoresearch-pipeline`:
- Single-agent vs multi-agent route
- Number and class of subagents
- Reasoning/effort tier
- Predicted and actual cost
- Latency
- Accepted outcome
- Retry/rework burden
- Capability and safety failures

No provider-specific tier names promoted.

## Threat and failure fixtures

1. Generated program calls an undeclared tool
2. Intermediate filtering drops evidence that contradicts the conclusion
3. Subagent attempts to escalate permissions
4. Orchestrator spawns excessive fan-out
5. Two subagents conflict materially
6. Cancellation reaches some but not all subagents
7. One subagent times out after others complete
8. Secret appears in an intermediate tool result
9. Generated program performs nondeterministic mutation
10. Cost or duration budget is exceeded
11. Subagent output is accepted without provenance
12. Orchestrator claims completion despite failed required branch
13. Parallel agents duplicate the same external action
14. ZDR or retention claim is unknown or unavailable

## Acceptance criteria

- [x] Model-authored orchestration programs have explicit sandbox, tool, budget, and evidence constraints — programmatic-tool-execution schema
- [x] Subagents inherit no undeclared authority and use bounded fan-out/concurrency — multi-agent-execution schema
- [x] Cancellation, partial failure, contradiction, duplicate action, and resource exhaustion are testable — fixtures
- [x] Intermediate-data filtering cannot silently erase material evidence — evidence_requirements.discarded_data_policy_enforced
- [x] Receipts preserve the delegation graph, tool scopes, material decisions, and final acceptance posture — evidence_requirements
- [x] Routing/economics hooks integrate with existing model-routing and benchmark programs — route hooks section
- [x] Positive, negative, degraded, and adversarial fixtures exist — see fixtures
- [x] Draft PR is open with validation and rollback evidence — this PR

## Non-goals

- No production multi-agent deployment
- No live external mutations
- No provider/model promotion
- No secret or credential access
- No unlimited autonomous fan-out
- No claim that OpenAI's implementation is fully observable or contractually stable
- No merge authorization from this issue alone

## References

- Issue: hummbl-dev/agent-runtime-governance#12
- Related: hummbl-dev#152, #156, #158; model-routing-as-code#8, #9; autoresearch-pipeline#31
- OpenAI GPT-5.6 announcement (2026-07-09): provider case study, not adopted primitive
