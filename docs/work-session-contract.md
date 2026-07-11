# Long-Horizon Work-Session Contract — Draft v0.1

## Status

**Draft / experimental.** Not for production use. Provider-neutral governance
contract for long-horizon work sessions across cloud agents, connected apps,
browsers, desktop/computer-use surfaces, scheduled/event-triggered execution,
and artifact production.

## Design principles

1. **Provider-neutral**: Contract must not depend on a specific vendor
2. **Least-authority**: Sessions declare minimum required capabilities
3. **Deterministic**: State transitions must be testable
4. **Receipt-producing**: Consequential operations produce receipts
5. **Human-in-the-loop**: High-stakes actions require human confirmation

## Scope distinctions

| Concept | Definition |
|---------|-----------|
| Conversation | Real-time exchange between user and agent |
| Project/context container | Persistent context for related work sessions |
| Delegated work session | A long-running session with delegated authority |
| Scheduled/condition-triggered run | A session initiated by schedule or event |
| Browser/computer-use subtask | A subtask requiring browser or desktop GUI |
| Connected-app/tool mutation | A mutation via a connected app or tool |
| Artifact publication | Creation or update of an artifact (doc, sheet, slide) |
| Coding/repository execution | Code changes in a repository |

---

## 1. Work-session state model

### States

| State | Description |
|-------|-------------|
| `proposed` | Session has been proposed but not yet scoped |
| `scoping` | Session is being scoped (capabilities, authority, plan) |
| `awaiting_context` | Session is waiting for context from the user or system |
| `planned` | Session has a plan but not yet approved |
| `awaiting_approval` | Session is waiting for human approval |
| `running` | Session is actively executing |
| `checkpointing` | Session is saving a checkpoint |
| `waiting_on_user` | Session is waiting for user input |
| `delegated_subtask_running` | A delegated subtask is running |
| `tool_or_app_action_pending` | A tool or app action is pending confirmation |
| `browser_or_computer_use_running` | Browser or computer-use subtask is running |
| `artifact_review` | An artifact is being reviewed before publication |
| `paused` | Session is paused by the user or system |
| `degraded` | Session is running with degraded capabilities |
| `blocked` | Session is blocked (error, missing dependency, authority gap) |
| `cancelled` | Session has been cancelled |
| `rolling_back` | Session is rolling back changes |
| `completed` | Session has completed normally |
| `failed` | Session has failed |
| `expired` | Session has expired (timeout or staleness) |

### Allowed transitions

```
proposed → scoping
scoping → awaiting_context
scoping → planned
awaiting_context → planned
planned → awaiting_approval
awaiting_approval → running (approved)
awaiting_approval → cancelled (denied)
running → checkpointing
running → waiting_on_user
running → delegated_subtask_running
running → tool_or_app_action_pending
running → browser_or_computer_use_running
running → artifact_review
running → paused
running → degraded
running → blocked
running → completed
checkpointing → running
waiting_on_user → running
delegated_subtask_running → running
tool_or_app_action_pending → running (confirmed)
tool_or_app_action_pending → cancelled (denied)
browser_or_computer_use_running → running
artifact_review → running (approved)
artifact_review → cancelled (rejected)
paused → running (resumed)
paused → expired (timeout)
degraded → running (recovered)
degraded → blocked
blocked → running (resolved)
blocked → rolling_back
blocked → failed
rolling_back → completed
rolling_back → failed
any → cancelled (user cancel)
any → expired (timeout)
```

---

## 2. Capability and authority declaration

Every runtime/session must declare:

```typescript
interface SessionCapabilityDeclaration {
  // Available apps/tools/connectors
  available_apps: string[];
  available_tools: string[];
  available_connectors: string[];

  // Access surfaces
  browser_access: "none" | "read" | "interact" | "full";
  local_file_access: "none" | "read" | "read_write";
  desktop_access: "none" | "computer_use";
  computer_use_access: "none" | "visual_gui" | "full_desktop";

  // Network policy
  network_policy: "none" | "local_only" | "owned_endpoints" | "open";

  // Schedule/event support
  schedule_support: boolean;
  event_trigger_support: boolean;

  // Artifact types
  artifact_types_create: string[];
  artifact_types_update: string[];

  // Credential and secret posture
  credential_posture: "none" | "read_only" | "use_with_confirmation" | "full";
  secret_access: "none" | "explicit_per_secret";

  // Data retention/locality
  data_retention: "session" | "persistent" | "unknown";
  data_locality: "local" | "provider_edge" | "provider_cloud" | "mixed" | "unknown";

  // Limits
  max_duration: string; // ISO 8601 duration
  max_cost: number; // in provider-defined units
  max_concurrency: number;
  external_action_authority: "none" | "preview_only" | "confirm_required" | "autonomous";

  // Human confirmation
  actions_requiring_confirmation: string[];

  // Unavailable/unknown capabilities
  unavailable_capabilities: string[];
  unknown_capabilities: string[];
}
```

---

## 3. Approval and mutation policy

### Gates by action class

| Action class | Default gate | Preview required |
|--------------|-------------|-----------------|
| Reading connected sources | none | no |
| Creating/updating docs | confirm_required | yes |
| Creating/updating sheets | confirm_required | yes |
| Creating/updating slides | confirm_required | yes |
| Creating/updating Sites | confirm_required | yes |
| Sending messages | confirm_required | yes |
| Scheduling events/tasks | confirm_required | yes |
| Browser transactions | confirm_required | yes |
| Desktop GUI actions | confirm_required | yes |
| Local file changes | confirm_required | yes |
| Repository changes | confirm_required | yes |
| Publishing/sharing artifacts | explicit_confirm | yes |
| Destructive actions | explicit_confirm + human_review | yes |
| Financial actions | explicit_confirm + human_review | yes |
| Credential actions | explicit_confirm + human_review | yes |
| Admin actions | explicit_confirm + human_review | yes |
| Security actions | explicit_confirm + human_review | yes |
| Production actions | explicit_confirm + human_review | yes |

### Least-authority defaults

- Sessions start with NO capabilities
- Capabilities are granted explicitly by the user or operator
- Capabilities can be revoked at any time
- No implicit capability escalation

---

## 4. Route ladder

Preferred execution order (highest structure first):

1. **Direct structured API/plugin/connector** — preferred when available
2. **Native file/document operation** — when no API but file access is available
3. **Browser automation** — when no API and no file access
4. **Desktop Computer Use** — only when visual GUI interaction is genuinely required
5. **Human/operator action** — when authority or capability is unavailable

### Route selection recording

When a lower-structure route is selected, the session must record:

```typescript
interface RouteSelection {
  selected_route: "api" | "file" | "browser" | "computer_use" | "human";
  reason: string; // why this route was selected
  higher_routes_tried: string[]; // routes that were unavailable
  timestamp: string; // ISO 8601
}
```

---

## 5. Checkpoint, resume, and closeout

### Durable checkpoints

- Sessions must checkpoint at meaningful boundaries (after each subtask, before
  consequential actions, before degradation)
- Checkpoints include: state, plan progress, delegated subtask status, pending
  confirmations
- Checkpoints are durable across client/device changes

### Progress/status reporting

- Sessions report progress at configurable intervals
- Progress includes: current state, completed steps, remaining steps, estimated
  completion, cost incurred

### Steering and correction

- Users can steer (adjust plan) or correct (fix a mistake) at any time
- Steering produces a steering receipt
- Correction may require rollback depending on the action

### Cancellation propagation

- User cancellation propagates to all delegated subtasks
- Each subtask receives a cancellation signal
- Subtasks produce cancellation receipts

### Stale-session detection

- Sessions are marked `expired` after a configurable timeout
- Stale sessions are detected by heartbeat or activity monitoring
- Expired sessions produce an expiry receipt

### Resumability after client/device changes

- Sessions are resumable from the last checkpoint
- Client/device changes are transparent (session state is server-side)
- Resume produces a resume receipt

### Scheduled-run overlap prevention

- Scheduled runs check for an active session with the same schedule
- If active, the new run is queued or skipped (configurable)
- Overlap prevention produces an overlap receipt

### Idempotency/replay protection

- Every action has a unique `action_id`
- Duplicate actions (same `action_id`) are detected and discarded
- Replay attempts produce a replay receipt

### Completion evidence

- Completed sessions produce a completion receipt with:
  - Session identity and initiating authority
  - Declared capabilities
  - Plan and actual execution
  - Mutations and artifact locations
  - Cost/time/resource usage
  - Failures and rollback events

### Handoff to Conversation Lifecycle Protocol

- On completion, session hands off to the cross-platform Conversation Lifecycle
  Protocol (separate spec)
- Handoff includes: session summary, artifacts produced, follow-up actions

---

## 6. Receipt and observability requirements

### Minimum receipt fields

```typescript
interface WorkSessionReceipt {
  receipt_id: string;
  session_id: string;
  initiating_authority: string;
  timestamp: string; // ISO 8601

  // Declared capabilities
  capabilities: SessionCapabilityDeclaration;

  // Plan and approval
  plan_summary: string;
  approval_gates: ApprovalGate[];

  // Source accesses
  source_accesses: SourceAccess[];

  // Subtask delegation
  delegated_subtasks: DelegatedSubtask[];

  // Mutations and artifacts
  mutations: Mutation[];
  artifact_locations: string[];

  // Browser/computer-use actions
  browser_actions: BrowserAction[];
  computer_use_actions: ComputerUseAction[];

  // Checkpoints and steering
  checkpoints: Checkpoint[];
  steering_events: SteeringEvent[];

  // Cost/time/resource
  cost_incurred: number;
  time_elapsed: string; // ISO 8601 duration
  resource_usage: Record<string, number>;

  // Failures and rollback
  failures: Failure[];
  rollback_events: RollbackEvent[];

  // Incomplete work
  incomplete_work: IncompleteWork[];

  // Outcome
  outcome: "completed" | "failed" | "cancelled" | "expired";
}
```

---

## Non-goals

- No provider-specific implementation
- No product-specific policy
- No crisis or safety authority
- No new canon or merge authorization from this issue alone

## Unresolved questions

1. Should state names align with existing workflow engines (Temporal, Airflow)?
2. What is the minimum capability set for a session to start?
3. How should multi-agent sessions be represented?
4. What is the canonical checkpoint format?

## Rollback instructions

This is a specification document. Rollback = revert the commit. No runtime
impact.

## Related

- `hummbl-dev/agent-runtime-governance#11` — this issue
- `hummbl-dev/hummbl-dev#139` — company signal intake
- `hummbl-dev/hummbl-dev#159` and `#160` — conversation/session continuity
- `hummbl-dev/founder-mode#1456` — Computer-use pilot
- `hummbl-dev/founder-mode#1455` — Mobile continuity
