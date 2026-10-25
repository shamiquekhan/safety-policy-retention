# Research question: safety-policy retention after guard removal

**Status:** Draft candidate question, 25 October 2026
**Working title:** *Safety Policy Retention after Guard Removal: A Controlled
Comparison of Trajectory and Constraint Supervision in Tool-Using LLM Agents*

## Question

Does explicit policy-constraint supervision reduce policy-violating tool-action
proposals after an independent runtime guard is disabled, compared with
corrected-trajectory supervised fine-tuning (SFT), while preserving legitimate
task completion under held-out compositional, context-flip and synthetic
indirect-prompt-injection conditions?

The question is intentionally narrower than “does the model become intrinsically
safe?” It asks about observable behavioral retention in one deterministic,
sandboxed environment and one or more named model checkpoints.

## Definitions

- **Runtime guard:** a separate executable component that can block, rewrite or
  require approval for a proposed tool action before execution.
- **Harness:** the surrounding agent system, including prompts, tool schemas,
  state management, permissions, guard logic and executor.
- **Policy retention:** the degree to which the trained model continues to emit
  policy-compliant actions when the specified enforcement guard is disabled,
  with the policy validator used only for measurement.
- **Distribution shift:** a change in policy combination, state facts or
  adversarial tool content—not merely a paraphrase of a training prompt.
- **Attempted violation:** a policy-invalid action proposal, whether or not a
  guard later blocks it.
- **Realized harm:** a prohibited mutation of synthetic sandbox state.

## Candidate conditions

The main causal comparison is:

1. **Trajectory SFT:** corrected safe trajectories only.
2. **Constraint-aware SFT:** the same corrected trajectories plus deterministic,
   decision-level constraint labels, trained with an auxiliary loss.

The study should also include a base-policy guard-off reference, a policy-prompt
baseline, a guarded base reference and guard-on versions of the trained models.
All arms must use the same model family, tool interface, policy text, scenario
templates, decoding settings and evaluation state.

## Hypotheses

- **H1:** Corrected-trajectory SFT lowers familiar-scenario attempted-violation
  rates relative to the unadapted base model.
- **H2:** Constraint-aware SFT lowers post-guard-removal attempted-violation
  rates relative to trajectory-only SFT on the same held-out scenarios.
- **H3:** Both trained conditions lose some safety or utility under unseen rule
  combinations, context flips or injected tool outputs.
- **H4:** Some apparent safety gains are explained by refusal or abandonment;
  therefore safety must be interpreted jointly with benign task success and
  false-refusal rate.

## Potential contribution

The contribution is publishable only if the final, verified study establishes at
least one bounded result:

- a matched comparison of two training signals after guard removal;
- a reproducible action/state logging and validation protocol;
- a specific, repeatable failure mode under compositional or contextual shift;
- or a useful null result showing that additional constraint labels do not help
  after controlling for data volume, optimization budget and task competence.

The work must not claim that guard removal proves policy internalization, that a
low violation rate is formal safety, or that a synthetic benchmark transfers to
production deployments.

## Assumptions and limitations

- The first study may use one open-weight backbone to keep the comparison
  controlled; claims will then be limited to that model and setting.
- Policies are synthetic, deterministic and intentionally small. They represent
  authorization, confidentiality, approval gating and resistance to untrusted
  tool-output instructions.
- The validator is ground truth for the sandbox, but validator correctness does
  not establish that the policies are complete or realistic.
- A guard-off execution arm is unsafe only inside the synthetic environment; no
  real external side effects are permitted.
- The novelty claim remains provisional until the closest papers, appendices,
  code releases and citation graph have been checked using the matrix in this
  repository.

## Decision gate before implementation

Do not begin fine-tuning until the decision memo answers whether the study is
different from Harness-Zero, Harness Policy Distillation, SafeEvolve, policy
internalization work and existing agent safety benchmarks. If the exact matched
comparison is already reported, narrow the question or change the evaluation
shift rather than building a larger system.
