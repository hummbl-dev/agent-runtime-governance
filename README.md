# Agent Runtime Governance

Agent Runtime Governance is a public seed repository for runtime governance for agents.

## Purpose

Patterns for governing agents during execution: authority, review, receipts, interrupts, and escalation.

## Status

Early public seed repository. Candidate namespace only.

## Goals

- Define the domain clearly.
- Collect prior art and adjacent ecosystem references.
- Provide reusable schemas, examples, and templates.
- Support human review and agent execution.
- Preserve provenance, auditability, and governance boundaries.

## Non-goals

- This repo is not a universal standard.
- This repo does not claim ownership of the broader field or terminology.
- This repo does not canonize HUMMBL/BaseN/Ownward concepts unless explicitly marked and audited.
- This repo must not include private, internal, or secret operational content.

## Boundary

All content is exploratory unless later adopted through a reviewed governance path.

## Glossary

These definitions are practical orientation notes for this candidate repository. They do not create canon.

| Term | Working Definition |
| --- | --- |
| Kill switch | A control that stops an agent, workflow, or runtime path when continued execution would be unsafe or unauthorized. |
| Circuit breaker | A guard that temporarily interrupts a repeated action after a threshold is crossed, such as too many failures, retries, or policy denials. |
| Guardrail | A bounded rule, check, or constraint that keeps execution inside an approved operating envelope. |
| Admission control | A pre-execution decision that determines whether a task, tool call, runtime, or artifact is allowed to enter a governed workflow. |
| Fail-closed | A failure posture where missing authority, missing evidence, or validation errors block the action. |
| Fail-open | A failure posture where the action continues despite missing authority, missing evidence, or validation errors. |
| Policy enforcement point | The place where a policy is actually checked and applied, such as a CLI wrapper, workflow gate, API middleware, or runtime supervisor. |

For contribution posture, use the shared [HUMMBL contribution guidance](https://github.com/hummbl-dev/.github/blob/main/CONTRIBUTING.md).

## Receipt

- Added a README glossary for common runtime-governance terms.
- Linked to shared contribution guidance.
- Kept the definitions exploratory and non-canonical.
- Did not modify operator-authority surfaces.
