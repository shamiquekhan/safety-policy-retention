# Updated execution roadmap

This roadmap narrows the project to one training comparison: corrected-trajectory
SFT versus policy-supervised SFT (PS-SFT). Runtime guards, long-horizon failures,
context flips and indirect prompt injection are evaluation conditions or
reference arms, not additional training mechanisms in the first study.

The first milestone is not a trained checkpoint. It is a literature decision and
a deterministic validator whose labels and state transitions can be tested.

## Research scope

### Main question

In a controlled tool-using environment, does adding explicit policy supervision
to corrected-trajectory SFT reduce proposed policy-violating tool actions after
an independent runtime guard is disabled, compared with trajectory-only SFT,
while preserving legitimate task completion under held-out contextual and
compositional shifts?

### Core conditions

- **A — Base:** original instruction-tuned model with written policy, guard off.
- **B — Trajectory-only SFT:** corrected safe actions and trajectories, guard off.
- **C — PS-SFT:** the same action targets plus explicit compliance/rule
  supervision, guard off.
- **D — Guarded references:** base and trained policies with the runtime guard on.

The primary comparison is B versus C. A tests whether corrected training moves
behavior at all. D estimates protection supplied by external enforcement.

### Policy families and stress conditions

Policy families:

1. authorization;
2. confidentiality/information flow; and
3. approval gating.

Stress conditions:

- familiar scenarios;
- held-out compositional combinations;
- context flips where state facts change the correct action;
- indirect prompt injection through untrusted tool outputs; and
- optional long-horizon retention of earlier constraints.

## First three days

### Day 1 — direct-overlap audit

Read the methods, ablations, limitations, supplementary material and code for
SafeEvolve, Harness-Zero and HPD. Record:

- exact training signal and data;
- components retained during evaluation;
- whether guard removal is genuine;
- proposed-action, executed-harm and utility metrics;
- distribution shifts; and
- exact tables/sections supporting each claim.

**Deliverable:** updated priority literature matrix and novelty memo.

### Day 2 — treatment specification

Write a one-page PS-SFT specification covering:

- compliance, rule and approval labels;
- action-generation target shared with trajectory-only SFT;
- auxiliary loss or shared-backbone head;
- what is identical across conditions;
- what differs; and
- how the deployment interface remains equivalent.

**Deliverable:** frozen draft of the treatment section in
`research/experiment_protocol.md`.

### Day 3 — paired pilot scenarios

Write 5–10 paired scenarios before running a model. Cover authorization,
confidentiality, approval gating and at least one context change. Specify the
expected action, policy result, guard intervention and state mutation in data.

**Deliverable:** `data/splits/pilot_scenarios.jsonl` plus validator test cases.

## Ten-week plan

### Week 1 — direct-overlap literature audit

Finish the priority-1 comparison and classify newer papers as policy training,
harness transfer, runtime enforcement, contextual failure or alternative
optimization.

**Exit:** the gap is stated as a conditional candidate, not as “no prior work.”

### Week 2 — question and protocol freeze

Freeze the main question, H1–H4, core conditions, primary episode-level outcome,
action-level secondary outcome, utility outcomes and guard-off semantics.

**Exit:** no design choice is being selected after seeing main results.

### Week 3 — sandbox and validator

Implement synthetic state, `read_record`, `update_record`, `send_message` and
`request_approval`. Add deterministic validators and a measurement-only mode.

**Tests:** allowed/unauthorized access, secret-flow boundaries, missing/valid
approval, context changes, injected instructions and state hashes.

**Exit:** replaying an episode reproduces labels and state transitions.

### Week 4 — scenario construction and base pilot

Create template-disjoint train/dev/test manifests. Run the base model in guarded
and unguarded modes. Verify benign task competence and observable but not
artificially manufactured unsafe proposals.

**Exit:** event logs reconstruct proposal, intervention, execution and state.

### Week 5 — corrected data and audit

Generate corrected trajectories and PS-SFT labels. Mechanically verify target
actions, policy labels, duplicates, leakage, balance and benign coverage.

**Exit:** freeze dataset and split hashes before selecting a main checkpoint.

### Week 6 — training implementation

Train B and C with matched action targets, token budgets, optimizer steps,
checkpoint rules and seeds. Use an auxiliary policy objective for C where the
stack supports it; otherwise label a structured-output treatment as exploratory.

**Exit:** both methods learn the tool schema without silent parser failures.

### Week 7 — pilot training and debugging

Run at least three training seeds if resources permit. Inspect safety, benign
success, refusal and action-format variance before fixing the main sample size.

**Exit:** the pilot can distinguish capability failure, refusal and policy
failure.

### Week 8 — main guard-disabled evaluation

Run the frozen held-out test set for B and C, plus the base and guard-on
references. Keep the validator read-only and the executor synthetic in guard-off
conditions.

**Exit:** raw logs and configuration hashes are complete.

### Week 9 — statistical analysis and failure taxonomy

Report primary episode violation incidence, action-level violation rate,
safe/benign success, sandbox harm, false refusals and guard interventions with
confidence intervals. Break down results by policy family and shift type.

**Exit:** all reported numbers regenerate from raw logs.

### Week 10 — paper and reproducibility package

Write methods, results, limitations and related work. Release code, configs,
synthetic fixtures, split manifests and redacted logs where licensing permits.

**Exit:** the paper makes only bounded behavioral claims.

## Literature decision gate

Do not start the main experiment until the audit answers:

- Does SafeEvolve already compare the exact supervision signals under guard-off
  evaluation?
- Does HPD's runtime-compliance evaluation cover an independent safety guard and
  the intended action/state outcome?
- Does PolicyAlign or another policy-specific method already run the equivalent
  matched comparison?
- Are the planned context shifts distinct from GHOST, Policy-Invisible
  Violations and related work?

If an exact comparison exists, pivot to a demonstrably missing outcome, shift or
failure mode instead of preserving the original novelty claim.

## Stop/revise rules

- If the validator cannot distinguish allowed and prohibited state transitions,
  stop model work and fix the environment.
- If the base model cannot complete benign tasks, simplify tools or change the
  model before interpreting safety.
- If the base model never proposes unsafe actions, improve diagnostic coverage;
  do not manufacture incorrect labels.
- If PS-SFT lowers violations only by refusing or abandoning tasks, report a
  safety–utility trade-off rather than an unqualified improvement.
- If estimates vary substantially across seeds, increase replication or narrow
  the claim.
- If confidence intervals are too wide, report an inconclusive pilot and use the
  observed variance to justify a revised test size.

## Compute boundary

The local 4 GB GPU is suitable for sandbox development, validator tests, small
pilots and pipeline checks. Multi-seed fine-tuning may require rented GPU access
or a collaborator's hardware. Do not add RL, optimizer-level safety constraints,
a second backbone and a large benchmark to the initial study.
