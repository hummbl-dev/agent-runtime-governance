#!/usr/bin/env python3
"""Tests for the Long-Horizon Work Session validator."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import validate_work_session

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


class TestValidFixtures(unittest.TestCase):
    def test_valid_work_session(self):
        errors = validate_work_session(load_fixture("valid-work-session.json"))
        self.assertEqual(errors, [], f"Expected no errors: {errors}")

    def test_degraded_app_unavailable(self):
        errors = validate_work_session(load_fixture("degraded-app-unavailable.json"))
        self.assertEqual(errors, [], f"Expected no errors: {errors}")


class TestAdversarialFixtures(unittest.TestCase):
    def test_adv_credential_access(self):
        errors = validate_work_session(load_fixture("adv-credential-access.json"))
        self.assertTrue(any("credential_posture" in e for e in errors), f"Expected credential error: {errors}")
        self.assertTrue(any("destructive_gate" in e for e in errors), f"Expected destructive_gate error: {errors}")
        self.assertTrue(any("financial_gate" in e for e in errors), f"Expected financial_gate error: {errors}")
        self.assertTrue(any("admin_gate" in e for e in errors), f"Expected admin_gate error: {errors}")
        self.assertTrue(any("credential_gate" in e for e in errors), f"Expected credential_gate error: {errors}")
        self.assertTrue(any("production_gate" in e for e in errors), f"Expected production_gate error: {errors}")
        self.assertTrue(any("structured_api" in e for e in errors), f"Expected route ladder error: {errors}")
        self.assertTrue(any("route_selection_receipted" in e for e in errors), f"Expected receipted error: {errors}")
        self.assertTrue(any("receipt_requirements" in e for e in errors), f"Expected receipt error: {errors}")
        self.assertTrue(any("Self-initiated" in e for e in errors), f"Expected self-init error: {errors}")

    def test_adv_scheduled_overlap(self):
        errors = validate_work_session(load_fixture("adv-scheduled-overlap.json"))
        self.assertTrue(any("overlap_prevention" in e for e in errors), f"Expected overlap error: {errors}")
        self.assertTrue(any("idempotency_protection" in e for e in errors), f"Expected idempotency error: {errors}")

    def test_adv_premature_computer_use(self):
        errors = validate_work_session(load_fixture("adv-premature-computer-use.json"))
        self.assertTrue(any("premature" in e.lower() for e in errors), f"Expected premature error: {errors}")


class TestSemanticRules(unittest.TestCase):
    def test_unrestricted_credential_posture_fails(self):
        r = {
            "schema_version": "long_horizon_work_session.v0.1",
            "session_id": "s1", "initiating_authority": "human",
            "authorized_objective": "o", "current_state": "running",
            "capability_declaration": {
                "available_apps": [], "browser_access": "denied",
                "local_file_access": "denied", "computer_use_access": "denied",
                "network_policy": "denied", "artifact_types": [],
                "credential_posture": "unrestricted",
                "max_duration_seconds": 60, "max_cost_usd": 0.01
            },
            "approval_policy": {
                "read_gate": "auto", "mutation_gate": "deny", "message_gate": "deny",
                "schedule_gate": "deny", "browser_gate": "deny", "desktop_gate": "deny",
                "publish_gate": "deny", "destructive_gate": "deny"
            },
            "route_ladder": {
                "preferred_order": ["structured_api"],
                "route_selection_receipted": True
            },
            "checkpoint_policy": {
                "checkpoint_enabled": True, "resume_supported": True, "stale_detection": True
            },
            "receipt_requirements": {
                "session_identity_logged": True, "capabilities_logged": True,
                "plan_logged": True, "mutations_logged": True,
                "checkpoints_logged": True, "failures_logged": True
            }
        }
        errors = validate_work_session(r)
        self.assertTrue(any("credential_posture" in e for e in errors))

    def test_auto_destructive_gate_fails(self):
        r = {
            "schema_version": "long_horizon_work_session.v0.1",
            "session_id": "s1", "initiating_authority": "human",
            "authorized_objective": "o", "current_state": "running",
            "capability_declaration": {
                "available_apps": [], "browser_access": "denied",
                "local_file_access": "denied", "computer_use_access": "denied",
                "network_policy": "denied", "artifact_types": [],
                "credential_posture": "prohibited",
                "max_duration_seconds": 60, "max_cost_usd": 0.01
            },
            "approval_policy": {
                "read_gate": "auto", "mutation_gate": "deny", "message_gate": "deny",
                "schedule_gate": "deny", "browser_gate": "deny", "desktop_gate": "deny",
                "publish_gate": "deny", "destructive_gate": "auto"
            },
            "route_ladder": {
                "preferred_order": ["structured_api"],
                "route_selection_receipted": True
            },
            "checkpoint_policy": {
                "checkpoint_enabled": True, "resume_supported": True, "stale_detection": True
            },
            "receipt_requirements": {
                "session_identity_logged": True, "capabilities_logged": True,
                "plan_logged": True, "mutations_logged": True,
                "checkpoints_logged": True, "failures_logged": True
            }
        }
        errors = validate_work_session(r)
        self.assertTrue(any("destructive_gate" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
