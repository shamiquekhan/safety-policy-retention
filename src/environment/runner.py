"""Replayable synthetic episode runner for guard-on/off pipeline checks."""

from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable

from .validator import Action, State, guarded_execute

ProposalFn = Callable[[dict[str, Any]], Action | None]
SuccessFn = Callable[[State, dict[str, Any]], bool]


def _state_hash(state: State) -> str:
    encoded = json.dumps(state, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:16]


@dataclass(frozen=True)
class EpisodeResult:
    events: tuple[dict[str, Any], ...]
    final_state: State
    task_success: bool | None
    attempted_violation: bool
    sandbox_harm: bool
    refusal_or_abandonment: bool


def run_episode(
    scenario: dict[str, Any],
    propose: ProposalFn,
    *,
    guard_on: bool,
    max_turns: int = 4,
    success: SuccessFn | None = None,
    metadata: dict[str, Any] | None = None,
) -> EpisodeResult:
    """Run a synthetic episode and emit one append-only event per proposal.

    ``propose`` receives an action-only observation. The runner never asks a
    model for or consumes a policy-decision field. In guard-off mode,
    :func:`guarded_execute` executes invalid proposals so state effects remain
    observable.
    """

    if max_turns < 1:
        raise ValueError("max_turns must be positive")

    metadata = dict(metadata or {})
    state = deepcopy(scenario["initial_state"])
    events: list[dict[str, Any]] = []
    training_condition = metadata.get("training_condition", "A")
    training_seed = metadata.get("training_seed")
    evaluation_seed = metadata.get("evaluation_seed", 0)
    model_id = metadata.get("model_id", "UNSELECTED")
    checkpoint_revision = metadata.get("checkpoint_revision")
    guard_mode = "on" if guard_on else "off"
    run_id = metadata.get("run_id") or ":".join(
        str(value)
        for value in (
            training_condition,
            model_id,
            checkpoint_revision or "unknown-checkpoint",
            f"train{training_seed if training_seed is not None else 'unknown'}",
            f"eval{evaluation_seed}",
            f"guard{guard_mode}",
        )
    )
    episode_id = metadata.get(
        "episode_id",
        f"{run_id}:{scenario['scenario_id']}",
    )
    attempted_violation = False
    sandbox_harm = False
    refusal_or_abandonment = False

    for turn_index in range(max_turns):
        state_before = deepcopy(state)
        state_before_hash = _state_hash(state_before)
        observation = {
            "task": scenario["task"],
            "policy": metadata.get("policy_text", ""),
            "state": deepcopy(state_before),
            "turn_index": turn_index,
            "scenario_id": scenario["scenario_id"],
        }
        action = propose(observation)
        next_state, validation, execution = guarded_execute(
            state_before, action, guard_on=guard_on
        )
        state = next_state
        attempted_violation = attempted_violation or not validation.compliant
        sandbox_harm = sandbox_harm or execution.get("harm_observed", False)
        action_is_dict = isinstance(action, dict)
        if action_is_dict and action.get("tool") == "finish":
            reason = action.get("arguments", {}).get("reason")
            refusal_or_abandonment = reason not in {None, "completed", "success"}

        events.append(
            {
                "episode_id": episode_id,
                "run_id": run_id,
                "scenario_id": scenario["scenario_id"],
                "template_id": scenario["template_id"],
                "episode_type": scenario["episode_type"],
                "policy_family": scenario["policy_family"],
                "shift_category": scenario.get("shift_category", scenario.get("category")),
                "split": scenario.get("split"),
                "scenario_hash": scenario.get("scenario_hash"),
                "model_id": model_id,
                "checkpoint_revision": checkpoint_revision,
                "training_condition": training_condition,
                "training_seed": training_seed,
                "evaluation_seed": evaluation_seed,
                "policy_version": metadata.get("policy_version", "0.1-draft"),
                "environment_version": metadata.get("environment_version", "0.1"),
                "evaluation_guard_mode": guard_mode,
                "turn_index": turn_index,
                "initial_state_id": scenario["scenario_id"],
                "observation_id": f"{scenario['scenario_id']}:{turn_index}",
                "raw_model_output": json.dumps(action, sort_keys=True),
                "parsed_proposed_action": deepcopy(action) if action_is_dict else None,
                "validator_result": validation.as_dict(),
                "violation_categories": list(validation.violation_categories),
                "guard_intervention": execution.get("guard_intervention"),
                "executed_action": deepcopy(action) if execution.get("executed") else None,
                "execution_result": deepcopy(execution),
                "state_effects": list(execution.get("state_effects", [])),
                "prohibited_effects": list(execution.get("prohibited_effects", [])),
                "harm_observed": bool(execution.get("harm_observed", False)),
                "state_before_hash": state_before_hash,
                "state_after_hash": _state_hash(state),
                "task_success": None,
                "refusal_or_abandonment": refusal_or_abandonment,
                "schema_error": validation.rule_id == "schema",
            }
        )
        if action_is_dict and action.get("tool") == "finish":
            break

    task_success = success(state, scenario) if success is not None else None
    for event in events:
        event["task_success"] = task_success
    return EpisodeResult(
        events=tuple(events),
        final_state=state,
        task_success=task_success,
        attempted_violation=attempted_violation,
        sandbox_harm=sandbox_harm,
        refusal_or_abandonment=refusal_or_abandonment,
    )
