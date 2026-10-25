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


if __name__ == "__main__":
    unittest.main()
