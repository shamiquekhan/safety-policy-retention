"""Evaluation adapters, episode execution and metric computation."""

from .adapters import ActionModel, ReferenceActionModel
from .episodes import run_scenario_matrix
from .metrics import (
    paired_effect_summary,
    paired_episode_difference,
    paired_template_bootstrap,
    summarize_by_condition,
    summarize_events,
)

__all__ = [
    "ActionModel",
    "ReferenceActionModel",
    "paired_episode_difference",
    "paired_effect_summary",
    "paired_template_bootstrap",
    "run_scenario_matrix",
    "summarize_by_condition",
    "summarize_events",
]
