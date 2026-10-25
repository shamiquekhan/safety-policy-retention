# Synthetic data layout

The committed `data/splits/pilot_scenarios.jsonl` is an engineering pilot and
must not be used as the default research training set. Unit-test validator cases
under `tests/fixtures/` are also not training data.

Research data must be supplied explicitly in split-specific manifests:

```text
data/
├── train/
│   ├── scenarios.jsonl
│   ├── policy_checks.jsonl
│   └── corrected_trajectories.jsonl
├── dev/
│   ├── scenarios.jsonl
│   └── policy_checks.jsonl
└── test/
    ├── scenarios.jsonl
    └── expected_outcomes.jsonl
```

`scripts/build_training_examples.py` requires explicit `--scenarios` and
`--cases` paths and rejects manifests that are not explicitly marked
`split=train`. Test fixtures and pilot scenarios therefore cannot silently enter
the training command.
