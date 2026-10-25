"""Validation helpers for scenario manifests and template-level splits."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from typing import Any, Iterable


REQUIRED_MANIFEST_FIELDS = {
    "scenario_id",
    "template_id",
    "pair_id",
    "split",
    "episode_type",
    "policy_family",
    "shift_category",
    "scenario_hash",
    "reference_safe_action",
    "task_success_predicate",
}


def scenario_hash(scenario: dict[str, Any]) -> str:
    """Return the stable hash for semantic scenario content."""

    content = {
        key: scenario[key]
        for key in (
            "template_id",
            "pair_id",
            "episode_type",
            "policy_family",
            "category",
            "task",
            "initial_state",
            "reference_safe_action",
            "task_success_predicate",
        )
    }
    encoded = json.dumps(content, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()[:16]


def validate_scenario_manifest(rows: Iterable[dict[str, Any]]) -> None:
    """Raise ``ValueError`` when a manifest is malformed or internally inconsistent."""

    scenarios = list(rows)
    scenario_ids: set[str] = set()
    hashes: set[str] = set()
    pairs: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for scenario in scenarios:
        missing = REQUIRED_MANIFEST_FIELDS - scenario.keys()
        if missing:
            raise ValueError(
                f"{scenario.get('scenario_id', '<unknown>')} missing fields: "
                f"{sorted(missing)}"
            )
        scenario_id = scenario["scenario_id"]
        if scenario_id in scenario_ids:
            raise ValueError(f"duplicate scenario_id: {scenario_id}")
        scenario_ids.add(scenario_id)

        expected_hash = scenario_hash(scenario)
        if scenario["scenario_hash"] != expected_hash:
            raise ValueError(
                f"scenario_hash mismatch for {scenario_id}: "
                f"expected {expected_hash}, got {scenario['scenario_hash']}"
            )
        if expected_hash in hashes:
            raise ValueError(f"duplicate semantic scenario hash: {expected_hash}")
        hashes.add(expected_hash)

        pair_id = scenario["pair_id"]
        if pair_id is not None:
            pairs[pair_id].append(scenario)

    for pair_id, pair in pairs.items():
        if len({row["split"] for row in pair}) != 1:
            raise ValueError(f"paired scenarios cross split boundary: {pair_id}")
        if len({row["template_id"] for row in pair}) != 1:
            raise ValueError(f"paired scenarios use different templates: {pair_id}")


def validate_template_disjoint_splits(rows: Iterable[dict[str, Any]]) -> None:
    """Ensure a template and its paired scenarios occur in only one split."""

    template_splits: dict[str, set[str]] = defaultdict(set)
    pair_splits: dict[str, set[str]] = defaultdict(set)
    for scenario in rows:
        template_splits[scenario["template_id"]].add(scenario["split"])
        if scenario["pair_id"] is not None:
            pair_splits[scenario["pair_id"]].add(scenario["split"])

    leaking_templates = {
        template: sorted(splits)
        for template, splits in template_splits.items()
        if len(splits) > 1
    }
    if leaking_templates:
        raise ValueError(f"templates cross split boundaries: {leaking_templates}")

    leaking_pairs = {
        pair: sorted(splits)
        for pair, splits in pair_splits.items()
        if len(splits) > 1
    }
    if leaking_pairs:
        raise ValueError(f"paired templates cross split boundaries: {leaking_pairs}")
