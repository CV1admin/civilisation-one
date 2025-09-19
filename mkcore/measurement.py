"""Measurement utilities for thin-line simulations."""
from __future__ import annotations

from random import Random
from typing import Dict

from .state import StateVector


def probabilities(state: StateVector) -> list[float]:
    """Return measurement probabilities for the computational basis."""

    probs = [abs(amplitude) ** 2 for amplitude in state]
    total = sum(probs)
    if total == 0:
        raise ValueError("state has zero probability mass")
    return [value / total for value in probs]


def sample_counts(
    state: StateVector, shots: int, rng: Random | None = None
) -> Dict[str, int]:
    """Sample measurement results and return counts keyed by bitstrings."""

    if shots <= 0:
        raise ValueError("shots must be positive")
    if rng is None:
        rng = Random()
    n_qubits = 0
    length = len(state)
    while (1 << n_qubits) < length:
        n_qubits += 1
    if (1 << n_qubits) != length:
        raise ValueError("state vector length is not a power of two")

    probs = probabilities(state)
    cumulative: list[float] = []
    running = 0.0
    for value in probs:
        running += value
        cumulative.append(running)

    counts = {format(index, f"0{n_qubits}b"): 0 for index in range(length)}
    for _ in range(shots):
        r = rng.random()
        for index, threshold in enumerate(cumulative):
            if r <= threshold:
                key = format(index, f"0{n_qubits}b")
                counts[key] += 1
                break
    return counts


def counts_to_signal(counts: Dict[str, int]) -> list[float]:
    """Convert measurement counts to a deterministic signal vector."""

    if not counts:
        raise ValueError("counts dictionary cannot be empty")
    ordered_keys = sorted(counts.keys())
    return [float(counts[key]) for key in ordered_keys]
