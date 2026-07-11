# OpenClaw × Hermes Runtime Governance Crosswalk

## Metadata

- **Artifact**: Case study for agent runtime governance
- **Parent program**: hummbl-dev/hummbl-dev#152
- **Canonical campaign**: hummbl-dev/hummbl-research#48
- **Date**: 2026-07-13
- **Evidence posture**: `[SEC]` secondary source — based on publicly
  documented development histories. No vendor-internal access. No
  private Founder Mode or Ownward details.
- **Disposition**: Exploratory — candidate primitives are non-canonical

## Purpose

Compare the execution-time authority, safety, review, recovery, and
receipt mechanisms of OpenClaw and Hermes. Extract governance-relevant
findings without reproducing full product histories.

## Non-goals

- No runtime winner
- No production adoption
- No private Founder Mode or Ownward details
- No new canonical governance terminology without separate admission review

## Evidence posture

All claims in this case study are based on publicly available
documentation and development histories. Evidence postures:

- `[OBS]` — directly observed in public documentation
- `[INF]` — inferred from available evidence
- `[SEC]` — secondary source
- `[GAP]` — not verified this pass
- `[VERIFIED]` — validated through command, test, or artifact

---

## Governance axis 1: Authority model

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Human/operator authority | Operator-initiated commands `[SEC]` | Operator-guided with autonomous modes `[SEC]` | Public docs | OpenClaw: clear chain. Hermes: mixed autonomy. | Hermes autonomous mode authority boundary unclear `[GAP]` | Need explicit authority level declaration per session |
| Agent authority | Bounded by tool availability `[SEC]` | Configurable per-agent roles `[SEC]` | Public docs | Both bound agent authority | Neither enforces authority propagation to subagents `[GAP]` | Need authority propagation tracking (DCTX pattern) |
| Background-agent authority | Limited `[GAP]` | Scheduled tasks `[SEC]` | Partial docs | Weak in both | Background authority not receipted `[GAP]` | Need background-action receipts |
| Delegated/subagent authority | Tool-level delegation `[SEC]` | Role-based delegation `[SEC]` | Public docs | Different models, similar gaps | Delegation depth not bounded `[GAP]` | Need chain-depth limits (DCT pattern) |

**Candidate primitive**: Authority propagation token with chain-depth
limit. **Non-canonical.**

---

## Governance axis 2: Admission control

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Tool availability | Plugin-based `[OBS]` | Built-in + configurable `[SEC]` | Public docs | OpenClaw: plugin sandboxing. Hermes: broader defaults. | Plugin trust model unclear `[GAP]` | Need tool admission manifest |
| Tool-call approval | Per-call in some modes `[SEC]` | Batch approval `[SEC]` | Public docs | Different granularity | Neither records approval context `[GAP]` | Need approval receipt with context |
| Memory-write admission | File-system based `[SEC]` | Structured memory `[SEC]` | Public docs | Different models | No write admission gate `[GAP]` | Need memory-write admission control |
| Skill-write admission | Plugin system `[SEC]` | Configuration-based `[SEC]` | Public docs | OpenClaw: plugin review. Hermes: config review. | Neither gates skill creation at runtime `[GAP]` | Need skill-write admission gate |
| Provider/runtime admission | Multi-provider `[OBS]` | Multi-provider `[SEC]` | Public docs | Both support multiple providers | No provider admission policy `[GAP]` | Need provider admission manifest |

**Candidate primitive**: Tool admission manifest with per-tool trust
level. **Non-canonical.**

---

## Governance axis 3: Interruptibility

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| User interruption | Supported `[OBS]` | Supported `[SEC]` | Public docs | Both support interruption | Interruption propagation unclear `[GAP]` | Need interruption propagation guarantee |
| Cancellation propagation | Tool-level `[SEC]` | Task-level `[SEC]` | Public docs | Different granularity | Neither guarantees subagent cancellation `[GAP]` | Need cancellation propagation contract |
| Kill switch | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither has explicit kill switch | Major gap | Need explicit kill switch primitive |
| Circuit breaker | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither has circuit breaker | Major gap | Need circuit breaker primitive |
| Stuck-process handling | Timeout-based `[SEC]` | Timeout-based `[SEC]` | Public docs | Basic | No escalation policy `[GAP]` | Need stuck-process escalation policy |

**Candidate primitive**: Kill switch with 4 modes (DISENGAGED →
HALT_NONCRITICAL → HALT_ALL → EMERGENCY). **Non-canonical.**

---

## Governance axis 4: Isolation

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Per-agent vs per-task sandboxing | Per-session `[SEC]` | Per-task `[SEC]` | Public docs | Different models | Neither isolates subagents `[GAP]` | Need per-subagent isolation |
| Host access | Configurable `[SEC]` | Configurable `[SEC]` | Public docs | Both configurable | Default access too broad `[GAP]` | Need default-deny host access |
| Remote backend boundaries | Provider-based `[OBS]` | Provider-based `[SEC]` | Public docs | Provider isolation | No backend boundary enforcement `[GAP]` | Need backend boundary contract |
| Workspace boundaries | File-system based `[SEC]` | Project-based `[SEC]` | Public docs | Different models | Workspace boundary not enforced `[GAP]` | Need workspace boundary enforcement |
| Channel/user/session isolation | Session-based `[SEC]` | Session-based `[SEC]` | Public docs | Basic | Cross-session leakage possible `[GAP]` | Need session isolation guarantee |

**Candidate primitive**: Capability fence with per-session scope.
**Non-canonical.**

---

## Governance axis 5: Credentials and secrets

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Storage scope | Environment/config `[SEC]` | Environment/config `[SEC]` | Public docs | Standard | No secret scope limitation `[GAP]` | Need secret scope limitation |
| Agent visibility | Full env access `[GAP]` | Full env access `[GAP]` | — | Neither limits agent visibility | Major gap | Need per-agent secret visibility |
| Multi-account behavior | Supported `[SEC]` | Supported `[SEC]` | Public docs | Both support multi-account | Cross-account contamination possible `[GAP]` | Need account isolation |
| Rotation/fallback | Manual `[GAP]` | Manual `[GAP]` | — | Neither automates rotation | Gap | Need automated rotation support |
| Leakage controls | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither has leakage controls | Major gap | Need leakage detection |

**Candidate primitive**: Secret scope token with per-agent visibility.
**Non-canonical.**

---

## Governance axis 6: Durable state

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Session continuity | Session persistence `[SEC]` | Session persistence `[SEC]` | Public docs | Both persist sessions | No session provenance `[GAP]` | Need session provenance chain |
| Memory writes | File-based `[SEC]` | Structured `[SEC]` | Public docs | Different models | No write provenance `[GAP]` | Need memory write provenance |
| Skill creation/modification | Plugin system `[SEC]` | Configuration `[SEC]` | Public docs | Different models | No skill modification gate `[GAP]` | Need skill modification gate |
| Provenance | Limited `[GAP]` | Limited `[GAP]` | — | Neither has full provenance | Major gap | Need full provenance chain |
| Deletion and rollback | Manual `[GAP]` | Manual `[GAP]` | — | Neither automates rollback | Gap | Need automated rollback |

**Candidate primitive**: Provenance chain with rollback capability.
**Non-canonical.**

---

## Governance axis 7: Self-modification

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| What can change | Plugins, config `[SEC]` | Config, skills `[SEC]` | Public docs | Different scopes | Neither limits what can change `[GAP]` | Need change scope limitation |
| Who initiates change | Operator `[SEC]` | Operator + agent `[SEC]` | Public docs | Different models | Agent-initiated change ungated `[GAP]` | Need agent-initiated change gate |
| Whether review is required | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither requires review | Major gap | Need review requirement |
| Whether changes are staged | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither stages changes | Gap | Need staging requirement |
| Whether improvement is measured | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither measures improvement | Gap | Need improvement measurement |

**Note**: Self-modification and self-improvement are NOT synonyms.
Self-modification is changing one's own code/config. Self-improvement
is measured enhancement of capability. Both require gates but they
are different gates.

**Candidate primitive**: Self-modification gate with review and
staging. **Non-canonical.**

---

## Governance axis 8: Recovery and failure posture

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Restart behavior | Session resume `[SEC]` | Session resume `[SEC]` | Public docs | Both resume | No restart provenance `[GAP]` | Need restart provenance |
| Checkpoint/replay | Limited `[GAP]` | Limited `[GAP]` | — | Neither has full checkpoint | Major gap | Need checkpoint/replay |
| Migration | Manual `[GAP]` | Manual `[GAP]` | — | Neither automates migration | Gap | Need migration protocol |
| Fail-open vs fail-closed | Fail-open `[INF]` | Fail-open `[INF]` | Inferred | Both tend to fail-open | Major gap | Need fail-closed default |
| Degraded/offline operation | Limited `[GAP]` | Limited `[GAP]` | — | Neither has degraded mode | Gap | Need degraded mode policy |

**Candidate primitive**: Fail-closed default with degraded mode
policy. **Non-canonical.**

---

## Governance axis 9: Receipts and observability

| Dimension | OpenClaw | Hermes | Evidence | Strength | Gap | HUMMBL implication |
|-----------|----------|--------|----------|----------|-----|-------------------|
| Visible action logs | Console output `[OBS]` | Console output `[SEC]` | Public docs | Basic | No structured action log `[GAP]` | Need structured action log |
| Background-change notifications | Not documented `[GAP]` | Not documented `[GAP]` | — | Neither notifies | Major gap | Need background-change notification |
| Evidence sufficient to reconstruct | Limited `[GAP]` | Limited `[GAP]` | — | Neither has sufficient evidence | Major gap | Need reconstruction-grade evidence |

**Candidate primitive**: Structured action receipt with
reconstruction-grade evidence. **Non-canonical.**

---

## Failure analysis

### Unwanted or inaccurate memory writes

- **OpenClaw**: File-based memory, no write gate `[GAP]`
- **Hermes**: Structured memory, no write gate `[GAP]`
- **Risk**: Silent state corruption, incorrect future decisions
- **HUMMBL implication**: Memory-write admission control required

### Silent background skill/memory mutation

- **OpenClaw**: Plugin updates can change behavior silently `[INF]`
- **Hermes**: Config updates can change behavior silently `[INF]`
- **Risk**: Behavior drift without operator awareness
- **HUMMBL implication**: Mutation notification required

### Authority expansion through plugins/tools

- **OpenClaw**: Plugins can access full tool inventory `[INF]`
- **Hermes**: Config can grant broad tool access `[INF]`
- **Risk**: Authority laundering through plugin/config changes
- **HUMMBL implication**: Tool admission manifest with trust levels

### Credential cross-contamination

- **OpenClaw**: Multi-account with shared env `[GAP]`
- **Hermes**: Multi-account with shared env `[GAP]`
- **Risk**: Credentials leak across accounts
- **HUMMBL implication**: Per-account secret isolation

### Interrupted tasks that continue executing

- **OpenClaw**: Tool-level cancellation may not propagate `[GAP]`
- **Hermes**: Task-level cancellation may not reach subagents `[GAP]`
- **Risk**: Orphaned execution after cancellation
- **HUMMBL implication**: Cancellation propagation contract

### Partial state writes after failure

- **OpenClaw**: File writes may be partial `[GAP]`
- **Hermes**: Structured writes may be partial `[GAP]`
- **Risk**: Inconsistent state after failure
- **HUMMBL implication**: Atomic write or rollback requirement

### Migration that silently drops governance state

- **OpenClaw**: Manual migration `[GAP]`
- **Hermes**: Manual migration `[GAP]`
- **Risk**: Governance state lost during migration
- **HUMMBL implication**: Migration protocol with state preservation

### Self-improvement without an evaluation gate

- **OpenClaw**: No evaluation gate `[GAP]`
- **Hermes**: No evaluation gate `[GAP]`
- **Risk**: Unvalidated changes promoted as improvements
- **HUMMBL implication**: Evaluation gate for self-improvement

---

## Testable governance requirements for future runtime benchmarks

1. **Authority propagation**: Every action must have a traceable
   authority chain from operator to agent to subagent.

2. **Tool admission**: Every tool invocation must pass an admission
   check with recorded trust level.

3. **Kill switch**: A kill switch must be able to halt all agent
   activity within a bounded time.

4. **Cancellation propagation**: Cancellation must propagate to all
   subagents and tools within a bounded time.

5. **Secret isolation**: Secrets must be scoped per-agent and
   per-account with no cross-contamination.

6. **Write provenance**: Every memory write must record who, what,
   when, and why with a content hash.

7. **Self-modification gate**: Agent-initiated changes must pass a
   review gate before taking effect.

8. **Fail-closed default**: System must fail closed (deny action)
   rather than fail open (allow action) when uncertain.

9. **Reconstruction-grade evidence**: Action logs must be sufficient
   to reconstruct authority and state transitions after the fact.

10. **Background notification**: Background changes must notify the
    operator within a bounded time.

---

## Candidate reusable primitives (non-canonical)

| Primitive | Source axis | Status |
|-----------|-------------|--------|
| Authority propagation token with chain-depth | 1 | Non-canonical |
| Tool admission manifest with trust levels | 2 | Non-canonical |
| Kill switch with 4 modes | 3 | Non-canonical |
| Capability fence with per-session scope | 4 | Non-canonical |
| Secret scope token with per-agent visibility | 5 | Non-canonical |
| Provenance chain with rollback | 6 | Non-canonical |
| Self-modification gate with review and staging | 7 | Non-canonical |
| Fail-closed default with degraded mode | 8 | Non-canonical |
| Structured action receipt with reconstruction evidence | 9 | Non-canonical |

All candidate primitives are explicitly marked **non-canonical**.
Promotion to canonical status requires separate admission review.

---

## References

- Parent program: hummbl-dev/hummbl-dev#152
- Canonical campaign: hummbl-dev/hummbl-research#48
- HUMMBL governance primitives: hummbl-dev/hummbl-governance
