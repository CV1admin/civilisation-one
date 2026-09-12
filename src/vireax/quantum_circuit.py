from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class QuantumSummary:
    qubits: int
    depth: int
    backend: str


class QuantumFieldCircuit:
    """Qiskit-compatible quantum field circuit with deterministic fallback."""

    def __init__(self, n_nodes: int = 2, qubits_per_node: int = 3) -> None:
        self.n_nodes = n_nodes
        self.qubits_per_node = qubits_per_node
        self.n_qubits = n_nodes * qubits_per_node

    def build(self, theta: float = 0.1) -> Any:
        try:
            from qiskit import QuantumCircuit  # type: ignore
        except Exception:
            return {"type": "fallback", "qubits": self.n_qubits, "theta": theta, "depth": 4}

        qc = QuantumCircuit(self.n_qubits)
        for i in range(0, self.n_qubits, self.qubits_per_node):
            qc.h(i)
            qc.rz(theta, i)
        for i in range(0, self.n_qubits - self.qubits_per_node, self.qubits_per_node):
            qc.cx(i, i + self.qubits_per_node)
        return qc

    def summarize(self, circuit: Any) -> QuantumSummary:
        if isinstance(circuit, dict):
            return QuantumSummary(qubits=circuit["qubits"], depth=circuit["depth"], backend="fallback")
        return QuantumSummary(qubits=circuit.num_qubits, depth=circuit.depth(), backend="qiskit")
