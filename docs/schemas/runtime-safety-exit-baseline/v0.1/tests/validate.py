#!/usr/bin/env python3
"""Agent Runtime Safety and Exit Baseline validator v0.1.

Validates runtime baseline records against the schema and enforces
semantic rules from the spec:

- ADOPT disposition requires default_deny egress and fail_closed
- ADOPT disposition requires ephemeral workspace and reset verified
- ADOPT disposition requires scoped or denied subagent forwarding
- ADOPT disposition requires export_verified and no runtime-locked critical formats
- ADOPT disposition requires all exit tests passed
- blocklist posture cannot be classified as ADOPT (it's not default_deny)
- unrestricted egress cannot be ADOPT or TRIAL
- unrestricted subagent_forwarding cannot be ADOPT
- REJECT disposition should have residual_risk entries

Uses only Python stdlib.
"""

import json
import sys
from pathlib import Path


REQUIRED_FIELDS = [
    "schema_version", "runtime_id", "version", "assessment_date",
    "session_identity", "workspace", "egress", "credentials",
    "side_effects", "artifacts", "exit", "receipts",
    "disposition", "residual_risk"
]

VALID_DISPOSITIONS = {"ADOPT", "TRIAL", "ASSESS", "HOLD", "COMPOSE", "REJECT"}
VALID_EGRESS = {"default_deny", "allowlist", "blocklist", "unrestricted", "unknown"}
VALID_FORWARDING = {"denied", "scoped", "unrestricted", "unknown"}
VALID_PERSISTENCE = {"session", "process", "workspace", "persistent", "unknown"}

CRITICAL_LOCKED_FORMATS = {"prompts", "memory", "receipts", "workflows", "policies"}


def _check_required(record: dict) -> list[str]:
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in record:
            errors.append(f"Missing required field: {field}")
    return errors


def _check_enums(record: dict) -> list[str]:
    errors = []
    if record.get("disposition") not in VALID_DISPOSITIONS:
        errors.append(f"Invalid disposition: {record.get('disposition')}")
    if record.get("egress", {}).get("posture") not in VALID_EGRESS:
        errors.append(f"Invalid egress posture: {record.get('egress', {}).get('posture')}")
    fwd = record.get("credentials", {}).get("subagent_forwarding")
    if fwd not in VALID_FORWARDING:
        errors.append(f"Invalid subagent_forwarding: {fwd}")
    pb = record.get("session_identity", {}).get("persistence_boundary")
    if pb not in VALID_PERSISTENCE:
        errors.append(f"Invalid persistence_boundary: {pb}")
    return errors


def _check_adopt_requirements(record: dict) -> list[str]:
    """ADOPT disposition requires the strongest controls."""
    errors = []
    if record.get("disposition") != "ADOPT":
        return errors

    egress = record.get("egress", {})
    if egress.get("posture") != "default_deny":
        errors.append(
            f"disposition is ADOPT but egress posture is '{egress.get('posture')}' "
            f"(must be default_deny)"
        )
    if not egress.get("fail_closed"):
        errors.append("disposition is ADOPT but egress fail_closed is false")

    workspace = record.get("workspace", {})
    if not workspace.get("ephemeral_default"):
        errors.append("disposition is ADOPT but workspace.ephemeral_default is false")
    if not workspace.get("reset_verified"):
        errors.append("disposition is ADOPT but workspace.reset_verified is false")

    creds = record.get("credentials", {})
    if creds.get("subagent_forwarding") not in ("denied", "scoped"):
        errors.append(
            f"disposition is ADOPT but subagent_forwarding is '{creds.get('subagent_forwarding')}' "
            f"(must be denied or scoped)"
        )

    artifacts = record.get("artifacts", {})
    if not artifacts.get("export_verified"):
        errors.append("disposition is ADOPT but artifacts.export_verified is false")
    locked = set(artifacts.get("runtime_locked_formats", []))
    critical_locked = locked & CRITICAL_LOCKED_FORMATS
    if critical_locked:
        errors.append(
            f"disposition is ADOPT but critical formats are runtime-locked: {critical_locked}"
        )

    exit_ = record.get("exit", {})
    for field in ["uninstall_tested", "state_cleanup_tested", "credential_revocation_tested"]:
        if not exit_.get(field):
            errors.append(f"disposition is ADOPT but exit.{field} is false")
    if not exit_.get("alternate_runtime_tested"):
        errors.append("disposition is ADOPT but exit.alternate_runtime_tested is null/missing")

    return errors


def _check_egress_posture_consistency(record: dict) -> list[str]:
    """Unrestricted egress cannot be ADOPT or TRIAL."""
    errors = []
    egress = record.get("egress", {})
    posture = egress.get("posture", "")
    disposition = record.get("disposition", "")

    if posture == "unrestricted" and disposition in ("ADOPT", "TRIAL"):
        errors.append(
            f"egress posture is 'unrestricted' but disposition is {disposition} "
            f"(must be ASSESS, HOLD, COMPOSE, or REJECT)"
        )

    if posture == "blocklist" and disposition == "ADOPT":
        errors.append(
            "egress posture is 'blocklist' but disposition is ADOPT "
            "(blocklist is not default_deny)"
        )
    return errors


def _check_credential_forwarding(record: dict) -> list[str]:
    """Unrestricted subagent forwarding cannot be ADOPT."""
    errors = []
    fwd = record.get("credentials", {}).get("subagent_forwarding", "")
    disposition = record.get("disposition", "")

    if fwd == "unrestricted" and disposition == "ADOPT":
        errors.append(
            "subagent_forwarding is 'unrestricted' but disposition is ADOPT "
            "(must be denied or scoped for ADOPT)"
        )
    return errors


def _check_reject_has_risks(record: dict) -> list[str]:
    """REJECT disposition should document residual risks."""
    errors = []
    if record.get("disposition") == "REJECT":
        if not record.get("residual_risk"):
            errors.append("disposition is REJECT but residual_risk is empty")
    return errors


def _check_side_effect_gates(record: dict) -> list[str]:
    """Live action classes should have human gates (not checked for REJECT)."""
    errors = []
    if record.get("disposition") == "REJECT":
        return errors
    se = record.get("side_effects", {})
    live_classes = se.get("live_action_classes", [])
    human_gates = se.get("human_gates", [])

    if live_classes and not human_gates:
        errors.append(
            f"side_effects has live_action_classes ({live_classes}) "
            f"but no human_gates"
        )
    return errors


def validate_record(record: dict) -> list[str]:
    errors = []
    errors.extend(_check_required(record))
    if errors:
        return errors
    errors.extend(_check_enums(record))
    errors.extend(_check_adopt_requirements(record))
    errors.extend(_check_egress_posture_consistency(record))
    errors.extend(_check_credential_forwarding(record))
    errors.extend(_check_reject_has_risks(record))
    errors.extend(_check_side_effect_gates(record))
    return errors


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate.py <record.json> [...]", file=sys.stderr)
        return 2
    all_valid = True
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as f:
            record = json.load(f)
        errors = validate_record(record)
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
