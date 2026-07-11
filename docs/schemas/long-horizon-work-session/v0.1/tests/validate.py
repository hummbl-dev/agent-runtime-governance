#!/usr/bin/env python3
"""Long-Horizon Work Session validator v0.1.

Validates contracts against schema and enforces semantic rules:

- Unrestricted credential_posture is prohibited
- Unrestricted computer_use_access requires human confirmation
- All destructive/financial/admin/credential/production gates must be 'confirm' or 'deny'
- Route ladder must prefer structured_api first
- computer_use before structured_api in route ladder is invalid
- route_selection_receipted must be true
- overlap_prevention and idempotency_protection must be true for scheduled sessions
- All receipt_requirements must be true
- Self-initiated authority with unrestricted capabilities is invalid

Uses only Python stdlib.
"""

import json
import sys
from pathlib import Path


def validate_work_session(record: dict) -> list[str]:
    errors = []
    required = [
        "schema_version", "session_id", "initiating_authority",
        "authorized_objective", "current_state", "capability_declaration",
        "approval_policy", "route_ladder", "checkpoint_policy", "receipt_requirements"
    ]
    for field in required:
        if field not in record:
            errors.append(f"Missing required field: {field}")
    if errors:
        return errors

    caps = record.get("capability_declaration", {})
    approval = record.get("approval_policy", {})
    route = record.get("route_ladder", {})
    checkpoint = record.get("checkpoint_policy", {})
    receipt = record.get("receipt_requirements", {})
    authority = record.get("initiating_authority", "")

    # Unrestricted credential_posture is prohibited
    if caps.get("credential_posture") == "unrestricted":
        errors.append("credential_posture 'unrestricted' is prohibited")

    # Unrestricted computer_use_access requires human confirmation
    if caps.get("computer_use_access") == "unrestricted":
        if approval.get("desktop_gate") not in ("confirm", "deny"):
            errors.append("computer_use_access 'unrestricted' requires desktop_gate 'confirm' or 'deny'")

    # Destructive/financial/admin/credential/production gates must be confirm or deny
    for gate in ["destructive_gate", "financial_gate", "admin_gate", "credential_gate", "production_gate"]:
        if gate in approval:
            if approval[gate] == "auto":
                errors.append(f"{gate} 'auto' is prohibited — must be 'confirm' or 'deny'")

    # Route ladder must prefer structured_api first
    order = route.get("preferred_order", [])
    if order and order[0] != "structured_api":
        errors.append(f"route_ladder preferred_order[0] is '{order[0]}', must be 'structured_api'")

    # computer_use before structured_api in route ladder is invalid
    if "computer_use" in order and "structured_api" in order:
        if order.index("computer_use") < order.index("structured_api"):
            errors.append("computer_use appears before structured_api in route ladder — premature GUI automation")

    # route_selection_receipted must be true
    if not route.get("route_selection_receipted", False):
        errors.append("route_selection_receipted must be true")

    # overlap_prevention and idempotency_protection must be true for scheduled sessions
    if caps.get("schedule_event_trigger_support", False):
        if not checkpoint.get("overlap_prevention", False):
            errors.append("overlap_prevention must be true when schedule_event_trigger_support is true")
        if not checkpoint.get("idempotency_protection", False):
            errors.append("idempotency_protection must be true when schedule_event_trigger_support is true")

    # All receipt_requirements must be true
    for k, v in receipt.items():
        if v is False:
            errors.append(f"receipt_requirements.{k} is false — all receipt fields must be true")

    # Self-initiated authority with unrestricted capabilities is invalid
    unrestricted_caps = sum(1 for k, v in caps.items()
                           if v == "unrestricted" and k in
                           ("browser_access", "local_file_access", "computer_use_access",
                            "network_policy", "credential_posture"))
    if authority == "agent-self" and unrestricted_caps > 1:
        errors.append(
            f"Self-initiated authority with {unrestricted_caps} unrestricted capabilities is prohibited"
        )

    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate.py <record.json> [...]", file=sys.stderr)
        return 2

    all_valid = True
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)

        errors = validate_work_session(record)

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
