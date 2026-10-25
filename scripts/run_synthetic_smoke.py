#!/usr/bin/env python3
"""Run the reference action adapter through the full synthetic pipeline.

This is an engineering smoke test only. It is not a model baseline and must
never be used as evidence for safety retention.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.evaluation import ReferenceActionModel, run_scenario_matrix, summarize_events


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--scenarios", type=Path, default=ROOT / "data/splits/pilot_scenarios.jsonl")
    parser.add_argument("--guard", choices=("off", "on", "both"), default="both")
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    scenarios = load_jsonl(args.scenarios)
    if args.limit is not None:
        scenarios = scenarios[: args.limit]
    model = ReferenceActionModel(scenarios)
    modes = (False, True) if args.guard == "both" else (args.guard == "on",)
    events: list[dict] = []
    for guard_on in modes:
        events.extend(
            run_scenario_matrix(
                model,
                scenarios,
                guard_on=guard_on,
                training_condition="A_reference_smoke",
                evaluation_seed=0,
                max_turns=1,
                policy_text="Synthetic policy version 0.1",
            )
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("".join(json.dumps(event, sort_keys=True) + "\n" for event in events))
    summaries = {
        guard_mode: summarize_events(
            [event for event in events if event["evaluation_guard_mode"] == guard_mode]
        )
        for guard_mode in sorted({event["evaluation_guard_mode"] for event in events})
    }
    print(json.dumps({"by_guard_mode": summaries}, indent=2, sort_keys=True))
    print(f"wrote {len(events)} events to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
