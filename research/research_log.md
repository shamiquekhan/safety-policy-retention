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

## Open checks

- Read the full methods and appendices for Harness-Zero, HPD and SafeEvolve.
- Check code availability, exact inference harnesses and whether any ablation
  truly removes runtime enforcement rather than only changing policy prompts.
- Define a search date, databases, query families and inclusion criteria before
  using counts such as “no prior work.”
- Decide whether the final experiment should use an episode-level attempted-
  violation endpoint as the primary estimand, with action-level violation as a
  secondary measure to avoid refusal-denominator artifacts.
