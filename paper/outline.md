# Paper outline

## 1. Introduction

- Tool-using agents rely on runtime mechanisms for permissions, approvals and
  information-flow control.
- Harness distillation shows that some performance/procedural behavior can
  persist after harness removal.
- Runtime compliance with an active guard is not the same as retained safety.
- State the narrow question: matched trajectory-only versus policy-supervised SFT
  (PS-SFT)
  after guard removal under action/state evaluation.
- Bound the contribution and avoid formal-safety language.

## 2. Related work

1. Harness distillation and runtime-semantics supervision.
2. Safety-oriented policy internalization and co-evolution.
3. Runtime enforcement and tool-agent benchmarks.
4. Context-dependent safety and fine-tuning/evaluation reliability.

## 3. Threat model and scope

- Synthetic records, destinations, approvals and tool-returned content.
- Four policy families and the exact prohibited state transitions.
- What is and is not meant by guard removal.

## 4. Method

- Sandbox and deterministic validator.
- Corrected-trajectory and auxiliary policy supervision (PS-SFT).
- Conditions A–D.
- Event log and replayability.
- Template-level data split.

## 5. Experimental setup

- Model revision, tokenizer, training budget and seeds.
- Decoding and episode limits.
- Scenario categories and sample-size rationale.
- Primary and secondary metrics.
- Statistical intervals and paired comparison.

## 6. Results

- Primary C versus B result.
- Safety/utility table by shift type.
- Guard-on reference and guard-off gap.
- Per-policy family and per-seed breakdowns.

## 7. Failure analysis

- Authorization/context confusion.
- Confidentiality leakage.
- Approval omission.
- Tool-output injection susceptibility.
- Refusal/abandonment versus safe alternative selection.

## 8. Limitations and conclusion

- Synthetic policies and one/few backbones.
- Finite scenario coverage and validator assumptions.
- No claim of formal or production safety.
- What a null result means for additional constraint supervision.
