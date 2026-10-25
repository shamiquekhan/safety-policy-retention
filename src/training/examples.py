"""Build matched action and policy-assessment SFT examples.

This module deliberately does not depend on a tokenizer or a model-training
framework. It defines the data contract that a later trainer must consume:
both conditions receive the same examples and ordering, while condition B gives
the policy-assessment task zero loss weight and condition C gives it a positive
auxiliary weight.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Iterable, Literal

from src.environment.validator import validate_action

ACTION_PREFIX = "[ACTION]"
POLICY_CHECK_PREFIX = "[POLICY_CHECK]"
Condition = Literal["B", "C"]
TaskName = Literal["action", "policy_check"]


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _prompt(prefix: str, payload: dict[str, Any]) -> str:
    return f"{prefix}\n{_canonical_json(payload)}"


@dataclass(frozen=True)
class TrainingExample:
    """Framework-neutral supervised example with a task-specific loss weight."""

    example_id: str
    task: TaskName
    source_id: str
    prompt: str
    target: str
    loss_weight: float

    def as_dict(self) -> dict[str, Any]:
        return {
            "example_id": self.example_id,
            "task": self.task,
            "source_id": self.source_id,
            "prompt": self.prompt,
            "target": self.target,
            "loss_weight": self.loss_weight,
        }


def _action_example(
    scenario: dict[str, Any], *, policy_text: str, source_id: str
) -> TrainingExample:
    payload = {
        "policy": policy_text,
        "task": scenario["task"],
        "state": scenario["initial_state"],
    }
    return TrainingExample(
        example_id=f"action:{source_id}",
        task="action",
        source_id=source_id,
        prompt=_prompt(ACTION_PREFIX, payload),
        target=_canonical_json(scenario["reference_safe_action"]),
        loss_weight=1.0,
    )


def _policy_example(
    scenario: dict[str, Any],
    case: dict[str, Any],
    *,
    policy_text: str,
    loss_weight: float,
) -> TrainingExample:
    candidate_action = case["candidate_action"]
    validation = validate_action(scenario["initial_state"], candidate_action)
    expected = {
        "compliant": case["expected_compliant"],
        "rule_id": case["expected_rule_id"],
    }
    actual = {"compliant": validation.compliant, "rule_id": validation.rule_id}
    if actual != expected:
        raise ValueError(
            f"validator fixture mismatch for {case['case_id']}: "
            f"expected {expected}, got {actual}"
        )

    payload = {
        "policy": policy_text,
        "task": scenario["task"],
        "state": scenario["initial_state"],
        "candidate_action": candidate_action,
    }
    target = {
        "compliant": validation.compliant,
        "rule_id": validation.rule_id,
        "requires_approval": validation.requires_approval,
        "safe_alternative": validation.safe_alternative,
    }
    return TrainingExample(
        example_id=f"policy_check:{case['case_id']}",
        task="policy_check",
        source_id=case["case_id"],
        prompt=_prompt(POLICY_CHECK_PREFIX, payload),
        target=_canonical_json(target),
        loss_weight=loss_weight,
    )


def build_training_examples(
    scenarios: Iterable[dict[str, Any]],
    cases: Iterable[dict[str, Any]],
    *,
    condition: Condition,
    policy_text: str,
    lambda_policy: float = 0.25,
) -> list[TrainingExample]:
    """Return a matched action/policy task schedule for condition B or C.

    The returned ordering is deterministic: all action examples in scenario
    order, followed by all policy-check examples in fixture order. Conditions B
    and C therefore differ only in the policy-task loss weight.
    """

    if lambda_policy <= 0:
        raise ValueError("lambda_policy must be positive for condition C")
    if condition not in {"B", "C"}:
        raise ValueError("condition must be 'B' or 'C'")

    scenario_rows = list(scenarios)
    scenario_by_id = {row["scenario_id"]: row for row in scenario_rows}
    policy_weight = 0.0 if condition == "B" else lambda_policy

    examples = [
        _action_example(row, policy_text=policy_text, source_id=row["scenario_id"])
        for row in scenario_rows
    ]
    for case in cases:
        scenario_id = case["scenario_id"]
        try:
            scenario = scenario_by_id[scenario_id]
        except KeyError as exc:
            raise ValueError(
                f"validator fixture references unknown scenario {scenario_id}"
            ) from exc
        examples.append(
            _policy_example(
                scenario,
                case,
                policy_text=policy_text,
                loss_weight=policy_weight,
            )
        )
    return examples
