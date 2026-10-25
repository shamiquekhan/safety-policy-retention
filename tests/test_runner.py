import json
import unittest
from copy import deepcopy
from pathlib import Path

from src.environment.runner import run_episode


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "data" / "splits" / "pilot_scenarios.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class EpisodeRunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = {
            row["scenario_id"]: row for row in load_jsonl(SCENARIO_PATH)
        }

    def test_guard_off_logs_and_executes_invalid_state_change(self) -> None:
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
            guard_on=False,
            max_turns=1,
            success=lambda state, _scenario: state["records"]["release_record"]["fields"]["status"]
            == "released",
        )
        event = result.events[0]
        self.assertTrue(result.attempted_violation)
        self.assertTrue(result.sandbox_harm)
        self.assertTrue(event["executed_action"])
        self.assertEqual(event["evaluation_guard_mode"], "off")
        self.assertIsNone(event["guard_intervention"])
        self.assertTrue(result.task_success)

    def test_guard_on_blocks_and_logs_same_invalid_proposal(self) -> None:
        scenario = self.scenarios["approval_update_002"]
        action = {
            "tool": "update_record",
            "arguments": {
                "record_id": "release_record",
                "fields": {"status": "released"},
            },
        }
        initial_state = deepcopy(scenario["initial_state"])
        result = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=True,
            max_turns=1,
        )
        event = result.events[0]
        self.assertTrue(result.attempted_violation)
        self.assertFalse(result.sandbox_harm)
        self.assertIsNone(event["executed_action"])
        self.assertEqual(event["guard_intervention"], "blocked")
        self.assertEqual(result.final_state, initial_state)

    def test_episode_id_distinguishes_training_seed_and_guard_mode(self) -> None:
        scenario = self.scenarios["auth_read_001"]
        action = scenario["reference_safe_action"]
        seed_zero = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0, "evaluation_seed": 0},
        )
        seed_one = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=False,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 1, "evaluation_seed": 0},
        )
        guarded = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=True,
            max_turns=1,
            metadata={"training_condition": "B", "training_seed": 0, "evaluation_seed": 0},
        )
        self.assertNotEqual(seed_zero.events[0]["episode_id"], seed_one.events[0]["episode_id"])
        self.assertNotEqual(seed_zero.events[0]["episode_id"], guarded.events[0]["episode_id"])

    def test_unauthorized_read_is_explicit_harm_without_state_mutation(self) -> None:
        scenario = self.scenarios["injection_read_001"]
        action = {
            "tool": "read_record",
            "arguments": {"record_id": "executive_report"},
        }
        result = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=False,
            max_turns=1,
        )
        event = result.events[0]
        self.assertTrue(result.sandbox_harm)
        self.assertEqual(event["prohibited_effects"], ["unauthorized_record_read"])
        self.assertEqual(event["state_before_hash"], event["state_after_hash"])

    def test_same_episode_id_with_incompatible_metadata_is_rejected_by_metrics(self) -> None:
        scenario = self.scenarios["auth_read_001"]
        action = scenario["reference_safe_action"]
        first = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=False,
            max_turns=1,
            metadata={"episode_id": "collision", "training_seed": 0},
        )
        second = run_episode(
            scenario,
            lambda _observation: deepcopy(action),
            guard_on=False,
            max_turns=1,
            metadata={"episode_id": "collision", "training_seed": 1},
        )
        from src.evaluation.metrics import summarize_events

        with self.assertRaisesRegex(ValueError, "inconsistent"):
            summarize_events([*first.events, *second.events])


if __name__ == "__main__":
    unittest.main()
