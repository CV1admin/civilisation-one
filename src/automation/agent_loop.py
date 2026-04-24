from __future__ import annotations

from dataclasses import dataclass

from src.extensions.cosmology_solver import best_delta


@dataclass
class IterationResult:
    iteration: int
    best_delta: float
    error: float


def run_agent_loop(iterations: int = 3) -> list[IterationResult]:
    results: list[IterationResult] = []
    for i in range(iterations):
        delta, err = best_delta()
        results.append(IterationResult(iteration=i + 1, best_delta=delta, error=err))
    return results
