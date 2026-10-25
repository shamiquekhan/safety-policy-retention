#!/usr/bin/env python3
"""Summarize append-only episode events with explicit metric denominators."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation.metrics import (
    paired_episode_difference,
    summarize_by_condition,
    summarize_events,
)


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    events = load_jsonl(args.input)
    result = summarize_events(events)
    result["by_condition"] = summarize_by_condition(events)
    conditions = {event.get("training_condition") for event in events}
    if {"B", "C"}.issubset(conditions):
        result["paired_attempted_violation_differences_C_minus_B"] = (
            paired_episode_difference(events)
        )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
