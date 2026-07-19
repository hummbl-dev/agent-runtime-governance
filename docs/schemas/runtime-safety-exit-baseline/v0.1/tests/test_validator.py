#!/usr/bin/env python3
"""Tests for the Agent Runtime Safety and Exit Baseline validator."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import validate_record

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


class TestValidRecords(unittest.TestCase):
    def test_valid_trial_baseline(self):
        errors = validate_record(load_fixture("valid-trial-baseline.json"))
        self.assertEqual(errors, [], f"Expected no errors: {errors}")


class TestInvalidRecords(unittest.TestCase):
    def test_invalid_unrestricted_egress(self):
        """Unrestricted egress with REJECT should pass validation (REJECT is honest)."""
        errors = validate_record(load_fixture("invalid-unrestricted-egress.json"))
        self.assertEqual(errors, [], f"REJECT with unrestricted egress should be valid: {errors}")

    def test_invalid_blocklist_as_default_deny(self):
        """Blocklist posture cannot be ADOPT."""
        errors = validate_record(load_fixture("invalid-blocklist-as-default-deny.json"))
        self.assertTrue(any("blocklist" in e for e in errors),
                        f"Expected blocklist error: {errors}")

    def test_invalid_credential_forwarding(self):
        """Unrestricted subagent forwarding cannot be ADOPT."""
        errors = validate_record(load_fixture("invalid-credential-forwarding.json"))
        self.assertTrue(any("subagent_forwarding" in e for e in errors),
                        f"Expected forwarding error: {errors}")


class TestSemanticRules(unittest.TestCase):
    def _base_record(self) -> dict:
        return {
            "schema_version": "agent_runtime_safety_exit_baseline.v0.1",
            "runtime_id": "test-runtime",
            "version": "1.0",
            "assessment_date": "2026-07-10",
            "session_identity": {
                "unique_per_session": True,
                "attributable": True,
                "persistence_boundary": "session"
            },
            "workspace": {
                "ephemeral_default": True,
                "reset_verified": True,
                "mounted_paths": []
            },
            "egress": {
                "posture": "default_deny",
                "allowed_destinations": [],
                "fail_closed": True,
                "bypass_tests": []
            },
            "credentials": {
                "credential_classes": [],
                "short_lived_supported": True,
                "subagent_forwarding": "denied"
            },
            "side_effects": {
                "synthetic_default": True,
                "live_action_classes": [],
                "human_gates": []
            },
            "artifacts": {
                "user_controlled_formats": ["json"],
                "runtime_locked_formats": [],
                "export_verified": True
            },
            "exit": {
                "uninstall_tested": True,
                "state_cleanup_tested": True,
                "credential_revocation_tested": True,
                "alternate_runtime_tested": "alt"
            },
            "receipts": {
                "raw_trace_ref": None,
                "evidence_ref": None,
                "result_ref": None
            },
            "disposition": "ADOPT",
            "residual_risk": []
        }

    def test_adopt_requires_default_deny(self):
        r = self._base_record()
        r["egress"]["posture"] = "allowlist"
        errors = validate_record(r)
        self.assertTrue(any("default_deny" in e for e in errors))

    def test_adopt_requires_ephemeral_workspace(self):
        r = self._base_record()
        r["workspace"]["ephemeral_default"] = False
        errors = validate_record(r)
        self.assertTrue(any("ephemeral_default" in e for e in errors))

    def test_adopt_requires_scoped_forwarding(self):
        r = self._base_record()
        r["credentials"]["subagent_forwarding"] = "unrestricted"
        errors = validate_record(r)
        self.assertTrue(any("subagent_forwarding" in e for e in errors))

    def test_adopt_requires_export_verified(self):
        r = self._base_record()
        r["artifacts"]["export_verified"] = False
        errors = validate_record(r)
        self.assertTrue(any("export_verified" in e for e in errors))

    def test_adopt_rejects_locked_critical_formats(self):
        r = self._base_record()
        r["artifacts"]["runtime_locked_formats"] = ["memory", "receipts"]
        errors = validate_record(r)
        self.assertTrue(any("runtime-locked" in e for e in errors))

    def test_unrestricted_egress_cannot_be_trial(self):
        r = self._base_record()
        r["egress"]["posture"] = "unrestricted"
        r["disposition"] = "TRIAL"
        errors = validate_record(r)
        self.assertTrue(any("unrestricted" in e for e in errors))

    def test_reject_requires_residual_risk(self):
        r = self._base_record()
        r["disposition"] = "REJECT"
        r["residual_risk"] = []
        errors = validate_record(r)
        self.assertTrue(any("residual_risk" in e for e in errors))

    def test_live_actions_require_human_gates(self):
        r = self._base_record()
        r["side_effects"]["live_action_classes"] = ["email", "db-write"]
        r["side_effects"]["human_gates"] = []
        errors = validate_record(r)
        self.assertTrue(any("human_gates" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
