"""Utilities for preparing thin-line quantum states."""
from __future__ import annotations

from math import sqrt
from typing import List

StateVector = List[complex]


def basis_state(index: int, n_qubits: int) -> StateVector:
    """Return a computational basis state as a complex vector."""

    dimension = 1 << n_qubits
    if index < 0 or index >= dimension:
        raise ValueError("index out of range for number of qubits")
    state = [0j] * dimension
    state[index] = 1 + 0j
    return state


def uniform_superposition(n_qubits: int) -> StateVector:
    """Return the |+...+> state by applying Hadamards to |0>."""

    amplitude = 1 / sqrt(1 << n_qubits)
    return [amplitude + 0j] * (1 << n_qubits)


def normalize(state: StateVector) -> StateVector:
    """Normalize a state vector to unit length."""

    norm_sq = sum((abs(amplitude) ** 2 for amplitude in state))
    if norm_sq == 0:
        raise ValueError("cannot normalize zero vector")
    norm = sqrt(norm_sq)
    return [amplitude / norm for amplitude in state]
