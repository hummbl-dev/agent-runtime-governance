# Agent Runtime Governance

Agent Runtime Governance is a public seed repository for runtime governance for agents.

## Purpose

Patterns for governing agents during execution: authority, review, receipts, interrupts, and escalation.

## Glossary

- **Kill switch**: An explicit stop mechanism that halts an agent, workflow, or integration when continued execution is unsafe or unauthorized.
- **Circuit breaker**: A temporary control that pauses or degrades execution after repeated failures, policy violations, or risk signals until review or recovery completes.
- **Guardrail**: A runtime constraint that guides acceptable behavior, such as allowed tools, data boundaries, approval requirements, or escalation rules.
- **Admission control**: The decision point that determines whether a request, tool call, policy packet, or execution step may enter a governed workflow.
- **Fail-closed vs fail-open**: A fail-closed path denies or stops execution when required governance checks cannot complete; a fail-open path allows execution to continue under those conditions.
- **Policy enforcement point**: The component that applies a governance decision at runtime, such as blocking a call, requiring review, logging a receipt, or routing to escalation.

## Contribution Guidance

Use [CONTRIBUTING.md](./CONTRIBUTING.md) for contribution process and [docs/v0.1-boundary.md](./docs/v0.1-boundary.md) for the current repository maturity boundary.

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

## Change Receipt

This README now defines the core governance terms used by the repository and links first-time contributors to the contribution process and v0.1 boundary.
