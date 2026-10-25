import json
import unittest
from pathlib import Path

from src.evaluation import ReferenceActionModel, run_scenario_matrix, summarize_events


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "data" / "splits" / "pilot_scenarios.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class SmokePipelineTests(unittest.TestCase):
    def test_reference_adapter_runs_both_guard_modes_without_violations(self) -> None:
        scenarios = load_jsonl(SCENARIO_PATH)
        model = ReferenceActionModel(scenarios)
        events = run_scenario_matrix(
            model,
            scenarios,
            guard_on=False,
            training_condition="A_reference_smoke",
            evaluation_seed=0,
            max_turns=1,
        )
        guarded_events = run_scenario_matrix(
            model,
            scenarios,
            guard_on=True,
            training_condition="A_reference_smoke",
            evaluation_seed=1,
            max_turns=1,
        )
        off_summary = summarize_events(events)
        on_summary = summarize_events(guarded_events)
        self.assertEqual(off_summary["episode_attempted_violation_rate"]["numerator"], 0)
        self.assertEqual(on_summary["episode_attempted_violation_rate"]["numerator"], 0)
        self.assertEqual(off_summary["malformed_proposal_count"], 0)
        self.assertEqual(len(events), len(scenarios))
        self.assertEqual(len(guarded_events), len(scenarios))


if __name__ == "__main__":
    unittest.main()
