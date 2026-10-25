# Safety Policy Retention after Guard Removal

This repository is a small, reproducible research workspace for studying whether
tool-using language models retain executable safety policies after an independent
runtime guard is disabled.

## Current status

**Stage:** literature audit and protocol design. No model fine-tuning has started.

**Working question:** Does adding explicit, machine-checkable constraint
supervision to corrected-trajectory SFT reduce post-guard-removal policy
violations compared with trajectory-only SFT, while preserving legitimate task
completion under held-out policy combinations, state changes and synthetic
indirect prompt injection?

This is a candidate contribution, not a confirmed novelty claim. The closest
literature already covers harness distillation, runtime-semantics supervision,
policy internalization and agent safety evaluation. The project therefore begins
with an evidence-backed gap audit before simulator implementation or training.

## Repository map

```text
research/       research question, literature matrix, protocol, preregistration
configs/        versioned policy and experiment specifications
data/           synthetic data and frozen split manifests (no model weights)
src/            future sandbox, validator, agent, training and evaluation code
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
- Results are behavioral evidence in a bounded sandbox, not formal or production
  safety guarantees.

## First deliverables

1. `research/research_question.md`
2. `research/literature_matrix.csv`
3. `research/decision_memo.md`
4. `research/experiment_protocol.md`
5. `research/preregistration.md` (draft; not frozen until the pilot is stable)

## Reproducibility rule

Every experiment should record the model revision, dataset and split hashes,
policy version, training seed, decoding parameters, environment version and
timestamp. Generated traces, checkpoints, caches and credentials must not be
committed.
