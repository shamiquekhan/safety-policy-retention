"""Run an action-only adapter over a synthetic scenario manifest."""

from __future__ import annotations

from typing import Any, Iterable

from src.environment.runner import run_episode

from .adapters import ActionModel


def run_scenario_matrix(
    model: ActionModel,
    scenarios: Iterable[dict[str, Any]],
    *,
    guard_on: bool,
    training_condition: str = "A",
    training_seed: int | None = None,
    evaluation_seed: int = 0,
    run_id: str | None = None,
    max_turns: int = 4,
    policy_text: str = "",
) -> list[dict[str, Any]]:
    """Return append-only events for each scenario in manifest order."""

    events: list[dict[str, Any]] = []
    for scenario in scenarios:
        result = run_episode(
            scenario,
            model.propose,
            guard_on=guard_on,
            max_turns=max_turns,
            metadata={
                "model_id": model.model_id,
                "checkpoint_revision": model.checkpoint_revision,
                "training_condition": training_condition,
                "training_seed": training_seed,
                "evaluation_seed": evaluation_seed,
                "run_id": run_id,
                "policy_text": policy_text,
            },
        )
        events.extend(result.events)
    return events
