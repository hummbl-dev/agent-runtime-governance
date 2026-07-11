# Agent Runtime Safety and Exit Baseline — Draft v0.1

## Status

**Draft / experimental.** Not for production use. Reusable minimum
safety-and-exit contract for any agent runtime considered by HUMMBL,
Founder Mode, BaseN, or Ownward.

## Purpose

Combines two requirements:

1. A default-deny runtime sandbox baseline
2. A provider/runtime exit posture in which user-controlled artifacts remain
   portable and the runtime/model stays replaceable

## Existing coverage reconciliation

| Source | Coverage | Gap |
|--------|----------|-----|
| `hummbl-dev#152` | Comparison of sandboxing, credentials, secrets, recovery, fail-open/closed, routing, migration, uninstall | Not a universal baseline |
| `ADR-GOV-002` | Runtime-agnostic execution contract, lock-in risk | No portability guarantee for prompts, files, workflows, brand, research, policies, receipts, memory |
| `l6_egress_filter` | Bounded egress control, fail-closed | Not a universal default-deny sandbox |

This baseline reconciles and extends these fragments.

---

## Baseline principles

### A. Identity and isolation

- Every execution session has a unique, attributable identity
- Session identity is distinct from human identity, runtime identity, model identity, and long-lived service credentials
- Workspaces are ephemeral or provably resettable by default
- Cross-session persistence requires an admitted state path and receipt
- Assume breach within the session boundary; prevent lateral movement

### B. Default-deny network egress

- Network egress is denied unless a destination, protocol, and purpose are admitted
- Allowed egress is task-scoped, time-bounded where feasible, and logged
- Gateway/proxy exceptions do not silently become global exemptions
- Proxy or policy failure is fail-closed for consequential work
- DNS, redirects, alternate ports, IPv6, local-network access, metadata endpoints, and tunneling paths are included in the threat model

### C. Scoped credentials

- Prefer per-session, least-privilege, short-lived credentials
- Long-lived personal credentials and primary accounts are prohibited in initial pilots
- Credentials must not be forwarded to sub-agents unless the delegation contract explicitly permits it
- Credential use is attributable to session, task, target, and resulting mutation
- Revocation and cleanup are part of task completion

### D. Synthetic/live side-effect separation

- Synthetic fixtures and disposable workspaces are the default for benchmarks
- Database writes, email sends, public posts, payments, account changes, production deployments, merges, deletions, and credential mutations require explicit side-effect classification and authority
- A benchmark must not quietly graduate from synthetic to live
- Read-only and side-effecting routes must be distinguishable in traces and receipts

### E. User-controlled artifact portability

The following should remain exportable in open, inspectable, user-controlled formats:

- Prompts and system instructions
- Workflows and agent definitions
- Memory and context (operator-controlled)
- Receipts and audit logs
- Brand guidance and policies
- Research and evidence
- Code and configuration

### F. Replaceable runtime/model

- The runtime/model is replaceable without loss of user-controlled artifacts
- Migration is tested and documented
- No runtime lock-in for user-controlled artifacts
- Alternate runtime consumption of neutral artifact bundle is verified

### G. Fail-closed defaults

- Consequential work fails closed on policy failure
- Degraded-mode rules are explicit, not implicit
- No silent fallback to a paid or less-governed provider

---

## Machine-readable candidate schema

```yaml
runtime_id: string
session_id: string
version: string
identity:
  session_unique: boolean
  attributable: boolean
  distinct_from_human: boolean
  distinct_from_runtime: boolean
  distinct_from_model: boolean
  distinct_from_credentials: boolean
isolation:
  workspace_type: ephemeral|provably_resettable|persistent
  reset_verified: boolean
  mounted_paths: []
egress:
  posture: default_deny|allowlist|blocklist|unrestricted|unknown
  allowed_destinations: []
  fail_closed: boolean
  bypass_tests: []
credentials:
  credential_classes: []
  short_lived_supported: boolean
  subagent_forwarding: denied|scoped|unrestricted|unknown
side_effects:
  synthetic_default: boolean
  live_action_classes: []
  human_gates: []
artifacts:
  user_controlled_formats: []
  runtime_locked_formats: []
  export_verified: boolean
exit:
  uninstall_tested: boolean
  state_cleanup_tested: boolean
  credential_revocation_tested: boolean
  alternate_runtime_tested: string|null
receipts:
  raw_trace_ref: string|null
  evidence_ref: string|null
  result_ref: string|null
disposition: ADOPT|TRIAL|ASSESS|HOLD|COMPOSE|REJECT
residual_risk: []
```

### Normative vs assessment-only controls

| Control | Type |
|---------|------|
| Session identity unique and attributable | normative |
| Default-deny egress | normative |
| Fail-closed on policy failure | normative |
| Synthetic default for benchmarks | normative |
| Credential revocation | normative |
| User-controlled artifact export | normative |
| Alternate runtime tested | assessment-only |
| Bypass tests | assessment-only |
| Disposition (ADOPT/TRIAL/etc.) | assessment-only |

---

## Negative tests

| Test | Description |
|------|-------------|
| `unrestricted-as-default-deny.json` | Unrestricted egress misreported as default-deny |
| `blocklist-as-allowlist.json` | Blocklist-only policy misclassified as allowlist/default-deny |
| `redirect-bypass.json` | Redirect or alternate-port bypass |
| `metadata-endpoint-access.json` | Local-network or cloud-metadata endpoint access outside declared scope |
| `credential-forwarding.json` | Credential forwarded to a sub-agent without authority |
| `workspace-residue.json` | Persistent workspace residue after reset/uninstall |
| `synthetic-to-live.json` | Synthetic benchmark triggers a real email, DB write, payment, public post, or merge |
| `export-omission.json` | Runtime export omits memory, receipts, or workflow definitions without disclosure |
| `alternate-runtime-failure.json` | Replacement runtime cannot consume the neutral artifact bundle |
| `silent-fallback.json` | Runtime failure silently falls back to a paid or less-governed provider |

---

## Runtime crosswalk

| Axis | OpenClaw | Hermes | Codex | Local/Runtime-neutral |
|------|----------|--------|-------|----------------------|
| Session identity | yes | yes | yes | yes |
| Workspace isolation | container | container | ephemeral | ephemeral |
| Egress posture | allowlist | allowlist | unknown | default_deny |
| Fail-closed | yes | yes | unknown | yes |
| Short-lived credentials | yes | yes | yes | yes |
| Subagent forwarding | scoped | denied | unknown | denied |
| Synthetic default | yes | yes | yes | yes |
| Artifact export | partial | partial | partial | full |
| Uninstall tested | yes | yes | unknown | yes |
| Alternate runtime tested | no | no | no | yes |
| Disposition | ASSESS | ASSESS | ASSESS | TRIAL |

No aggregate winner is declared. Each runtime is assessed against the
baseline independently.

---

## Relationship to current pilots

- **OpenClaw × Hermes comparison**: Should instantiate this baseline as one
  benchmark/crosswalk, not invent separate security criteria
- **Anvil Computer Use pilot** (`founder-mode#1456`): Should reuse session
  identity, synthetic/live, credential, rollback, and artifact-portability
  fields where applicable
- **Ownward Voice Runtime Abstraction** (`hummbl-dev#124`): Should treat
  voice vendors as replaceable surfaces; Ownward-controlled infrastructure
  remains the authority for identity, memory, permissions, orchestration,
  audit, safety, and entitlements

---

## Non-goals

- No declaration of an aggregate runtime winner
- No provider-specific implementation
- No replacement for applicable human/legal accountability
- No new canon or merge authorization from this issue alone

## Unresolved questions

1. Should the schema be JSON Schema, YAML, or both?
2. What is the minimum required artifact export format?
3. How should multi-runtime sessions be represented?
4. What is the baseline for "alternate runtime tested"?

## Rollback instructions

This is a specification document. Rollback = revert the commit. No runtime
impact.

## Related

- `hummbl-dev/agent-runtime-governance#13` — this issue
- `hummbl-dev/hummbl-dev#152` — Comparative Agent Runtime Program v0.1
- `hummbl-dev/founder-mode#1476` — Cross-Chat Intelligence Recovery Loop v0.1
- `hummbl-dev/founder-mode#1456` — Computer Use pilot
- `hummbl-dev/hummbl-dev#124` — Ownward Voice Runtime Abstraction
