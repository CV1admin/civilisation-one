"""Dynamics for thin-line simulations."""
from __future__ import annotations

from cmath import exp
from math import sqrt
from typing import List, Sequence, Tuple

from .state import StateVector

Matrix2 = Tuple[Tuple[complex, complex], Tuple[complex, complex]]

HADAMARD: Matrix2 = (
    (1 / sqrt(2), 1 / sqrt(2)),
    (1 / sqrt(2), -1 / sqrt(2)),
)


def rz(theta: float) -> Matrix2:
    """Rotation around the Z axis."""

    half = theta / 2
    return ((exp(-1j * half), 0j), (0j, exp(1j * half)))


def apply_single_qubit_gate(
    state: StateVector, gate: Matrix2, qubit: int, n_qubits: int
) -> StateVector:
    """Apply a single-qubit gate to the state vector."""

    if qubit < 0 or qubit >= n_qubits:
        raise ValueError("qubit index out of range")
    result = list(state)
    stride = 1 << qubit
    period = stride << 1
    for start in range(0, len(state), period):
        for offset in range(stride):
            zero_index = start + offset
            one_index = zero_index + stride
            zero_amp = state[zero_index]
            one_amp = state[one_index]
            result[zero_index] = gate[0][0] * zero_amp + gate[0][1] * one_amp
            result[one_index] = gate[1][0] * zero_amp + gate[1][1] * one_amp
    return result


def apply_controlled_x(
    state: StateVector, control: int, target: int, n_qubits: int
) -> StateVector:
    """Apply a controlled-X gate to the state vector."""

    if control == target:
        raise ValueError("control and target must be different")
    if not (0 <= control < n_qubits and 0 <= target < n_qubits):
        raise ValueError("qubit index out of range")
    result = list(state)
    for index in range(len(state)):
        if ((index >> control) & 1) == 1 and ((index >> target) & 1) == 0:
            flipped = index ^ (1 << target)
            result[index], result[flipped] = result[flipped], result[index]
    return result


def entangle_chain(state: StateVector, n_qubits: int) -> StateVector:
    """Apply a chain of controlled-X gates between neighbouring qubits."""

    for qubit in range(n_qubits - 1):
        state = apply_controlled_x(state, qubit, qubit + 1, n_qubits)
    return state


def apply_hadamard_all(state: StateVector, n_qubits: int) -> StateVector:
    """Apply Hadamard to every qubit."""

    for qubit in range(n_qubits):
        state = apply_single_qubit_gate(state, HADAMARD, qubit, n_qubits)
    return state
