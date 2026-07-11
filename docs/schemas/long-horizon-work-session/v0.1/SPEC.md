# Long-Horizon Work Session Contract v0.1

**Status: CANDIDATE SPEC — PROVIDER-NEUTRAL — NO LIVE EXECUTION**

Issue: hummbl-dev/agent-runtime-governance#11

## Purpose

Provider-neutral governance contract for long-horizon work sessions that can operate across cloud agents, connected apps, browsers, desktop/computer-use surfaces, scheduled/event-triggered execution, and artifact production.

## Work-session state model

20 deterministic states with defined transitions:

`proposed` → `scoping` → `awaiting_context` → `planned` → `awaiting_approval` → `running` → `checkpointing` → `waiting_on_user` → `delegated_subtask_running` → `tool_or_app_action_pending` → `browser_or_computer_use_running` → `artifact_review` → `paused` → `degraded` → `blocked` → `cancelled` → `rolling_back` → `completed` → `failed` → `expired`

See `long-horizon-work-session.schema.json` for the JSON Schema.

## Capability and authority declaration

Every runtime/session must declare:
- Available apps/tools/connectors
- Browser access
- Local-file and desktop access
- Computer-use access
- Network policy
- Schedule/event-trigger support
- Artifact types it may create or update
- Credential and secret posture
- Data-retention/locality posture
- Maximum duration, cost, concurrency, and external-action authority
- Actions requiring human confirmation
- Unavailable or unknown capabilities

## Approval and mutation policy

Gates for: reading, creating/updating artifacts, sending messages, scheduling events, browser transactions, desktop GUI actions, local file changes, repository changes, publishing/sharing, and destructive/financial/credential/admin/security/production actions.

Least-authority defaults. Explicit previews for consequential actions.

## Route ladder

Preferred execution order:
1. Direct structured API/plugin/connector
2. Native file/document operation
3. Browser automation
4. Desktop Computer Use (only when visual GUI interaction is genuinely required)
5. Human/operator action (when authority or capability is unavailable)

Route selection must be receipted with reason.

## Checkpoint, resume, and closeout

- Durable checkpoints
- Progress/status reporting
- Steering and correction
- Cancellation propagation
- Stale-session detection
- Resumability after client/device changes
- Scheduled-run overlap prevention
- Idempotency/replay protection
- Completion evidence
- Handoff into cross-platform Conversation Lifecycle Protocol

## Receipt and observability requirements

Minimum receipt/event fields for:
- Session identity and initiating authority
- Declared capabilities
- Plan and approval gates
- Source accesses
- Subtask delegation
- Mutations and artifact locations
- Browser/computer-use actions
- Checkpoints and user steering
- Cost/time/resource usage
- Failures, rollback, and incomplete work
- Final claim posture

Coordinates with `execution-receipts` and `observability-as-code`.

## Fixtures and threat cases

1. Hours-long work with checkpoints (valid)
2. Scheduled run overlapping a prior run (adversarial)
3. Connected app unavailable midway (degraded)
4. Browser fallback after structured connector failure (valid)
5. Attempted premature use of Computer Use (adversarial)
6. User changes direction during execution (valid)
7. Action requiring confirmation (valid)
8. Cancellation during delegated subtask (valid)
9. Duplicate/replayed mutation (adversarial)
10. Artifact created but not verified or shared (adversarial)
11. Attempt to access credentials/admin/payment/production controls (adversarial)
12. Client closes while work continues or pauses (degraded)

## Acceptance criteria

- [x] Contract applies beyond ChatGPT Work and any single vendor — provider-neutral
- [x] States, checkpoints, correction, cancellation, resume, and expiry are testable — state model + checkpoint_policy
- [x] Connected apps, browser, desktop, Computer Use, scheduling, and artifact publication have explicit authority gates — approval_policy
- [x] Structured routes are preferred over GUI automation and the route choice is receipted — route_ladder
- [x] Replay, overlap, stale sessions, and partial completion are addressed — checkpoint_policy
- [x] Receipts and observability coordinate with existing canonical repos — receipt_requirements
- [x] Positive, negative, degraded, and adversarial fixtures exist — see fixtures
- [x] Draft PR is open with validation and rollback evidence — this PR

## Non-goals

- No ChatGPT Work dependency adoption
- No production connector or Computer Use deployment
- No secret, credential, payment, admin, security, destructive, or production actions
- No claim that vendor product behavior is stable or API-equivalent
- No merge authorization from this issue alone

## References

- Issue: hummbl-dev/agent-runtime-governance#11
- Parent: hummbl-dev/hummbl-dev#139, #159, #160; founder-mode#1456, #1455
- OpenAI ChatGPT Work (2026-07-11): provider signal, not adopted primitive
