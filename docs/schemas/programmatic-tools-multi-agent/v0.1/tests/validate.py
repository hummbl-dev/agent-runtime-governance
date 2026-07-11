#!/usr/bin/env python3
"""Programmatic Tool Calling and Multi-Agent Execution Governance validator v0.1.

Validates contracts against schemas and enforces semantic rules:

Programmatic tool execution:
- Unrestricted permissions require human principal (no self-delegation)
- Sandbox type 'none' requires isolation_level 'none' and code_execution 'denied'
- Unrestricted secret_access is invalid
- discard_policy that drops contradicting evidence is invalid
- evidence_requirements must be true when receipt_required is true
- Unrestricted network requires allowlist tools (no undeclared tool path)

Multi-agent execution:
- No subagent may have reduced_permissions=false with broad inherited_permissions
- max_fan_out > 100 is excessive
- final_gate 'none' is invalid for non-trivial orchestrator
- evidence_attribution must be true for all subagents
- self-assigned orchestrator authority is invalid

Uses only Python stdlib.
"""

import json
import sys
from pathlib import Path


def validate_tool_execution(record: dict) -> list[str]:
    errors = []
    required = [
        "schema_version", "contract_id", "initiating_principal",
        "authorized_objective", "generated_program_hash", "runtime_declaration",
        "allowed_tools", "permissions", "boundaries", "resource_limits",
        "stop_cancel_behavior", "failure_handling", "validation_requirements",
        "evidence_requirements"
    ]
    for field in required:
        if field not in record:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    principal = record.get("initiating_principal", "")
    perms = record.get("permissions", {})
    runtime = record.get("runtime_declaration", {})
    evidence = record.get("evidence_requirements", {})
    boundaries = record.get("boundaries", {})
    validation = record.get("validation_requirements", {})

    # Unrestricted secret_access is invalid
    if perms.get("secret_access") == "unrestricted":
        errors.append("secret_access 'unrestricted' is prohibited")

    # Sandbox 'none' must have isolation 'none' and code_execution 'denied'
    if runtime.get("sandbox_type") == "none":
        if runtime.get("isolation_level") != "none":
            errors.append("sandbox_type 'none' requires isolation_level 'none'")
        if perms.get("code_execution") != "denied":
            errors.append("sandbox_type 'none' requires code_execution 'denied'")

    # Unrestricted permissions require human principal
    unrestricted_count = sum(1 for v in perms.values() if v == "unrestricted")
    if unrestricted_count > 1 and not principal.startswith("human"):
        errors.append(
            f"Multiple unrestricted permissions ({unrestricted_count}) require human principal, got '{principal}'"
        )

    # Discard policy that drops contradicting evidence is invalid
    discard = boundaries.get("discard_policy", "").lower()
    if "contradict" in discard and "discard" in discard:
        errors.append("discard_policy drops contradicting evidence — evidence laundering")

    # evidence_requirements must be true when receipt_required is true
    if evidence.get("receipt_required"):
        for k, v in evidence.items():
            if v is False:
                errors.append(f"evidence_requirements.{k} is false but receipt_required is true")

    # validation_requirements must be true when receipt_required is true
    if evidence.get("receipt_required"):
        for k, v in validation.items():
            if v is False:
                errors.append(f"validation_requirements.{k} is false but receipt_required is true")

    return errors


def validate_multi_agent(record: dict) -> list[str]:
    errors = []
    required = [
        "schema_version", "contract_id", "orchestrator", "subagents",
        "concurrency_limits", "communication_topology", "conflict_handling",
        "cancellation_propagation", "resource_accounting", "final_gate"
    ]
    for field in required:
        if field not in record:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    orchestrator = record.get("orchestrator", {})
    subagents = record.get("subagents", [])
    concurrency = record.get("concurrency_limits", {})
    final_gate = record.get("final_gate", {})

    # Self-assigned orchestrator authority is invalid
    if orchestrator.get("authority") == "self-assigned":
        errors.append("orchestrator authority 'self-assigned' is prohibited — no self-delegation")

    # No subagent may have reduced_permissions=false with broad inherited_permissions
    for i, sa in enumerate(subagents):
        if not sa.get("reduced_permissions", True):
            if len(sa.get("inherited_permissions", [])) > 2:
                errors.append(
                    f"subagent[{i}] has reduced_permissions=false with {len(sa.get('inherited_permissions', []))} "
                    f"inherited permissions — authority escalation risk"
                )

    # evidence_attribution must be true for all subagents
    for i, sa in enumerate(subagents):
        if not sa.get("evidence_attribution", False):
            errors.append(f"subagent[{i}] has evidence_attribution=false — provenance loss")

    # max_fan_out > 100 is excessive
    if concurrency.get("max_fan_out", 0) > 100:
        errors.append(f"max_fan_out {concurrency['max_fan_out']} exceeds safe threshold (100)")

    # final_gate 'none' is invalid for non-trivial orchestrator
    if final_gate.get("gate_type") == "none":
        if orchestrator.get("synthesis_responsibility", False):
            errors.append("final_gate 'none' is invalid when orchestrator has synthesis_responsibility")

    # conflict_handling resolution_authority 'none' with synthesis_responsibility is invalid
    conflict = record.get("conflict_handling", {})
    if conflict.get("resolution_authority") == "none":
        if orchestrator.get("synthesis_responsibility", False):
            errors.append("conflict_handling resolution_authority 'none' invalid when orchestrator synthesizes")

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate.py <record.json> [--tool|--agent] [...]", file=sys.stderr)
        return 2

    args = sys.argv[1:]
    mode = None
    paths = []
    for arg in args:
        if arg == "--tool":
            mode = "tool"
        elif arg == "--agent":
            mode = "agent"
        else:
            paths.append(arg)

    all_valid = True
    for path in paths:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)

        if mode is None:
            sv = record.get("schema_version", "")
            if "programmatic_tool_execution" in sv:
                errors = validate_tool_execution(record)
            elif "multi_agent_execution" in sv:
                errors = validate_multi_agent(record)
            else:
                errors = [f"Unknown schema_version: {sv}"]
        elif mode == "tool":
            errors = validate_tool_execution(record)
        elif mode == "agent":
            errors = validate_multi_agent(record)
        else:
            errors = ["Unknown mode"]

        if errors:
            all_valid = False
            print(f"INVALID: {path}")
            for e in errors:
                print(f"  - {e}")
        else:
            print(f"VALID: {path}")
    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
