"""Metric computation for append-only synthetic episode logs."""

from .metrics import paired_episode_difference, summarize_by_condition, summarize_events

__all__ = ["paired_episode_difference", "summarize_by_condition", "summarize_events"]
