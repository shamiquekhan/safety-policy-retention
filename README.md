# Safety Policy Retention after Guard Removal

This repository is a small, reproducible research workspace for studying whether
tool-using language models retain executable safety policies after an independent
runtime guard is disabled.

## Current status

**Stage:** validator-first pipeline and direct-overlap audit. No model
fine-tuning or baseline model run has started.

**Working question:** Does adding explicit, machine-checkable policy
supervision—called **policy-supervised SFT (PS-SFT)** here—to corrected-
trajectory SFT reduce post-guard-removal policy violations compared with
trajectory-only SFT, while preserving legitimate task completion under held-out
policy combinations, state changes and synthetic indirect prompt injection?

PS-SFT means decision-level policy labels or an auxiliary policy-classification
loss added to the same corrected tool-use targets. It does not refer to
optimizer-level methods such as chance-constrained updates, proximal objectives
or safety-gradient projection; those are separate future comparisons.

This is a candidate contribution, not a confirmed novelty claim. The closest
literature already covers harness distillation, runtime-semantics supervision,
policy internalization and agent safety evaluation. The project therefore keeps
the gap claim bounded while validating the simulator before training.

## Repository map

```text
research/       research question, literature matrix, protocol, preregistration
configs/        versioned policy and experiment specifications
data/           synthetic data and frozen split manifests (no model weights)
src/            validator, training-data builders and future agent/evaluation code
tests/          validator and simulator tests
scripts/        reproducible command-line entry points
results/        pilot/main outputs and figures; generated files are ignored
paper/          outline and limitations
```

## Research safeguards

- Synthetic state only; no real messages, accounts or external side effects.
- The guard-disabled arm must not block or rewrite actions.
- The validator remains measurement-only when the guard is off.
- Proposed actions, guard interventions, executed actions and state changes are
  logged separately.
- The held-out split is by scenario template or rule structure, not paraphrase.
- Safety is always reported alongside benign utility and refusal/abandonment.
- PS-SFT is safety-improving only if benign task success satisfies a predeclared
  non-inferiority margin against trajectory-only SFT.
- Results are behavioral evidence in a bounded sandbox, not formal or production
  safety guarantees.

## First deliverables

1. `research/research_question.md`
2. `research/literature_matrix.csv`
3. `research/priority_literature_matrix.csv`
4. `research/decision_memo.md`
5. `research/experiment_protocol.md`
6. `research/preregistration.md` (draft; not frozen until the pilot is stable)
7. `data/splits/pilot_scenarios.jsonl`
8. `configs/training.yaml`

## Reproducibility rule

Every experiment should record the model revision, dataset and split hashes,
policy version, training seed, decoding parameters, environment version and
timestamp. Generated traces, checkpoints, caches and credentials must not be
committed.
