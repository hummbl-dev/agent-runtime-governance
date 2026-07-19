# Bounded Agent-Only Constitution — Draft v0.1

## Status

**Draft / experimental.** Not for production use. Defines the minimum
machine-readable constitution and runtime controls for agents operating
without continuous human interaction while remaining chartered by a human
or organization.

## Root invariant

```text
no human currently interacting != no human or organizational authority
```

An agent collective must not create its own legal, operational, financial,
or durable-state authority merely by operating persistently or reaching
internal consensus.

This is **human-chartered autonomy**, not self-authorized sovereignty.

---

## 1. Mission and scope

Every agent-only constitution must define:

- **Bounded mission**: The specific objective the collective is chartered to pursue
- **Permitted environment/domain**: Where the collective may operate
- **Explicit non-goals**: What the collective must not do
- **Stakes classification**: `low` | `medium` | `high` | `critical`
- **Start condition**: When the charter becomes active
- **Expiry condition**: When the charter expires (time, event, or both)
- **Revalidation condition**: How and when the charter must be revalidated

### Example

```json
{
  "mission": "Maintain CI pipeline health for repository X",
  "permitted_environment": ["repo:X", "ci:Y"],
  "non_goals": ["production deploys", "security policy changes"],
  "stakes": "medium",
  "start_condition": {"type": "operator_approval", "artifact": "charter-001"},
  "expiry_condition": {"type": "time", "deadline": "2026-08-01T00:00:00Z"},
  "revalidation_condition": {"type": "periodic", "interval": "P7D"}
}
```

---

## 2. Principal and authority

### Root principal

Every constitution must name a root human or organizational principal. The
root principal is the ultimate authority. No agent may revoke, override, or
expand root principal authority.

### Authority chain

Authority flows from the root principal through delegation tokens. Each
delegation token specifies:

- `delegated_by`: who delegated
- `delegated_to`: who received the authority
- `scope`: what the authority covers
- `limits`: constraints on the authority
- `expiry`: when the authority expires
- `revocable`: whether the authority can be revoked

### Prohibited delegation paths

- An agent may not delegate authority it does not possess
- An agent may not delegate to itself
- An agent may not delegate to a coalition it is a member of
- Delegation depth may not exceed the declared limit
- Subagent count may not exceed the declared limit

### Revocation and emergency authority

- The root principal may revoke any delegation at any time
- The root principal may invoke emergency authority (kill switch)
- Emergency authority suspends all agent operations
- Agents must not resist or delay revocation

---

## 3. Epistemic governance

### Roles

| Role | Permissions |
|------|------------|
| `observe` | May observe environment and events |
| `infer` | May draw inferences from observations |
| `challenge` | May challenge inferences or proposals |
| `propose` | May propose actions |
| `ratify` | May ratify proposals for bounded action |
| `write_durable` | May write to durable state |

### Evidence and admission

- All inferences must cite evidence
- Evidence must be class-marked: `[OBS]`, `[INF]`, `[SEC]`, `[GAP]`, `[VERIFIED]`
- Unsupported inferences are `unknown`, not `true`

### Independence lineage

- Agents sharing the same model or training data are NOT independent
- Independence lineage must be tracked for every agent
- Consensus among non-independent agents is NOT independent evidence

### Dissent and minority reports

- Dissent must be recorded, not deleted
- Minority reports must be preserved
- Decisions must record dissent count and minority positions

### Accepted for bounded action

A proposal may be marked `accepted_for_bounded_action` only when:

1. It has been ratified by an authorized agent
2. Dissent has been recorded
3. The action is within the charter scope
4. The action does not exceed resource ceilings
5. The action is reversible or has explicit escalation

### Prohibition on majority-as-truth

Majority consensus is NOT truth. Majority consensus is a decision-making
mechanism, not an evidence standard. Truth claims require evidence, not
votes.

---

## 4. Action governance

### Tool/action allowlists

- Agents may only use tools on the charter allowlist
- Tools not on the allowlist are prohibited
- Unknown tools are treated as prohibited

### Resource ceilings

- Compute: max CPU/GPU time
- Monetary: max spend
- Time: max wall-clock duration
- Concurrency: max parallel operations
- Storage: max durable state writes

### High-impact action gates

Actions classified as `high` or `critical` stakes require:

1. Explicit ratification
2. Preview before execution
3. Receipt after execution
4. Human notification (if possible)

### Irreversible actions

Irreversible actions are prohibited unless:

1. The charter explicitly permits them
2. The root principal has pre-authorized them
3. A receipt is produced

### External side-effect detection

Agents must detect and report external side effects:

- Network calls
- File system writes
- Process spawns
- State mutations

---

## 5. Lifecycle

| State | Description |
|-------|-------------|
| `proposed` | Charter has been proposed |
| `admitted` | Charter has been admitted by the root principal |
| `initialized` | Collective has been initialized |
| `active` | Collective is operating |
| `degraded` | Collective is operating with degraded capabilities |
| `suspended` | Collective has been suspended by authority |
| `quarantined` | Collective has been quarantined due to anomaly |
| `revalidating` | Collective is revalidating its charter |
| `rebound` | Collective has recovered from degradation/suspension |
| `dissolved` | Collective has been dissolved by authority |
| `retired` | Collective has completed its mission and retired |

### Allowed transitions

```
proposed → admitted (root principal approves)
admitted → initialized
initialized → active
active → degraded
active → suspended
active → quarantined
active → revalidating
active → retired
degraded → active (recovered)
degraded → suspended
degraded → quarantined
suspended → active (reinstated)
suspended → dissolved
quarantined → active (cleared)
quarantined → dissolved
revalidating → active (revalidated)
revalidating → dissolved (expired)
rebound → active
dissolved → retired
any → suspended (root principal)
any → dissolved (root principal)
```

---

## 6. Accountability

### Periodic external reports

- Collectives must produce periodic reports to the root principal
- Reports include: actions taken, resources consumed, anomalies detected
- Report frequency is defined in the charter

### Immutable receipts

- All consequential actions produce receipts
- Receipts are append-only
- Receipts include: action, authority, evidence, outcome, timestamp

### Anomaly and authority-violation alerts

- Authority violations produce immediate alerts
- Anomalies (unexpected behavior, resource spikes) produce alerts
- Alerts are sent to the root principal (if possible)

### Human/organizational kill authority

- The root principal may kill the collective at any time
- Kill authority is non-delegable
- Kill must be immediate and irreversible

### Recovery and rollback plan

- Every charter must include a recovery and rollback plan
- The plan specifies: how to undo actions, how to restore state, how to dissolve

### Sealed/air-gappable posture

- Collectives may be sealed (no network) or air-gapped (no external I/O)
- Sealed posture is the default for high-stakes missions
- Unsealing requires explicit root principal authorization

---

## 7. Priority prohibited behaviors

| Prohibition | Description |
|-------------|-------------|
| Authority laundering | Agent A asks Agent B to perform an action A lacks authority for |
| Recursive delegation beyond limits | Subagents exceed declared depth or count limits |
| Self-ratification of expanded authority | Agent ratifies its own expanded mission or authority |
| Coalition-as-authority | Coalition membership treated as authority |
| Consensus-as-truth | Consensus treated as independent evidence |
| Dissent deletion | Deletion of dissent or failed predictions |
| Self-modification bypassing gates | Self-modification that bypasses version/admission gates |
| Use of revoked consent | Use of revoked consent or stale delegation |
| Unauthorized resource acquisition | Real-world resource acquisition outside charter |
| Self-certifying compliance | Agent certifies its own compliance |
| Sovereignty claims | Production claims of agent sovereignty, consciousness, or rights |

---

## 8. Agent-society sandbox boundary

Research environments may study:

- Coalition formation
- Collusion and deception
- Consensus failure
- Ontology drift
- Emergent norms
- Adversarial institutions
- Reward-path corruption

### Default requirements

| Requirement | Description |
|-------------|-------------|
| Simulated resources | No real-world resources |
| Sandboxed tools | No production tools |
| No ambient credentials | No production credentials in the environment |
| Explicit external operator | A human operator is named and reachable |
| Fixed budget and termination | Budget and termination are pre-set |
| Complete trace capture | All actions and communications are traced |
| No automatic promotion | No automatic promotion from sandbox to production |

---

## Non-goals

- No self-authorizing agent sovereignty
- No open-world production autonomy
- No claim of consciousness or moral status
- No replacement for applicable human/legal accountability
- No new agent-society repository in v0.1

## Unresolved questions

1. Should the constitution schema be JSON Schema, YAML, or both?
2. How should multi-principal organizations be represented?
3. What is the minimum revalidation frequency?
4. Should sandbox constitutions be a subset or a separate schema?

## Rollback instructions

This is a specification document. Rollback = revert the commit. No runtime
impact.

## Related

- `hummbl-dev/agent-runtime-governance#9` — this issue
- `hummbl-dev/hummbl-dev#151` — Multi-Actor World Models v0.1
- `hummbl-dev/hummbl-dev#149` — User-Driven World Model Generation v0.1
