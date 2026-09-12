from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from .api_layer import APIMessage, VireaxAPILayer
from .data_pipeline import EMSpectrumPipeline
from .equation_framework import PhysicsEquationFramework
from .quantum_circuit import QuantumFieldCircuit


class VireaxCenterNode:
    """Unified orchestration hub for quantum/data/equation/API subsystems."""

    def __init__(self) -> None:
        self.quantum = QuantumFieldCircuit()
        self.data = EMSpectrumPipeline()
        self.equations = PhysicsEquationFramework()
        self.api = VireaxAPILayer()

    def run(self) -> dict:
        circuit = self.quantum.build(theta=0.1)
        q_summary = asdict(self.quantum.summarize(circuit))

        em_rows = self.data.load_rows(limit=8)
        eq = self.equations.synthesize_relation("energy")

        api_state = self.api.route(APIMessage(route="/state", payload={"quantum": q_summary, "em_rows": len(em_rows)}))

        result = {
            "quantum": q_summary,
            "em_rows": len(em_rows),
            "equation_match": eq,
            "api": api_state,
        }
        Path("outputs").mkdir(exist_ok=True)
        Path("outputs/vireax_center_node.json").write_text(json.dumps(result, indent=2))
        return result
