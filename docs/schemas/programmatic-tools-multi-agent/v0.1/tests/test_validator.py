#!/usr/bin/env python3
"""Tests for the Programmatic Tool Calling and Multi-Agent Execution validator."""

import json
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from validate import validate_tool_execution, validate_multi_agent

FIXTURES_DIR = Path(__file__).parent.parent / "fixtures"


def load_fixture(name: str) -> dict:
    with open(FIXTURES_DIR / name, encoding="utf-8") as f:
        return json.load(f)


class TestValidToolExecution(unittest.TestCase):
    def test_valid_tool_execution(self):
        errors = validate_tool_execution(load_fixture("valid-tool-execution.json"))
        self.assertEqual(errors, [], f"Expected no errors: {errors}")


class TestAdversarialToolExecution(unittest.TestCase):
    def test_adv_undeclared_tool_unrestricted(self):
        errors = validate_tool_execution(load_fixture("adv-undeclared-tool-unrestricted.json"))
        self.assertTrue(any("secret_access" in e for e in errors), f"Expected secret_access error: {errors}")
        self.assertTrue(any("human principal" in e for e in errors), f"Expected human principal error: {errors}")
        self.assertTrue(any("receipt_required" in e for e in errors), f"Expected evidence error: {errors}")

    def test_adv_evidence_drop(self):
        errors = validate_tool_execution(load_fixture("adv-evidence-drop.json"))
        self.assertTrue(any("evidence laundering" in e for e in errors), f"Expected laundering error: {errors}")
        self.assertTrue(any("discarded_data_policy_enforced" in e for e in errors), f"Expected discard policy error: {errors}")


class TestValidMultiAgent(unittest.TestCase):
    def test_valid_multi_agent(self):
        errors = validate_multi_agent(load_fixture("valid-multi-agent-execution.json"))
        self.assertEqual(errors, [], f"Expected no errors: {errors}")


class TestAdversarialMultiAgent(unittest.TestCase):
    def test_adv_permission_escalation(self):
        errors = validate_multi_agent(load_fixture("adv-permission-escalation.json"))
        self.assertTrue(any("self-assigned" in e for e in errors), f"Expected self-assigned error: {errors}")
        self.assertTrue(any("authority escalation" in e for e in errors), f"Expected escalation error: {errors}")
        self.assertTrue(any("evidence_attribution" in e for e in errors), f"Expected provenance error: {errors}")
        self.assertTrue(any("max_fan_out" in e for e in errors), f"Expected fanout error: {errors}")
        self.assertTrue(any("final_gate" in e for e in errors), f"Expected final_gate error: {errors}")

    def test_adv_excessive_fanout(self):
        errors = validate_multi_agent(load_fixture("adv-excessive-fanout.json"))
        self.assertTrue(any("max_fan_out" in e for e in errors), f"Expected fanout error: {errors}")

    def test_adv_no_provenance(self):
        errors = validate_multi_agent(load_fixture("adv-no-provenance.json"))
        self.assertTrue(any("evidence_attribution" in e for e in errors), f"Expected provenance error: {errors}")


class TestSemanticRules(unittest.TestCase):
    def test_unrestricted_secret_access_fails(self):
        r = {
            "schema_version": "programmatic_tool_execution.v0.1",
            "contract_id": "c1", "initiating_principal": "human",
            "authorized_objective": "o", "generated_program_hash": "h",
            "runtime_declaration": {"sandbox_type": "container", "isolation_level": "full", "ephemeral": True},
            "allowed_tools": [], "permissions": {
                "network": "denied", "filesystem": "denied", "subprocess": "denied",
                "code_execution": "denied", "secret_access": "unrestricted"
            },
            "boundaries": {"input_boundary": "x", "intermediate_data_boundary": "y",
                           "retained_intermediate_results": [], "discarded_intermediate_results": [],
                           "discard_policy": "none"},
            "resource_limits": {"max_steps": 1, "max_duration_seconds": 1, "max_tokens": 1, "max_cost_usd": 0.01},
            "stop_cancel_behavior": {"cancel_propagation": "immediate", "partial_result_policy": "discard"},
            "failure_handling": {"on_tool_failure": "abort", "on_budget_exceeded": "abort"},
            "validation_requirements": {"output_validation": True, "tool_scope_verification": True},
            "evidence_requirements": {"tool_invocations_logged": True, "material_decisions_logged": True,
                                      "discarded_data_policy_enforced": True, "receipt_required": False}
        }
        errors = validate_tool_execution(r)
        self.assertTrue(any("secret_access" in e for e in errors))

    def test_sandbox_none_requires_denied_code_execution(self):
        r = {
            "schema_version": "programmatic_tool_execution.v0.1",
            "contract_id": "c1", "initiating_principal": "human",
            "authorized_objective": "o", "generated_program_hash": "h",
            "runtime_declaration": {"sandbox_type": "none", "isolation_level": "full", "ephemeral": True},
            "allowed_tools": [], "permissions": {
                "network": "denied", "filesystem": "denied", "subprocess": "denied",
                "code_execution": "sandboxed", "secret_access": "prohibited"
            },
            "boundaries": {"input_boundary": "x", "intermediate_data_boundary": "y",
                           "retained_intermediate_results": [], "discarded_intermediate_results": [],
                           "discard_policy": "none"},
            "resource_limits": {"max_steps": 1, "max_duration_seconds": 1, "max_tokens": 1, "max_cost_usd": 0.01},
            "stop_cancel_behavior": {"cancel_propagation": "immediate", "partial_result_policy": "discard"},
            "failure_handling": {"on_tool_failure": "abort", "on_budget_exceeded": "abort"},
            "validation_requirements": {"output_validation": True, "tool_scope_verification": True},
            "evidence_requirements": {"tool_invocations_logged": True, "material_decisions_logged": True,
                                      "discarded_data_policy_enforced": True, "receipt_required": False}
        }
        errors = validate_tool_execution(r)
        self.assertTrue(any("code_execution" in e for e in errors))
        self.assertTrue(any("isolation_level" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
