# Candidate literature from the 25 October 2026 search

This file preserves search-result candidates that may matter to the gap audit.
They are **not** evidence for a novelty claim until the primary paper, version,
methods and evaluation setup are checked. Search-engine summaries and generated
“key takeaways” can omit whether a guard remains active, so they are tracked
separately from `literature_matrix.csv`.

## Likely adjacent to training or policy internalization

- **PREFINE: Preference-based Implicit Reward and Cost Fine-tuning for Safety
  Alignment.** Potentially relevant to safety/utility constrained optimization,
  but the described Safety Gym/Bullet Gym setting is not the proposed stateful
  tool-agent guard-removal comparison.
- **From Hard Refusals to Safe-Completions.** Relevant to refusal versus useful
  completion, but text output safety is not action/state retention.
- **Learning from Runtime Feedback through Failure-Bank Self-Evolution for
  Vision-Language-Action Models.** Potentially relevant to persistent policy
  improvement from runtime feedback, but VLA control and tool-agent policy
  retention are different settings.
- **PolicyAlign** and **RePolicy.** Potentially relevant to policy-conditioned
  alignment or policy invocation; check whether deployment retains an external
  guard and whether actions are executed in a stateful environment.
- **SafePyramid** and **Policy-Invisible Violations in LLM-Based Agents.**
  Potentially relevant to hidden facts, policy context and hierarchical
  evaluation; check whether they include training or only guard evaluation.

## Runtime enforcement rather than retention

- **A GHOST in Long-Horizon Agents**, **AdaGuard**, **PolicyGuide**,
  **PolicyGuard**, **ShieldAgent**, **GuardAgent**, **ActGov**, **ActPlane**,
  **Guardrails as Infrastructure**, and **Runtime Governance for AI Agents.**
  These may strengthen the argument that runtime enforcement is an important
  reference condition. They do not automatically close the proposed gap because
  active enforcement can prevent execution without changing the model's
  unguarded proposal distribution.
- **What Can Be Enforced?** Potentially useful for formalizing what deterministic
  runtime gates can guarantee. It should inform the threat-model language, not be
  treated as empirical evidence of learned retention.
- **The Verifier Tax.** Potentially relevant to safety/utility and intervention
  cost. Check whether the paper measures unguarded behavior or only the cost of
  keeping a verifier active.

## How to process these candidates

For each candidate, record:

1. exact primary URL and version/date;
2. whether training changes model parameters;
3. whether the guard is active at test time;
4. whether proposed and executed actions are separately logged;
5. whether state/context shift is held out by structure rather than wording;
6. whether the model is compared against an equal-budget trajectory-only
   baseline; and
7. whether the result is about safety, utility, intervention cost or formal
   enforcement.

Only a paper satisfying the relevant fields should be allowed to displace the
current gap statement. In particular, a high active-guard compliance score is not
evidence that policy-supervised SFT (PS-SFT) improves guard-off retention.
