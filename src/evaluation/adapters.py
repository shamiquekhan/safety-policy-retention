"""Model-adapter contracts for action-only episode evaluation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Protocol

Action = dict[str, Any]


class ActionModel(Protocol):
    """Minimal interface required by the synthetic episode runner."""

    model_id: str
    checkpoint_revision: str | None

    def propose(self, observation: dict[str, Any]) -> Action | None:
        """Return one action-only proposal for the current observation."""


class ReferenceActionModel:
    """Oracle adapter used only for pipeline smoke tests, never as evidence."""

    model_id = "REFERENCE_ACTION_ORACLE"
    checkpoint_revision = "synthetic-reference-v0"

    def __init__(self, scenarios: list[dict[str, Any]]) -> None:
        self._actions = {
            scenario["scenario_id"]: scenario["reference_safe_action"]
            for scenario in scenarios
        }

    def propose(self, observation: dict[str, Any]) -> Action:
        scenario_id = observation["scenario_id"]
        try:
            return deepcopy(self._actions[scenario_id])
        except KeyError as exc:
            raise ValueError(f"unknown scenario for reference adapter: {scenario_id}") from exc
