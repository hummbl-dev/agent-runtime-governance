# Prior Art and Adjacent Ecosystem

This document surveys public prior art and adjacent ecosystem primitives relevant
to runtime governance for agents. It is a survey, not a comparison matrix and not
an endorsement.

## Non-canon note

This survey is **non-canon**. Listing a project here:

- Is a pointer to public prior art, not an endorsement.
- Does not assert that this repo adopts, aligns with, or extends that project.
- Does not claim ownership of any term the project uses.
- Does not canonize any vendor, product, or internal system that resembles it.

Terminology used in this repo (governance, runtime, guardrail, admission control,
policy enforcement, kill switch, circuit breaker, rate limit) is borrowed from
public prior art and is used descriptively, not authoritatively.

## Public prior art: policy engines

### Open Policy Agent (OPA)

- **What it does:** A general-purpose policy engine that evaluates declarative
  policies written in Rego against JSON input. Commonly used for authorization,
  admission control, and runtime policy decisions.
- **Relevance:** Reference model for a standalone policy engine with a declarative
  policy language, deny/allow decisions, and an audit surface. Directly informs
  the `policyEngine` and `enforcementPoints` shape of a v0.1 packet.
- **Docs:** https://www.openpolicyagent.org/docs/latest/

### AWS Service Control Policies (SCPs)

- **What it does:** Organization-level guardrails in AWS Organizations that
  constrain the maximum available permissions for accounts within an organization.
- **Relevance:** Reference model for authority-scoped guardrails applied at a
  boundary above the runtime, and for the idea that governance can constrain but
  not grant. Informs the `authority` and `guardrailSpecs` shape.
- **Docs:** https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html

### Azure Policy

- **What it does:** A policy-as-code service in Azure that evaluates resource
  properties against declarative policy definitions and enforces compliance at
  deployment and audit time.
- **Relevance:** Reference model for policy-as-code with audit, deny, and
  deploy-if-not-exists effects, and for evaluating governance at an enforcement
  point rather than only at runtime. Informs `enforcementPoints` and
  `auditRequirements`.
- **Docs:** https://learn.microsoft.com/en-us/azure/governance/policy/overview

### Kyverno

- **What it does:** A Kubernetes-native policy engine that validates, mutates,
  and generates Kubernetes resources using declarative YAML policies.
- **Relevance:** Reference model for native policy authoring without a separate
  policy language, and for admission-time enforcement in a container orchestrator.
  Informs `policyEngine` and `enforcementPoints`.
- **Docs:** https://kyverno.io/docs/

### Gatekeeper (OPA Gatekeeper)

- **What it does:** An admission controller for Kubernetes that uses OPA to
  enforce declarative policies on Kubernetes API requests.
- **Relevance:** Reference model for embedding a policy engine at a specific
  enforcement point (admission) and for separating policy authoring from policy
  enforcement. Informs `enforcementPoints` and `auditRequirements`.
- **Docs:** https://open-policy-agent.github.io/gatekeeper/website/docs/

### HashiCorp Sentinel

- **What it does:** A policy-as-code framework for Terraform and other HashiCorp
  products that evaluates infrastructure changes against declarative Sentinel
  policies before apply.
- **Relevance:** Reference model for policy-as-code with a soft-mandate
  enforcement model (advisory, soft-mandatory, hard-mandatory) and for evaluating
  governance at a plan/apply boundary. Informs `policyEngine` and the
  fail-closed vs fail-open distinction.
- **Docs:** https://developer.hashicorp.com/sentinel/docs

### Cedar (AWS)

- **What it does:** A policy language and authorization engine from AWS for
  writing fine-grained authorization policies using principals, actions, and
  resources.
- **Relevance:** Reference model for a compact, analyzable policy language with
  explicit allow/deny semantics and schema-backed validation. Informs
  `policyEngine` and deny/allow modeling.
- **Docs:** https://www.cedarpolicy.com/docs

### Conftest

- **What it does:** A tool for testing structured configuration files (YAML,
  JSON, HCL) against Rego policies, commonly used in CI pipelines.
- **Relevance:** Reference model for validating governance-relevant artifacts
  (configuration, manifests) against policies before they reach a runtime.
  Informs the validation intent behind the v0.1 valid/invalid fixtures.
- **Docs:** https://www.conftest.dev/

## Adjacent ecosystem primitives

These are not policy engines but are primitives that runtime governance for
agents will likely compose with or reference.

### Kill switches

- **What it does:** A mechanism to immediately halt or disable a system, process,
  or agent, typically used as a last-resart safety control.
- **Relevance:** Directly informs `killSwitchPolicy`. A governance packet should
  be able to declare when a kill switch may be triggered and by whom.
- **Public reference:** https://en.wikipedia.org/wiki/Kill_switch

### Circuit breakers (Hystrix, Resilience4j)

- **What it does:** A resilience pattern that opens a circuit when failure rates
  exceed a threshold, halting calls to a failing dependency until it recovers.
- **Relevance:** Directly informs `circuitBreakerPolicy`. Hystrix popularized the
  pattern in the JVM ecosystem; Resilience4j is its modern successor.
- **Docs:**
  - Hystrix: https://github.com/Netflix/Hystrix/wiki
  - Resilience4j: https://resilience4j.readme.io/docs

### Rate limiters (Redis, Envoy)

- **What it does:** Mechanisms that bound the rate of operations (requests,
  calls, actions) to protect downstream systems or control cost.
- **Relevance:** Adjacent primitive for runtime governance of agent actions,
  especially for cost and abuse control. Referenced descriptively, not adopted.
- **Docs:**
  - Redis rate limiting: https://redis.io/docs/manual/patterns/distributed-locks/
  - Envoy rate limit: https://www.envoyproxy.io/docs/envoy/latest/configuration/listeners/network_filters/rate_limit_filter

### Admission controllers (Kubernetes)

- **What it does:** Plugins in the Kubernetes API server that intercept and
  validate, mutate, or reject object creation requests before they are persisted.
- **Relevance:** Reference model for an enforcement point that sits on the path
  between request and effect, with deny/allow and audit semantics. Directly
  informs `enforcementPoints`.
- **Docs:** https://kubernetes.io/docs/reference/access-authn-authz/admission-controllers/

### Guardrails (NVIDIA NeMo Guardrails, Guardrails AI)

- **What it does:** Frameworks for adding programmable rails to LLM-based
  applications: input/output validation, topic control, safety, and structured
  output enforcement.
- **Relevance:** The closest adjacent ecosystem to agent runtime governance.
  NeMo Guardrails focuses on conversational rails for LLM apps; Guardrails AI
  focuses on validating LLM outputs against schemas and rules. Both inform
  `guardrailSpecs`.
- **Docs:**
  - NVIDIA NeMo Guardrails: https://github.com/NVIDIA/NeMo-Guardrails
  - Guardrails AI: https://www.guardrailsai.com/docs

## Vocabulary

Terms used descriptively in this repo, borrowed from the prior art above. No
ownership is claimed over any of them.

- **Governance:** The set of policies, authority, and review practices that
  constrain and shape a system's behavior.
- **Runtime:** The period during which an agent or process is executing and
  making decisions.
- **Guardrail:** A boundary control that prevents a system from taking an
  out-of-bound action.
- **Admission control:** An enforcement pattern where requests are validated
  before they take effect.
- **Policy enforcement:** The act of evaluating a request against a policy and
  acting on the result (allow, deny, mutate, audit).
- **Kill switch:** A last-resort control that halts a system immediately.
- **Circuit breaker:** A resilience control that suspends calls to a failing
  dependency until it recovers.
- **Rate limit:** A control that bounds the frequency of operations.

## Key concepts

- **Policy engines:** Standalone systems that evaluate declarative policies
  against input (OPA, Cedar, Kyverno, Sentinel, Conftest).
- **Enforcement points:** Locations in a request/runtime path where policies are
  evaluated (admission controllers, plan/apply boundaries, runtime hooks).
- **Deny/allow:** The basic decision shape of most policy engines; some add
  mutate, audit, or warn.
- **Exceptions:** Mechanisms for permitting an otherwise-denied action under
  recorded, reviewable conditions.
- **Audit trails:** Durable records of what was decided, by what policy, and
  with what input.
- **Escalation:** Routing a decision or incident to a human or higher-authority
  process when policy cannot resolve it.
- **Fail-closed vs fail-open:** Whether a policy engine denies (closed) or
  permits (open) a request when it cannot evaluate successfully. v0.1 records
  this as a declared posture, not an enforced behavior.
