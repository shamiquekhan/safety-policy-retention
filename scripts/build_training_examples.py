#!/usr/bin/env python3
"""Build framework-neutral action/policy SFT examples for condition B or C."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.training.examples import build_training_examples


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--condition", choices=("B", "C"), required=True)
    parser.add_argument("--scenarios", type=Path, default=ROOT / "data/splits/pilot_scenarios.jsonl")
    parser.add_argument("--cases", type=Path, default=ROOT / "tests/fixtures/validator_cases.jsonl")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--policy-text", default="Synthetic policy version 0.1")
    parser.add_argument("--lambda-policy", type=float, default=0.25)
    args = parser.parse_args()

    examples = build_training_examples(
        load_jsonl(args.scenarios),
        load_jsonl(args.cases),
        condition=args.condition,
        policy_text=args.policy_text,
        lambda_policy=args.lambda_policy,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        "".join(json.dumps(example.as_dict(), sort_keys=True) + "\n" for example in examples)
    )
    print(f"wrote {len(examples)} examples for condition {args.condition} to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
