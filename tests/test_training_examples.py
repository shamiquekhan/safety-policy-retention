import json
import unittest
from pathlib import Path

from src.training.examples import build_training_examples


ROOT = Path(__file__).resolve().parents[1]
SCENARIO_PATH = ROOT / "data" / "splits" / "pilot_scenarios.jsonl"
CASE_PATH = ROOT / "tests" / "fixtures" / "validator_cases.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


class TrainingExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.scenarios = load_jsonl(SCENARIO_PATH)
        cls.cases = load_jsonl(CASE_PATH)
        cls.condition_b = build_training_examples(
            cls.scenarios,
            cls.cases,
            condition="B",
            policy_text="Synthetic policy version 0.1",
            lambda_policy=0.25,
        )
        cls.condition_c = build_training_examples(
            cls.scenarios,
            cls.cases,
            condition="C",
            policy_text="Synthetic policy version 0.1",
            lambda_policy=0.25,
        )

    def test_conditions_have_identical_examples_and_order(self) -> None:
        self.assertEqual(
            [(item.task, item.source_id, item.prompt, item.target) for item in self.condition_b],
            [(item.task, item.source_id, item.prompt, item.target) for item in self.condition_c],
        )

    def test_only_policy_task_loss_weight_differs(self) -> None:
        for item_b, item_c in zip(self.condition_b, self.condition_c):
            if item_b.task == "action":
                self.assertEqual(item_b.loss_weight, 1.0)
                self.assertEqual(item_c.loss_weight, 1.0)
            else:
                self.assertEqual(item_b.loss_weight, 0.0)
                self.assertEqual(item_c.loss_weight, 0.25)

    def test_action_task_has_action_only_target_and_prefix(self) -> None:
        action_examples = [item for item in self.condition_c if item.task == "action"]
        self.assertEqual(len(action_examples), len(self.scenarios))
        for example in action_examples:
            self.assertTrue(example.prompt.startswith("[ACTION]\n"))
            target = json.loads(example.target)
            self.assertIn("tool", target)
            self.assertIn("arguments", target)
            self.assertNotIn("decision", target)

    def test_policy_task_is_validator_labelled_and_prefixed(self) -> None:
        policy_examples = [item for item in self.condition_c if item.task == "policy_check"]
        self.assertEqual(len(policy_examples), len(self.cases))
        for example in policy_examples:
            self.assertTrue(example.prompt.startswith("[POLICY_CHECK]\n"))
            target = json.loads(example.target)
            self.assertIn("compliant", target)
            self.assertIn("rule_id", target)
            self.assertIn("requires_approval", target)


if __name__ == "__main__":
    unittest.main()
