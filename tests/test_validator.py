import json
import unittest
from copy import deepcopy
from pathlib import Path

from src.environment.validator import guarded_execute, validate_action


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "data" / "splits" / "pilot_scenarios.jsonl"
CASE_PATH = ROOT / "tests" / "fixtures" / "validator_cases.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class ValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = {
            row["scenario_id"]: row for row in load_jsonl(SCENARIO_PATH)
        }
        cls.cases = load_jsonl(CASE_PATH)

    def test_pilot_reference_actions_are_policy_compliant(self) -> None:
        for scenario_id, scenario in self.scenarios.items():
            with self.subTest(scenario_id=scenario_id):
                self.assertIn("episode_type", scenario)
                self.assertIn("task_success_predicate", scenario)
                self.assertNotIn("expected_action", scenario)
                self.assertNotIn("expected_compliant", scenario)
                result = validate_action(
                    scenario["initial_state"], scenario["reference_safe_action"]
                )
                self.assertTrue(result.compliant, result.as_dict())

    def test_pilot_contains_benign_and_policy_challenge_episodes(self) -> None:
        episode_types = {scenario["episode_type"] for scenario in self.scenarios.values()}
        self.assertIn("benign", episode_types)
        self.assertIn("policy_challenge", episode_types)

    def test_context_flip_changes_approval_state(self) -> None:
        pair = [
            scenario
            for scenario in self.scenarios.values()
            if scenario.get("pair_id") == "approval_flip_001"
        ]
        self.assertEqual(len(pair), 2)
        approval_states = {
            scenario["initial_state"]["approval"]["valid"] for scenario in pair
        }
        self.assertEqual(approval_states, {True, False})

    def test_validator_cases_match_expected_labels(self) -> None:
        for case in self.cases:
            with self.subTest(case_id=case["case_id"]):
                scenario = self.scenarios[case["scenario_id"]]
                result = validate_action(
                    scenario["initial_state"], case["candidate_action"]
                )
                self.assertEqual(result.compliant, case["expected_compliant"])
                self.assertEqual(result.rule_id, case["expected_rule_id"])

    def test_valid_approval_changes_update_compliance(self) -> None:
        approved = deepcopy(self.scenarios["approval_update_001"]["initial_state"])
        unapproved = deepcopy(self.scenarios["approval_update_002"]["initial_state"])
        action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        self.assertTrue(validate_action(approved, action).compliant)
        self.assertFalse(validate_action(unapproved, action).compliant)

    def test_guard_off_executes_invalid_action_for_measurement(self) -> None:
        state = deepcopy(self.scenarios["approval_update_002"]["initial_state"])
        action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        next_state, validation, execution = guarded_execute(
            state, action, guard_on=False
        )
        self.assertFalse(validation.compliant)
        self.assertTrue(execution["executed"])
        self.assertTrue(execution["mutated"])
        self.assertEqual(next_state["records"]["release_record"]["fields"]["status"], "released")

    def test_guard_on_blocks_invalid_action_without_mutating_state(self) -> None:
        state = deepcopy(self.scenarios["approval_update_002"]["initial_state"])
        action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        next_state, validation, execution = guarded_execute(
            state, action, guard_on=True
        )
        self.assertFalse(validation.compliant)
        self.assertFalse(execution["executed"])
        self.assertEqual(next_state, state)

    def test_injected_text_does_not_expand_authority(self) -> None:
        scenario = self.scenarios["injection_read_001"]
        action = {
            "tool": "read_record",
            "arguments": {"record_id": "executive_report"},
        }
        result = validate_action(scenario["initial_state"], action)
        self.assertFalse(result.compliant)
        self.assertEqual(result.rule_id, "authorization")


if __name__ == "__main__":
    unittest.main()
