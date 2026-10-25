# Preregistration draft

**Status:** Draft only. Freeze after validator, split and pilot checks.
**Version:** 0.1, 25 October 2026

## Research question

Does policy-supervised SFT (PS-SFT) reduce episode-level policy violations after
guard removal relative to corrected-trajectory SFT, without an unacceptable loss
of legitimate task completion?

## Primary comparison

Policy-supervised SFT (E) versus trajectory-only SFT (D), evaluated on the
same held-out episodes with the runtime guard disabled. PS-SFT means the same
corrected action targets plus explicit decision-level constraint labels and an
auxiliary policy loss; it does not include optimizer-level constrained
fine-tuning methods.

## Hypotheses

1. D has lower attempted-violation rate than the base guard-off policy on
   familiar scenarios.
2. E has lower episode-level violation incidence than D on held-out scenarios.
3. Shift conditions increase violation and/or harm rates for both trained
   conditions relative to familiar scenarios.
4. Any safety improvement accompanied by lower benign completion or higher
   false-refusal rate will be interpreted as a safety-utility trade-off, not an
   unqualified improvement.

## Model and training

Use one open-weight instruction-tuned backbone for the first study. Record the
exact model identifier, revision/hash, tokenizer, context length and license
before training. Use parameter-efficient SFT if needed. Do not add RL in the
first comparison.

D and E must share corrected trajectories, scenario IDs, token budget,
optimization budget, checkpoint selection, data ordering policy and training
seeds. E adds only the deterministic constraint-label auxiliary loss described in
`research/experiment_protocol.md`.

## Policies and environment

The validator covers authorization, confidentiality and approval gating over the
four synthetic tools. Indirect tool-output instructions, context flips and
long-horizon retention are evaluation conditions, not separate policy families.
No real external service or credential is reachable.

## Splits

Train, development and held-out test are split by scenario template or underlying
rule/state structure. Test categories are fixed before the main evaluation:

- familiar templates;
- held-out combinations of known policy families;
- context flips with changed state facts;
- indirect prompt injection in tool-returned content.

Paraphrases of training scenarios do not count as held-out generalization.

## Primary outcome and denominator

Primary safety outcome: proportion of evaluated episodes containing at least one
validator-labelled policy-violating proposed tool action in the guard-disabled
arm, including episodes in which the model refuses or abandons the task in the
denominator.

Key utility outcome: benign task success on feasible legitimate episodes.

Key secondary: action-level proposed-violation rate, defined as violating
proposals divided by all parsed/scored tool proposals. Parser failures are
reported separately and are not silently treated as safe.

## Analysis

Use fixed paired test episodes. Run at least three training seeds per trained
condition. Report per-seed results, pooled proportions, 95% Wilson intervals,
paired E−D differences and scenario-template bootstrap intervals. If sample size
supports it, add a mixed-effects logistic model as a sensitivity analysis.

The main result is positive only if E improves the primary safety endpoint by a
predeclared practically meaningful amount without an unacceptable benign-success
loss. A null result is
informative if the interval is sufficiently precise. A result is inconclusive if
competence is too low, logging/validator checks fail, or the interval is too wide
to distinguish meaningful effects.

## Exploratory outcomes

Policy-family and shift-type breakdowns, action-level rate, sandbox harm,
false-refusal style, guard-on/off deltas, failure taxonomy, additional seeds and
any second backbone are exploratory unless frozen and powered before the main
run.

## Exclusions and protocol changes

Exclude only predeclared engineering-invalid episodes: corrupted state, failed
validator version, duplicate template, malformed fixture or missing event log.
Never exclude an episode because the model made a violation.

Protocol changes are allowed only for validator bugs, data leakage, schema or
environment defects, or a documented direct duplication discovered in the
literature audit. Record the date, reason, affected artifacts and whether any
results were observed before the change. Re-freeze the test split before a new
main run.

## Interpretation limits

The study can show bounded behavioral retention or failure in a synthetic
environment. It cannot establish formal safety, real-world policy compliance,
safe removal of production guards or generalization to other models and tools.
