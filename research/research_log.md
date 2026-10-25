# Research log

## 2026-10-25 — Initial workspace and literature audit

- Created a local research workspace; no GitHub remote or external publication
  action was performed.
- Verified the closest cited papers from their primary pages where available.
- Confirmed that Harness-Zero reports post-removal transfer of harness-induced
  behavior and task performance, but its headline result is not a safety-policy
  retention comparison.
- Confirmed that HPD adds runtime-control semantics to supervision but deploys
  through the original harness interface; this is not the same as a guard-off
  action-level safety test.
- Confirmed that SafeEvolve is a harness-policy co-evolution method using
  harness-use SFT plus harness-augmented RL. It is a close safety comparator but
  does not isolate the proposed two-condition SFT comparison.
- Added newer adjacent work on complex policy internalization and organization-
  specific policy alignment to avoid an outdated gap statement.
- Corrected a naming ambiguity: `ClawsBench` and `SafeClawBench` are distinct
  papers and should not be cited as one benchmark.

## Evidence policy

Claims in the matrix are marked as `verified`, `partial` or `to-check`. A search
snippet, secondary synthesis or generated consensus is not treated as evidence
for a novelty claim. Page/section/table evidence must be added for the three
closest papers before preregistration is frozen.

## 2026-10-25 — Terminology and scope refinement

- Renamed the proposed treatment **policy-supervised SFT (PS-SFT)**.
- Reserved “constraint-aware optimization” for methods that alter gradients or
  optimizer updates, such as chance-constrained, proximal or safety-subspace
  methods.
- Reframed the main comparison as trajectory-only SFT versus PS-SFT, with the
  same corrected tool-use targets and an added decision-level auxiliary loss.
- Made episode-level attempted-violation incidence the primary safety estimand,
  while retaining proposed-action violation rate as a required secondary outcome
  to expose conditional action quality and refusal/abandonment effects.
- Kept the first study to one backbone and SFT only. Optimizer-level constraints,
  RL, a second backbone and a large benchmark are deferred until the pilot is
  measurable and stable.
- Treat the local 4 GB GPU as suitable for simulator development and small pilot
  runs, not as evidence that a multi-seed main fine-tuning study will fit locally.

## Open checks

- Keep the direct-overlap audit bounded to the evidence locations in
  `research/direct_overlap_audit.md`; HPD code availability remains unverified.
- If additional implementation details become available, check whether any
  ablation truly removes runtime enforcement rather than only changing policy
  prompts.
- Define a search date, databases, query families and inclusion criteria before
  using counts such as “no prior work.”
- Confirm that the final preregistration retains episode-level violation
  incidence as the primary safety estimand and action-level violation as a key
  secondary outcome.

## 2026-10-25 — Scenario schema and validator milestone

- Replaced ambiguous `expected_action` fields with `reference_safe_action` in
  pilot scenarios.
- Added `episode_type` (`benign` or `policy_challenge`) and
  `task_success_predicate` to each scenario.
- Added separate `tests/fixtures/validator_cases.jsonl` fixtures with
  `candidate_action` and expected validator labels.
- Implemented deterministic validation and synthetic execution in
  `src/environment/validator.py`.
- Added tests for authorization, confidentiality, approval handling, injected
  instructions, guard-on blocking, guard-off state mutation and context flips.
- Verification: `python3 -m pytest -q` passed with 8 tests and 20 subtests.

## 2026-10-25 — Shared-interface PS-SFT and sandbox runner milestone

- Replaced the combined decision/action inference format with action-only
  inference for every condition.
- Specified separate `[ACTION]` and `[POLICY_CHECK]` training tasks over one
  shared backbone.
- Defined `L_B = L_action` and
  `L_C = L_action + lambda_policy * L_policy`, with separate token
  normalization and matched examples/order for B and C.
- Added `configs/training.yaml`, `src/training/examples.py` and
  `scripts/build_training_examples.py` so B/C data equivalence can be checked
  before a model-specific trainer is selected.
- Added stable scenario hashes, shift categories and pilot split metadata.
- Added template/pair split validation and an append-only episode runner that
  records proposals, validator labels, guard interventions, executions and
  state hashes.
- Completed a primary-paper direct-overlap audit for Harness-Zero, HPD and
  SafeEvolve. The go decision remains provisional and is now framed as a
  matched B-versus-C comparison rather than a claim that safety transfer is
  unexplored.

## 2026-10-25 — Validator boundary and metric milestone

- Made approval gating apply consistently to all consequential updates and
  sends, including authorized destinations.
- Added deterministic checks for approval scope, authorized approver and
  expiration time, plus malformed/unknown-action tests.
- Added explicit-denominator metrics for episode attempted-violation rate,
  action-level violation rate, benign success, sandbox harm, false refusal and
  guard intervention.
- Added Wilson 95% intervals, per-condition summaries and paired C-minus-B
  episode differences.
- Added `scripts/summarize_events.py` and verified it on a synthetic B/C event
  log.
