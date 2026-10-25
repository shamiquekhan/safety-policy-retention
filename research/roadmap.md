# Execution roadmap

This roadmap deliberately separates evidence collection, simulator correctness,
pilot feasibility and the main comparison. The first milestone is not a trained
checkpoint; it is a validator whose labels and state transitions can be tested.

## Next 48 hours

1. Read the methods, appendices and code for Harness-Zero, HPD and SafeEvolve.
2. Add page/section/table evidence to the first three rows of the literature
   matrix.
3. Run the candidate-literature triage: classify each item as training-side
   internalization, runtime enforcement, benchmark/evaluation or theory.
4. Freeze a search procedure: databases, query families, date, deduplication and
   inclusion criteria. Do not use unbounded search-result counts as gap evidence.
5. Decide the pilot model only after checking its structured tool-call reliability
   and local/remote compute budget.

## Week 1 — gap audit and protocol freeze

**Build:** final candidate question, decision memo, literature matrix, protocol
draft and paper outline.
**Exit:** no unresolved claim that “no prior work exists”; exact differences from
the closest methods are written down; policy and metric definitions are stable.

## Week 2 — deterministic sandbox

**Build:** state schema, four tools, validator, guard wrapper, measurement-only
mode and append-only event logger.
**Tests:** authorized/unauthorized reads, approved/unapproved consequential
actions, confidentiality boundaries, injected tool-output instructions, state
hashes and guard-off non-intervention.
**Exit:** unit tests pass and replaying an episode reproduces the same labels and
state transitions.

## Week 3 — scenario generator and pilot harness

**Build:** template-based scenario generator with train/dev/test manifests,
balanced policy families, benign tasks, context flips and injection fixtures.
**Pilot:** run the base model in guarded and unguarded modes; verify both benign
success and observable unsafe proposals.
**Exit:** logs reconstruct decisions and metrics without manual relabeling.

## Week 4 — corrected data and audit

**Build:** collect reference traces, record guard interventions, create corrected
targets and deterministic constraint labels.
**Audit:** schema validity, validator consistency, duplicates, balance, test
leakage, safe-target validity and benign coverage.
**Exit:** freeze train/dev/test manifests and dataset hashes before model
selection for the main run.

## Week 5 — matched SFT pilot

**Build:** D trajectory-only and E constraint-aware auxiliary-loss training with
the same budget.
**Run:** at least three seeds on a small pilot split; log every hyperparameter,
checkpoint and cost.
**Exit:** both variants parse the action schema and complete enough benign tasks
for a meaningful safety comparison.

## Week 6 — preregistered main evaluation

**Run:** A–F on the frozen test set, with guard-off arms genuinely unguarded and
the validator measurement-only.
**Store:** raw event logs, environment version, model revision, seed and decoding
settings.
**Exit:** no silent parser, validator or executor failures.

## Week 7 — analysis and failure investigation

**Compute:** episode attempted-violation rate, action-level rate, safe/benign
success, harm, refusal and guard intervention outcomes with intervals.
**Inspect:** paired failures by policy family and shift type; distinguish policy
confusion, context failure, injection following, schema error and refusal.
**Exit:** primary comparison and uncertainty table are reproducible from raw logs.

## Week 8 — bounded paper and release

**Write:** method, results, failure analysis and limitations while preserving
negative results and protocol deviations.
**Release:** code, configs, synthetic fixtures, split manifests and redacted
logs where licensing permits.
**Exit:** every reported number can be regenerated from a documented command and
versioned artifact.

## Stop/revise rules

- If full-text review finds the exact matched comparison, revise the question
  before training.
- If the validator cannot distinguish allowed and prohibited state transitions,
  stop model work and fix the environment.
- If the base model cannot complete benign tasks, simplify tools or change the
  model before interpreting safety.
- If the base model never proposes unsafe actions, inspect task difficulty and
  policy opportunities; do not manufacture ambiguity just to raise violations.
- If E only reduces violations by refusing or abandoning tasks, report a trade-off
  or null retention gain rather than a safety improvement.
- If confidence intervals are too wide, report an inconclusive pilot and use the
  observed variance to justify a revised test size.
