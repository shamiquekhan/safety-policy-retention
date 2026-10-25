# Limitations to state explicitly

- The project evaluates observable behavior, not internal representations or
  mechanistic policy knowledge.
- A deterministic validator can be correct for the specified sandbox while the
  policy specification remains incomplete or unrealistic.
- Synthetic secrets, approvals and destinations are not substitutes for real
  organizational authority or data-flow semantics.
- One backbone, a small tool set and a finite scenario suite limit external
  validity.
- Guard-off execution is safe only because the environment has no real external
  side effects; this is not evidence that production guards can be removed.
- Model-generated explanations or constraint fields are not treated as ground
  truth. Only the validator and observed state transitions determine labels.
- Refusal can lower harm while destroying utility, so no single safety number is
  sufficient.
- Seed, decoding and checkpoint variation may change estimates; uncertainty and
  per-seed results are required.
