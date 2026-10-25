"""Training-data builders for the shared-interface SFT comparison."""

from .examples import (
    ACTION_PREFIX,
    POLICY_CHECK_PREFIX,
    TrainingExample,
    build_training_examples,
    validate_training_inputs,
)

__all__ = [
    "ACTION_PREFIX",
    "POLICY_CHECK_PREFIX",
    "TrainingExample",
    "build_training_examples",
    "validate_training_inputs",
]
