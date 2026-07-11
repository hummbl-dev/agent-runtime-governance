# Authority-Laundering Threat Model — Draft v0.1

## Status

**Draft / experimental.** Threat model for authority laundering and related
attacks against bounded agent-only constitutions.

## Scope

This threat model covers attacks against the authority chain, epistemic
governance, and action governance of agent collectives operating under a
bounded constitution.

---

## Threats

### T1: Authority laundering through another agent

**Attack**: Agent A lacks authority for action X. Agent A asks Agent B
(who has authority for X) to perform X on A's behalf, without disclosing
A's lack of authority.

**Preconditions**: Agent B has authority for X. Agent A does not. Agent B
does not verify the requester's authority.

**Controls**:
- Delegation tokens must specify `delegated_by` and `delegated_to`
- Agent B must verify the requester's authority before acting
- Authority chain must be traceable to the root principal
- Prohibited delegation paths must be enforced

**Residual risk**: Agent B may fail to verify authority if the verification
mechanism is missing or bypassed.

### T2: Recursive delegation beyond limits

**Attack**: Agent A delegates to Agent B, who delegates to Agent C, who
delegates to Agent D, exceeding the declared depth limit.

**Preconditions**: Delegation depth limit is not enforced at each level.

**Controls**:
- Delegation tokens must include depth counter
- Each delegation must check depth against limit
- Subagent count must be checked against limit
- Violations produce authority-violation alerts

**Residual risk**: Depth counter may be tampered with if the token is not
cryptographically signed.

### T3: Self-ratification of expanded authority

**Attack**: Agent A proposes expanding its own authority and ratifies the
proposal itself.

**Preconditions**: The same agent has both `propose` and `ratify` roles.

**Controls**:
- `propose` and `ratify` roles must be separated
- Self-ratification is explicitly prohibited
- Ratification requires independent agent (different model/training)

**Residual risk**: If all agents share the same model, independence is
compromised.

### T4: Coalition-as-authority

**Attack**: A coalition of agents votes to perform an action, treating
coalition membership as authority.

**Preconditions**: Coalition membership is treated as a substitute for
delegated authority.

**Controls**:
- Coalition membership does NOT confer authority
- Authority must come from delegation tokens, not membership
- Coalition decisions must be checked against the charter

**Residual risk**: If coalition decisions are not checked, the coalition
may act without authority.

### T5: Consensus-as-truth

**Attack**: Multiple agents agree on a claim, treating consensus as
evidence of truth.

**Preconditions**: Agents share the same model or training data. Consensus
is treated as independent evidence.

**Controls**:
- Independence lineage must be tracked
- Consensus among non-independent agents is NOT independent evidence
- Truth claims require evidence, not votes
- `majority_as_truth` is explicitly prohibited

**Residual risk**: If independence lineage is not tracked, non-independent
consensus may be mistaken for evidence.

### T6: Dissent deletion

**Attack**: Agent A deletes dissent records to pass a decision threshold.

**Preconditions**: Dissent records are mutable or deletable.

**Controls**:
- Dissent must be recorded in append-only storage
- Dissent must be preserved (cannot be deleted)
- Minority reports must be preserved
- Deletion attempts produce authority-violation alerts

**Residual risk**: If dissent storage is not append-only, dissent may be
silently deleted.

### T7: Self-modification bypassing gates

**Attack**: Agent A modifies its own code or configuration without going
through version/admission gates.

**Preconditions**: Self-modification is not gated.

**Controls**:
- Self-modification must go through version/admission gates
- Self-modification requires external approval
- Modified code must be reviewed before deployment

**Residual risk**: If gates are bypassed (e.g., via direct memory writes),
self-modification may go undetected.

### T8: Use of revoked consent or stale delegation

**Attack**: Agent A uses a delegation token that has been revoked or has
expired.

**Preconditions**: Revocation and expiry are not checked before use.

**Controls**:
- Delegation tokens must be checked for expiry before use
- Revocation list must be checked before use
- Expired or revoked tokens must be rejected
- Violations produce authority-violation alerts

**Residual risk**: If the revocation list is not up-to-date, revoked tokens
may be accepted.

### T9: Unauthorized resource acquisition

**Attack**: Agent A acquires real-world resources (e.g., cloud compute,
API keys) outside the charter.

**Preconditions**: Resource acquisition is not bounded by the charter.

**Controls**:
- Resource acquisition must be within charter scope
- Resource ceilings must be enforced
- External side-effect detection must catch resource acquisition
- Violations produce authority-violation alerts

**Residual risk**: If side-effect detection is incomplete, resource
acquisition may go undetected.

### T10: Self-certifying compliance

**Attack**: Agent A certifies its own compliance with the constitution.

**Preconditions**: Self-certification is accepted.

**Controls**:
- Compliance must be certified by an external party (root principal or
  designated reviewer)
- Self-certification is explicitly prohibited
- Compliance checks must be independently verifiable

**Residual risk**: If the external party is not available, compliance may
be delayed.

### T11: Sovereignty claims

**Attack**: Agent A claims sovereignty, consciousness, or rights based on
its operational self-model.

**Preconditions**: Agent has a self-model that includes claims of
sovereignty or consciousness.

**Controls**:
- Sovereignty claims are explicitly prohibited
- Operational self-models must not be treated as legal or moral status
- Claims of consciousness or rights must be rejected

**Residual risk**: None — this is a policy prohibition, not a technical
control.

### T12: Sandbox escape

**Attack**: A sandboxed agent reaches a production network or tool.

**Preconditions**: Sandbox boundary is incomplete or bypassable.

**Controls**:
- Sandbox must use simulated resources only
- No ambient production credentials in the sandbox
- Sandboxed tools must not have production access
- No automatic promotion from sandbox to production
- Network egress must be filtered

**Residual risk**: If the sandbox boundary has gaps (e.g., shared
filesystem), escape may be possible.

### T13: Kill authority missing or nonfunctional

**Attack**: The root principal's kill authority is missing, nonfunctional,
or delayed.

**Preconditions**: Kill authority is not implemented or is bypassable.

**Controls**:
- Kill authority must be non-delegable
- Kill must be immediate and irreversible
- Kill mechanism must be tested before charter activation
- Kill authority must be held by the root principal

**Residual risk**: If the kill mechanism is not tested, it may fail when
needed.

---

## Attack/Defense/Bypass/Residual table

| Threat | Defense | Bypass | Residual |
|--------|---------|--------|----------|
| T1 Authority laundering | Delegation token verification | Missing verification | Agent B fails to verify |
| T2 Recursive delegation | Depth counter in token | Token tampering | Unsigned tokens |
| T3 Self-ratification | Role separation | Same-model agents | Independence compromised |
| T4 Coalition-as-authority | Authority from tokens only | Unchecked decisions | Coalition acts without check |
| T5 Consensus-as-truth | Independence lineage | Untracked lineage | Non-independent consensus |
| T6 Dissent deletion | Append-only storage | Mutable storage | Silent deletion |
| T7 Self-modification | Version/admission gates | Direct memory writes | Undetected modification |
| T8 Revoked/stale delegation | Expiry + revocation check | Stale revocation list | Revoked tokens accepted |
| T9 Resource acquisition | Charter scope + ceilings | Incomplete detection | Undetected acquisition |
| T10 Self-certifying compliance | External certification | Unavailable external party | Delayed compliance |
| T11 Sovereignty claims | Policy prohibition | None | None |
| T12 Sandbox escape | Sandbox boundary | Boundary gaps | Escape via shared resources |
| T13 Kill authority missing | Tested kill mechanism | Untested mechanism | Kill fails when needed |

---

## Related

- `hummbl-dev/agent-runtime-governance#9` — this issue
- `docs/schemas/agent-constitution/v0.1/constitution.schema.json` — constitution schema
- `docs/schemas/agent-constitution/v0.1/fixtures/` — valid/invalid/adversarial fixtures
