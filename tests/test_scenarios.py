import json
import unittest
from pathlib import Path

from src.environment.scenarios import (
    validate_scenario_manifest,
    validate_template_disjoint_splits,
)


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "data" / "splits" / "pilot_scenarios.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class ScenarioManifestTests(unittest.TestCase):
    def test_pilot_manifest_has_stable_hashes_and_required_metadata(self) -> None:
        scenarios = load_jsonl(SCENARIO_PATH)
        validate_scenario_manifest(scenarios)
        validate_template_disjoint_splits(scenarios)
        self.assertEqual(len(scenarios), 12)

    def test_template_split_leak_is_rejected(self) -> None:
        scenarios = load_jsonl(SCENARIO_PATH)
        scenarios[0] = {**scenarios[0], "split": "train"}
        with self.assertRaisesRegex(ValueError, "templates cross split"):
            validate_template_disjoint_splits(scenarios)


if __name__ == "__main__":
    unittest.main()
