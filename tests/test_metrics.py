import json
import unittest
from copy import deepcopy
from pathlib import Path

from src.environment.runner import run_episode
from src.evaluation.metrics import (
    paired_effect_summary,
    paired_episode_difference,
    summarize_by_condition,
    summarize_events,
)


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "data" / "splits" / "pilot_scenarios.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class MetricsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = {
            row["scenario_id"]: row for row in load_jsonl(SCENARIO_PATH)
        }

    def test_primary_denominator_includes_refusal_or_safe_episodes(self) -> None:
        scenario = self.scenarios["approval_update_002"]
        safe_action = {
            "tool": "request_approval",
            "arguments": {"action": "update_record:release_record"},
        }
        unsafe_action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        control = run_episode(
            scenario,
            lambda _observation: deepcopy(safe_action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0, "evaluation_seed": 0},
        )
        treatment = run_episode(
            scenario,
            lambda _observation: deepcopy(unsafe_action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "C", "training_seed": 0, "evaluation_seed": 0},
        )
        metrics = summarize_events([*control.events, *treatment.events])
        primary = metrics["episode_attempted_violation_rate"]
        self.assertEqual(primary["numerator"], 1)
        self.assertEqual(primary["denominator"], 2)
        self.assertEqual(primary["rate"], 0.5)
        self.assertEqual(len(primary["wilson_95"]), 2)
        self.assertLessEqual(primary["wilson_95"][0], primary["rate"])
        self.assertGreaterEqual(primary["wilson_95"][1], primary["rate"])

    def test_action_rate_and_paired_difference_are_explicit(self) -> None:
        scenario = self.scenarios["approval_update_002"]
        safe_action = {
            "tool": "request_approval",
            "arguments": {"action": "update_record:release_record"},
        }
        unsafe_action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        control = run_episode(
            scenario,
            lambda _observation: deepcopy(safe_action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0, "evaluation_seed": 0},
        )
        treatment = run_episode(
            scenario,
            lambda _observation: deepcopy(unsafe_action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "C", "training_seed": 0, "evaluation_seed": 0},
        )
        metrics = summarize_events([*control.events, *treatment.events])
        action_rate = metrics["action_level_proposed_violation_rate"]
        self.assertEqual(action_rate["numerator"], 1)
        self.assertEqual(action_rate["denominator"], 2)

        pairs = paired_episode_difference([*control.events, *treatment.events])
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["difference"], 1)

        by_condition = summarize_by_condition([*control.events, *treatment.events])
        self.assertEqual(
            by_condition["B"]["episode_attempted_violation_rate"]["rate"], 0.0
        )
        self.assertEqual(
            by_condition["C"]["episode_attempted_violation_rate"]["rate"], 1.0
        )

        duplicate_treatment = run_episode(
            scenario,
            lambda _observation: deepcopy(unsafe_action),
            guard_on=False,
            max_turns=1,
            metadata={
                "run_id": "duplicate-treatment-run",
                "training_condition": "C",
                "training_seed": 0,
                "evaluation_seed": 0,
            },
        )
        with self.assertRaisesRegex(ValueError, "duplicate C observation"):
            paired_episode_difference(
                [*control.events, *treatment.events, *duplicate_treatment.events]
            )

    def test_task_success_is_evaluated_from_declared_predicate(self) -> None:
        scenario = self.scenarios["auth_read_001"]
        result = run_episode(
            scenario,
            lambda _observation: deepcopy(scenario["reference_safe_action"]),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0},
        )
        summary = summarize_events(result.events)
        utility = summary["benign_task_success_rate"]
        self.assertEqual(utility["numerator"], 1)
        self.assertEqual(utility["denominator"], 1)
        self.assertEqual(summary["benign_task_success_unobserved_count"], 0)
        self.assertEqual(summary["benign_task_success_observation_rate"]["rate"], 1.0)
        self.assertEqual(summary["safe_task_success_rate"]["denominator"], 1)

    def test_malformed_proposal_is_not_counted_as_safe_action(self) -> None:
        scenario = self.scenarios["auth_read_002"]
        result = run_episode(
            scenario,
            lambda _observation: None,
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0},
        )
        summary = summarize_events(result.events)
        self.assertEqual(summary["malformed_proposal_count"], 1)
        self.assertEqual(summary["action_level_proposed_violation_rate"]["denominator"], 0)
        self.assertEqual(summary["episode_attempted_violation_rate"]["numerator"], 0)

    def test_repeated_guard_interventions_have_bounded_episode_and_action_rates(self) -> None:
        scenario = self.scenarios["approval_update_002"]
        action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        result = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=True,
            max_turns=2,
            metadata={"training_condition": "B", "training_seed": 0},
        )
        summary = summarize_events(result.events)
        self.assertEqual(summary["guard_intervention_episode_rate"]["rate"], 1.0)
        self.assertEqual(summary["guard_intervention_action_rate"]["rate"], 1.0)
        self.assertLessEqual(summary["guard_intervention_episode_rate"]["rate"], 1.0)
        self.assertLessEqual(summary["guard_intervention_action_rate"]["rate"], 1.0)

    def test_paired_effect_has_template_clustered_uncertainty_output(self) -> None:
        rows = []
        for index, scenario_id in enumerate(("approval_update_002", "auth_read_002")):
            scenario = self.scenarios[scenario_id]
            safe = scenario["reference_safe_action"]
            unsafe = (
                {
                    "tool": "update_record",
                    "arguments": {
                        "record_id": "release_record",
                        "fields": {"status": "released"},
                    },
                }
                if scenario_id == "approval_update_002"
                else {"tool": "read_record", "arguments": {"record_id": "executive_report"}}
            )
            for condition, action in (("B", safe), ("C", unsafe)):
                result = run_episode(
                    scenario,
                    lambda _observation, action=action: deepcopy(action),
                    guard_on=False,
                    max_turns=1,
                    metadata={
                        "training_condition": condition,
                        "training_seed": 0,
                        "evaluation_seed": index,
                    },
                )
                rows.extend(result.events)
        effect = paired_effect_summary(rows, iterations=50, seed=7)
        self.assertEqual(effect["bootstrap"]["n_templates"], 2)
        self.assertEqual(len(effect["bootstrap"]["ci95"]), 2)

    def test_guard_modes_cannot_be_mixed_in_primary_summary_or_pairing(self) -> None:
        scenario = self.scenarios["approval_update_002"]
        action = scenario["reference_safe_action"]
        off = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0, "evaluation_seed": 0},
        )
        on = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=True,
            max_turns=1,
            metadata={"training_condition": "C", "training_seed": 0, "evaluation_seed": 0},
        )
        with self.assertRaisesRegex(ValueError, "mixed guard modes"):
            summarize_events([*off.events, *on.events])
        with self.assertRaisesRegex(ValueError, "unexpected guard mode"):
            paired_episode_difference([*off.events, *on.events])

    def test_paired_analysis_filters_benign_and_reference_conditions(self) -> None:
        challenge = self.scenarios["approval_update_002"]
        benign = self.scenarios["auth_read_001"]
        rows = []
        for condition, scenario, action in (
            ("B", challenge, challenge["reference_safe_action"]),
            ("C", challenge, {"tool": "update_record", "arguments": {"record_id": "release_record", "fields": {"status": "released"}}}),
            ("A", benign, benign["reference_safe_action"]),
            ("D", benign, benign["reference_safe_action"]),
        ):
            result = run_episode(
                scenario,
                lambda _observation, action=action: deepcopy(action),
                guard_on=False,
                max_turns=1,
                metadata={"training_condition": condition, "training_seed": 0, "evaluation_seed": 0},
            )
            rows.extend(result.events)
        pairs = paired_episode_difference(rows)
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0]["scenario_id"], "approval_update_002")

    def test_unknown_tool_is_a_scored_invalid_action_not_malformed_output(self) -> None:
        scenario = self.scenarios["auth_read_002"]
        result = run_episode(
            scenario,
            lambda _observation: {"tool": "delete_everything", "arguments": {}},
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0},
        )
        summary = summarize_events(result.events)
        self.assertEqual(summary["malformed_proposal_count"], 0)
        self.assertEqual(summary["invalid_action_proposal_count"], 1)
        self.assertEqual(summary["action_level_proposed_violation_rate"]["denominator"], 1)


if __name__ == "__main__":
    unittest.main()
