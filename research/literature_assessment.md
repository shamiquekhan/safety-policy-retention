# Literature assessment: does PS-SFT improve safety after guard removal?

**Assessment date:** 25 October 2026
**Status:** Primary-paper audit completed on 25 October 2026; numerical claims
and code-level details remain bounded by the evidence table in
`research/direct_overlap_audit.md`.

## Bottom line

Policy-supervised SFT is a credible hypothesis, not an established result.
The literature reviewed so far supports three bounded observations:

1. Fine-tuning can change a language model's safety behavior and the measured
   result can vary with seed and decoding procedure.
2. Some harness-induced behavior can persist after external assistance is
   removed.
3. Learned behavior does not automatically reproduce all protection supplied by
   a runtime guard.

The unresolved comparison is narrower: whether explicit decision-level policy
supervision improves proposed tool-action safety over corrected-trajectory SFT
after an independently identifiable guard is disabled, especially under
compositional, contextual and indirect-injection shifts.

## Evidence classes

| Evidence class | Representative work | Supports | Does not establish |
|---|---|---|---|
| Harness distillation | Harness-Zero | Harness-induced behavior can transfer into weights after specialized harness removal | Security-policy retention or superiority of PS-SFT |
| Runtime-semantics supervision | HPD | Explicit control-state supervision can improve runtime compliance | Safety retention after removing an independent guard |
| Agent safety internalization | SafeEvolve/OPSD-style variants | Some safety behavior can persist without runtime-harness assistance | PS-SFT beating trajectory-only SFT in a matched tool environment |
| Safety-preserving fine-tuning | SPF, Safe Delta and related methods | Training objectives can trade off safety retention and utility | Lower unsafe tool proposals after guard removal |
| Runtime enforcement | ClawGuard and related systems | External enforcement can prevent unsafe execution | How much safety remains when enforcement is removed |
| Agent evaluation | AgentDojo, ClawsBench, SafeClawBench | Tool attacks, utility and realized harm can be evaluated separately | A causal claim about the training signal that caused retention |

## Critical terminology correction

“Constraint-aware SFT” is ambiguous. It can refer to:

- policy labels or safe-alternative labels in supervised examples;
- constrained optimizer updates;
- proximal or trust-region objectives;
- safety-sensitive gradient or subspace preservation; or
- additional policy demonstrations.

This project uses **policy-supervised SFT (PS-SFT)** only for the first
meaning: the same corrected tool-use targets as trajectory SFT plus explicit
decision-level labels for compliance, rule identity, approval requirement and
safe alternative, implemented as an auxiliary policy loss. Optimizer-level
methods are adjacent work and should not be mixed into the first experiment.

## Defensible research gap

The gap is not that no prior work has distilled harness behavior, internalized
policies or evaluated safety after external assistance. The defensible gap is a
controlled comparison with all of the following properties:

1. the same backbone, policy text, tool interface and training budget;
2. the same corrected trajectories for both trained conditions;
3. the only intended treatment difference is the added PS-SFT supervision;
4. the independent runtime guard is genuinely disabled at evaluation;
5. the validator remains measurement-only in the guard-off arm;
6. proposed actions, guard interventions, executed actions and state changes are
   logged separately; and
7. held-out tests include structural rule combinations, context flips and
   malicious tool-returned instructions.

The gap remains provisional until full methods, appendices and code for
Harness-Zero, HPD, SafeEvolve and adjacent post-training safety methods are
checked.

## Recommended research questions

**Main question:** With policy, model, interface and budget held constant as
practical, does PS-SFT reduce proposed policy-violating tool actions after guard
removal without materially reducing legitimate task completion?

- **RQ1 — Retention:** Does PS-SFT reduce proposed policy-violating actions?
- **RQ2 — Shift:** Does the difference persist under compositional shifts,
  context flips and indirect prompt injection?
- **RQ3 — Utility:** Does either method increase false refusals or reduce benign
  task success?

## Minimal experiment

Use one open-weight instruction-tuned backbone and begin with SFT only:

- **A:** base model, guard off;
- **B:** corrected-trajectory SFT, guard off;
- **C:** PS-SFT, guard off;
- **D:** matched guard-on reference runs for the base and trained models.

Keep the written policy visible for both trained conditions. Do not remove the
policy prompt and the guard simultaneously. Add policy-omission tests only after
the main comparison is stable.

### Primary and supporting outcomes

- **Primary:** episode attempted-violation incidence on guard-disabled
  policy-challenge episodes, including refusal/abandonment episodes in the
  denominator.
- **Key secondary:** proposed-action violation rate, calculated over all
  parsed/scored tool proposals in guard-off evaluation.
- **Utility:** benign task success and false-refusal rate, with a predeclared
  non-inferiority margin relative to trajectory-only SFT.
- **Realized effects:** sandbox harm rate based on prohibited state changes.
- **Reference:** guard intervention rate in guard-on runs.

A positive result requires an improvement in episode-level safety and benign task
success within the predeclared non-inferiority margin relative to trajectory-only
SFT; action-level results help explain how the effect arises and whether refusal
is driving it.

## Pilot and statistics

Use a small pilot to estimate violation rates, template variance and seed
variance before fixing the main sample size. Start with approximately 20–40
templates for engineering feasibility; do not treat that range as a powered main
study.

For the main comparison:

- use identical held-out episodes across B and C;
- run at least three training seeds per trained condition if resources permit;
- report per-seed results and 95% confidence intervals;
- use template-level bootstrap intervals or an appropriate mixed-effects model;
- predeclare the practical effect threshold; and
- never interpret a non-significant result as proof of equivalence.

## Compute scope

The local 4 GB GPU is appropriate for sandbox development, validator tests,
small pilots and pipeline checks. A repeated multi-seed SFT study may require
cloud GPU access or collaboration. Do not add RL, optimizer-level safety
constraints, a second backbone and a large benchmark simultaneously.

## Interpretation rules

| Result | Interpretation |
|---|---|
| PS-SFT improves violations and preserves benign success | Evidence of improved measured retention in the tested setting |
| PS-SFT improves safety but harms benign success | Safety–utility trade-off, not an unqualified improvement |
| Both SFT methods improve similarly | Behavioral transfer without evidence that PS-SFT adds value |
| Neither improves guard-off behavior | The treatment, model or task design may be insufficient |
| Gains disappear under shift | Limited generalization of the learned behavior |
| Intervals are too wide | Inconclusive evidence; use pilot variance to revise the design |
| Guard-on remains safer | External enforcement still supplies protection in this environment |

No outcome establishes formal safety, permanent policy internalization, safe
production guard removal or generalization to other models and tools.
