from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import json

from .center_node import VireaxCenterNode


@dataclass
class ResearchIteration:
    iteration: int
    mode: str
    conceptual_insight: str
    mathematical_mapping: str
    integration_note: str
    next_step: str


class VireaxResearchEngine:
    """Implements the recursive intelligence loop across Q/D/E/I layers."""

    VALID_MODES = {"simulation", "synthesis", "discovery", "optimization"}

    def __init__(self, mode: str = "simulation") -> None:
        mode = mode.lower().strip()
        if mode not in self.VALID_MODES:
            raise ValueError(f"Invalid mode: {mode}")
        self.mode = mode
        self.node = VireaxCenterNode()

    def _mapping_for_mode(self) -> str:
        if self.mode == "simulation":
            return "∂tΞ ≈ D∇²Ξ − ∂V/∂Ξ + λI(Ξ), sampled into circuit observables"
        if self.mode == "synthesis":
            return "Map equation-table relations to circuit-level couplings via shared conserved quantities"
        if self.mode == "discovery":
            return "Search parameter perturbations δ around baseline and evaluate structural invariants"
        return "Minimize model error under constraints: mass conservation + free-energy monotonicity"

    def run(self, iterations: int = 2) -> list[ResearchIteration]:
        results: list[ResearchIteration] = []
        for i in range(1, iterations + 1):
            node_state = self.node.run()
            insight = (
                f"Iteration {i}: {self.mode} mode executed across Q/D/E/I with "
                f"{node_state['em_rows']} EM rows and backend={node_state['quantum']['backend']}"
            )
            item = ResearchIteration(
                iteration=i,
                mode=self.mode,
                conceptual_insight=insight,
                mathematical_mapping=self._mapping_for_mode(),
                integration_note="Center node state persisted to outputs/vireax_center_node.json",
                next_step="Increase mode depth and compare invariants against baseline",
            )
            results.append(item)

        Path("outputs").mkdir(exist_ok=True)
        Path("outputs/vireax_research_log.json").write_text(
            json.dumps([asdict(r) for r in results], indent=2)
        )
        return results
