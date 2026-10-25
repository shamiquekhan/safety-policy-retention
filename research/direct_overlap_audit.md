# Direct-overlap audit: Harness-Zero, HPD and SafeEvolve

**Audit date:** 25 October 2026
**Status:** Primary-paper audit completed; repository/code checks recorded where
available. The proposed experiment remains distinct, but the novelty claim is
bounded and provisional.

## Decision

Proceed with the validator-first pilot and the matched B-versus-C experiment.
The reviewed papers establish that harness-induced or runtime-semantic behavior
can transfer into model parameters, including in some guard-free or
harness-free evaluations. None of the three reports the exact comparison in
this repository: the same corrected action trajectories, with versus without a
separate deterministic policy-assessment loss, followed by guard-off proposal
and state-change evaluation in the same synthetic environment.

This is not a claim that prior work failed to study safety transfer. It is a
narrow claim about the remaining controlled comparison.

## Evidence matrix

| Paper | What is trained? | What is absent at inference? | Proposal/state evidence | Utility and split evidence | Exact B-versus-C comparison? |
|---|---|---|---|---|---|
| Harness-Zero | Agent-as-harness reviewed trajectories followed by LoRA SFT. Corrections are expressed in the student's native action space. | The evolved harness, private reference harness and harnessing agent are removed; the target/minimal harness remains. | Evaluates task performance and harness-exclusive behavior recovery. It is not a policy-validator study with attempted-violation and realized-harm endpoints. | Uses benchmark task splits and reports task performance; no matched security-policy utility/non-inferiority analysis. | **No.** It is a direct harness-distillation comparator, not a PS-SFT-versus-trajectory-SFT safety ablation. |
| HPD | Shared model trained on native-context action prediction, document-conditioned action prediction and control-document reconstruction; runtime semantics are made explicit through privileged control documents. | The control document is absent at deployment, but the original harness interface remains. | Reports runtime compliance, reference-path and task metrics; the paper does not establish independent guard-off state-harm measurement. | Reports multiple benchmarks and five-seed comparisons, but not the proposed policy-challenge episode endpoint or matched B/C treatment. | **No.** It is the closest multi-task/runtime-semantics design and motivates separate `[ACTION]` and `[POLICY_CHECK]` tasks. |
| SafeEvolve | Harness-use SFT followed by harness-augmented GRPO, with evolving safety prompts/SkillBanks and rule-based trajectory verifiers. | OPSD is evaluated without runtime-harness assistance, but the main method is a mixed harness/policy co-evolution system. | Table 6 reports guard-free policy internalization metrics: OPSD lowers AgentDojo ASR 2.37→1.84 and AgentDyn ASR 6.88→3.84, while AgentDyn utility falls 15.45→8.88 and AgentHarm harmfulness falls 56.45→43.57. | Includes clean, injection and malicious-query tasks, held-out ASB analysis and separate utility/refusal/harm metrics; still not the matched deterministic B/C comparison. | **No.** It demonstrates partial, metric-dependent safety transfer and a safety–utility trade-off, not PS-SFT superiority over matched corrected-trajectory SFT. |

## Paper and code locations checked

### Harness-Zero

- §3.2–§3.3: agent-as-harness review and SFT on reviewed rollouts.
- §4.3 and Table 2: evolved/reference harness removal and deployment under the
  target harness; distilled performance rises from the base target-harness
  result but is evaluated as task performance.
- §4.5, Table 4 and Appendix G: harness-exclusive behavior recovery.
- Appendix E: LoRA SFT configuration and single-seed training details.
- Official implementation checked: `metaevo-ai/harness-zero`. The repository
  confirms reviewed-trajectory SFT, deployment without `h*`, `K` and the
  harnessing agent, and a target minimal harness rather than an independent
  security guard.

### Harness Policy Distillation

- §3.3.3: three-view training and native deployment.
- §4.1–§4.2 and Table 1: runtime compliance, execution and task metrics.
- §4.4: HPD component and training-schedule ablations.
- Appendix C.3: shared training settings and baseline definitions.
- Appendix E: metric definitions separate reference-action fit, execution
  contract compliance and completion.
- The paper links `HuiCir/HPDCode`, but the linked repository returned a 404
  during this audit. Code availability is therefore recorded as **unverified**,
  not absent.

### SafeEvolve

- §3.2–§3.4: harness evolution, harness-augmented policy optimization and the
  co-evolution loop.
- §4.1 and Appendix A.1: finite-state Python simulators, structured tool calls,
  trajectory verifiers and benchmark setup.
- Table 2/Appendix B: frozen-policy harness-only evaluation.
- Table 6/Appendix B: OPSD safety internalization without runtime-harness
  assistance at test time.
- Appendix A.5–A.6: backbones, training schedule and four-H200 compute setup.
- Official implementation checked: `MaoPopovich/SafeEvolve`. The repository
  contains separate runtime, SFT and GRPO stacks, confirming that the main
  method is substantially more mixed than the proposed SFT-only intervention.

## Consequence for this repository

The direct-overlap audit changes the framing, not the experiment:

1. Do not claim that safety-after-guard-removal is unexplored.
2. Keep Harness-Zero as the harness-distillation comparator.
3. Keep HPD as the runtime-semantics and multi-task-supervision comparator.
4. Keep SafeEvolve as the strongest safety-transfer and safety–utility
   comparator.
5. State the contribution as a matched, validator-backed B-versus-C SFT
   comparison with action-only inference, independent guard-off execution,
   proposal/state logging and template-level structural splits.

The decision gate is **go**, subject to the pilot exit criteria in the protocol.
