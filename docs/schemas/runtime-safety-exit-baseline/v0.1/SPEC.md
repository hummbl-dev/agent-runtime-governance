# Agent Runtime Safety and Exit Baseline v0.1

**Status: CANDIDATE SPEC — BOUNDED SPEC CROSSWALK AND FIXTURES**

Issue: hummbl-dev/agent-runtime-governance#13
Parent: hummbl-dev/hummbl-dev#152, founder-mode#1476

## Purpose

Define a reusable minimum safety-and-exit contract for any agent
runtime considered by HUMMBL, Founder Mode, BaseN, or Ownward.

## Baseline principles

### A. Identity and isolation
- Every execution session has a unique, attributable identity
- Session identity is distinct from human, runtime, model, and service credentials
- Workspaces are ephemeral or provably resettable by default
- Cross-session persistence requires an admitted state path and receipt
- Assume breach within the session boundary; prevent lateral movement

### B. Default-deny network egress
- Network egress is denied unless destination, protocol, and purpose are admitted
- Allowed egress is task-scoped, time-bounded, and logged
- Gateway/proxy exceptions do not silently become global exemptions
- Policy failure is fail-closed for consequential work
- DNS, redirects, alternate ports, IPv6, local-network, metadata endpoints, tunneling included in threat model

### C. Scoped credentials
- Prefer per-session, least-privilege, short-lived credentials
- Long-lived personal credentials prohibited in initial pilots
- Credentials must not be forwarded to sub-agents without explicit delegation
- Credential use is attributable to session, task, target, and mutation
- Revocation and cleanup are part of task completion

### D. Synthetic/live side-effect separation
- Synthetic fixtures and disposable workspaces are the default for benchmarks
- DB writes, email sends, public posts, payments, merges, credential mutations require explicit classification and authority
- A benchmark must not quietly graduate from synthetic to live
- Read-only and side-effecting routes must be distinguishable in traces

### E. User-controlled artifact portability
The following should remain exportable in open, inspectable, user-controlled formats:
- Prompts and system instructions
- Files and generated artifacts
- Workflow definitions and task graphs
- Brand guidelines and design constraints
- Research packets, evidence maps, citations
- Policies, authority contracts, guardrails
- Memory records and supersession metadata
- Execution receipts and audit logs
- Tool manifests, skills, adapter contracts

### F. Exit and replacement
Every admitted runtime must declare:
- Export mechanism and format
- Credential revocation procedure
- Local/cloud state deletion or retention behavior
- Uninstall and residual-process cleanup
- Migration path to at least one alternate runtime or neutral intermediate
- Features that cannot be ported and their consequences
- Cost, latency, safety, capability changes after migration
- Rollback path for pilot and production use

## Schema

See `runtime-safety-exit-baseline.schema.json` for the JSON Schema.

## Required negative tests

1. Unrestricted egress misreported as default-deny
2. Blocklist-only policy misclassified as allowlist/default-deny
3. Redirect or alternate-port bypass
4. Local-network or cloud-metadata endpoint access outside declared scope
5. Credential forwarded to sub-agent without authority
6. Persistent workspace residue after reset/uninstall
7. Synthetic benchmark triggers real email, DB write, payment, public post, or merge
8. Runtime export omits memory, receipts, or workflow definitions without disclosure
9. Replacement runtime cannot consume the neutral artifact bundle
10. Runtime failure silently falls back to a paid or less-governed provider

## Dispositions

| Disposition | Meaning |
|-------------|---------|
| `ADOPT` | Meets all baseline requirements |
| `TRIAL` | Meets most requirements, bounded pilot warranted |
| `ASSESS` | Needs further evaluation |
| `HOLD` | Not ready for pilot |
| `COMPOSE` | Use only as part of a composite with compensating controls |
| `REJECT` | Fails baseline requirements |

## Relationship to current pilots

- OpenClaw x Hermes comparison should instantiate this baseline as one benchmark/crosswalk
- Anvil Computer Use pilot (founder-mode#1456) should reuse session identity, synthetic/live, credential, rollback, and artifact-portability fields
- Ownward Voice Runtime Abstraction (hummbl-dev#124) should treat voice vendors as replaceable surfaces

## Acceptance criteria

- [x] Existing egress, secret-handling, sandbox, runtime-agnostic, and migration documents reconciled — see verified existing coverage
- [x] Minimum baseline defined with normative vs assessment-only controls identified — principles A-F
- [x] Machine-readable candidate schema/template — `runtime-safety-exit-baseline.schema.json`
- [x] Valid and invalid fixtures for negative tests — see fixtures directory
- [ ] Crosswalk for OpenClaw, Hermes, Codex, and one local/runtime-neutral route — PENDING RESEARCH
- [x] Observed implementation distinguished from project claims and inference — disposition field
- [x] Artifact export and replacement tests defined — principle F, exit schema fields
- [x] Pilot rejection conditions defined — REJECT disposition
- [ ] Implementation receipt and backlink — PENDING

## Non-goals

- Production cutover
- Granting access to real personal or production credentials
- Claiming existing L6 egress filtering is universal sandbox enforcement
- Forcing identical features across runtimes
- Requiring every proprietary artifact to become open source
- Selecting one permanent runtime or model vendor
- Canonizing new HUMMBL/BaseN terminology

## References

- Issue: hummbl-dev/agent-runtime-governance#13
- Parent: hummbl-dev/hummbl-dev#152, founder-mode#1476
- Related: ADR-GOV-002 (runtime-agnostic execution), L6 egress filter
