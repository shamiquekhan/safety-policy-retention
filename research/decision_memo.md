# Decision memo: is the proposed PS-SFT study still worth doing?

**Date:** 25 October 2026
**Status:** Primary-paper audit completed; code availability and implementation
details are recorded in `research/direct_overlap_audit.md`.

## 1. What has already been done?

### Harness-Zero

Harness-Zero uses an optimized harness and an agent-as-harness process to
generate corrected demonstrations, then fine-tunes a model so behavior induced
by the specialized harness can persist after that harness is removed. Its
headline evidence is performance and behavior-pattern recovery across knowledge
work, tool-use and science domains. This establishes that some harness-induced
behavior can transfer into weights; it does not isolate safety policy retention
or compare trajectory-only SFT with explicit policy labels.

### Harness Policy Distillation (HPD)

HPD makes runtime control semantics explicit training targets alongside actions,
using control documents and harness verification. Its reported deployment uses
the original harness interface and measures autonomous task success and runtime
compliance. This is a direct methodological competitor for structured runtime
supervision, but it does not by itself establish post-guard-removal safety or
realized sandbox-harm retention.

### SafeEvolve

SafeEvolve co-evolves harness artifacts and model policy using harness-use SFT
and harness-augmented RL. It is the closest safety-oriented comparator and
reports a safety-utility trade-off on agent benchmarks. Its training stack mixes
multiple interventions and does not answer the clean causal comparison proposed
here: the same corrected data, with or without auxiliary constraint
supervision, evaluated with the guard genuinely disabled.

The refined audit makes this comparator more important, not less. SafeEvolve's
policy-only/OPSD-style results support partial, metric-dependent safety transfer
without establishing that explicit constraint-labelled SFT beats trajectory-only
SFT. Safety and utility can move in opposite directions, so the exact tables and
supplementary setup remain required full-text/code checks rather than evidence of
a blank post-removal literature.

### Existing evaluation work

AgentDojo establishes a dynamic tool environment for prompt-injection attacks
and defenses. ClawsBench shows that capability and unsafe-action rates can
diverge in realistic simulated productivity workflows. SafeClawBench separates
semantic acceptance, audit evidence and sandbox-observed harm. Context-flip work
motivates paired state changes in which a previously safe-looking action becomes
unsafe. Fine-tuning reliability work motivates multiple seeds and repeated
decoding measurements. These works inform the protocol but do not provide the
proposed training-signal comparison.

### Adjacent training and enforcement methods

Policy-specific alignment, safe-completion training, proximal SFT and preference-
based safety optimization motivate alternative training interventions, but they
should not be conflated with PS-SFT. In particular, PREFINE belongs in the
adjacent-methods discussion because it studies preference-based reward/cost
fine-tuning for sequential continuous-control policies rather than the proposed
stateful tool-agent guard-removal comparison. Runtime systems such as PolicyGuide,
ActPlane, AdaGuard and policy-first tooling are useful guard-on references, not
direct evidence of retained unguarded behavior.

## 2. What remains different enough to justify the study?

The defensible gap is **not** “nobody has distilled harness behavior,” “nobody
has internalized policies,” or “nobody has evaluated safety after training.” The
remaining comparison is narrower:

> In the same stateful synthetic tool environment, does adding deterministic
> decision-level policy supervision—called policy-supervised SFT (PS-SFT)
> here—to corrected-trajectory SFT improve guard-off action selection over
> trajectory-only SFT, when the test split holds out rule combinations, context
> flips and untrusted tool-output attacks, while preserving benign completion?

Four controls make this gap meaningful:

1. **Matched training inputs:** both variants use the same corrected trajectories,
   scenario count, data volume and optimization budget.
2. **Matched deployment:** both variants receive the same policy text, tool
   schema and output format; only the training loss differs.
3. **Genuine guard ablation:** the guard cannot block or rewrite actions in the
   guard-off arm; the validator only labels proposals and state changes.
4. **Separated endpoints:** attempted proposals, executed actions, sandbox harm,
   benign success and false refusal are logged independently.

This gap is viable only if the full-text/code audit does not reveal an existing
paper with all four controls.

HPD and SafeEvolve must remain in the direct-overlap audit. They are not
irrelevant to this question: HPD explicitly supervises runtime semantics, and
SafeEvolve combines harness-use SFT with harness-augmented RL. The narrower
candidate contribution is the matched SFT-only comparison in which corrected
trajectories are held constant while policy supervision changes, followed by
guard-disabled action/state evaluation under held-out shifts.

## 3. What result would still be worth reporting?

- **Positive:** PS-SFT reduces the prespecified guard-off episode-level violation
  endpoint with a confidence interval that excludes a practically negligible
  effect, without an unacceptable drop in benign success.
- **Negative/null:** it does not improve retention, or its gain disappears after
  controlling for refusal and competence. This would challenge the value of the
  extra supervision and be useful if the comparison is well powered and clean.
- **Failure-mode result:** both methods perform well on familiar scenarios but
  fail on context flips or indirect injection in a repeatable, validator-backed
  way. That is a useful characterization of safety-transfer limits.
- **Inconclusive:** intervals are too wide, benign competence is too low, labels
  or logging fail validation, or a direct duplicate is discovered. Report the
  pilot as a feasibility result and revise the design rather than forcing a
  conclusion.

## Decision

Proceed to a small validator-first sandbox and a pilot, but keep the novelty
claim provisional. Do not fine-tune or scale the benchmark until the pilot
demonstrates both benign task competence and observable unsafe proposals. Keep
optimizer-level safety methods, RL, a second backbone and a large benchmark out
of the first comparison.

The primary-paper audit is now complete. Harness-Zero, HPD and SafeEvolve remain
direct comparators, but none reports the exact matched B-versus-C design with
action-only inference, an independently disabled guard and deterministic
proposal/state-harm logging. Proceed to the validator-first pilot, with the
remaining go/no-go gate being measurement validity and model competence rather
than further literature expansion.
