from __future__ import annotations

import json
import math
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class _SimpleCircuit:
    num_qubits: int
    depth_value: int = 0
    encoded_probs: list[float] | None = None

    def depth(self) -> int:
        return self.depth_value


class XiQuantumPipeline:
    """Classical Ξ evolution -> quantum-style encoding -> synthetic observables."""

    def __init__(
        self,
        cfg_path: str = "configs/phase_diagram.yaml",
        lambda_ent: float = 0.1,
        n_spatial: int = 4,
        qubits_per_point: int = 3,
    ) -> None:
        self.cfg = self._load_cfg(cfg_path)
        self.lambda_ent = lambda_ent
        self.n_spatial = n_spatial
        self.qubits_per_point = qubits_per_point
        self.total_qubits = n_spatial * qubits_per_point

    def _load_cfg(self, cfg_path: str) -> dict[str, float]:
        p = Path(cfg_path)
        if not p.exists():
            return {"dx": 1.0}
        text = p.read_text().strip().splitlines()
        cfg: dict[str, float] = {"dx": 1.0}
        for line in text:
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            try:
                cfg[k.strip()] = float(v.strip())
            except ValueError:
                pass
        return cfg

    def _normalize_mass(self, xi: list[float]) -> list[float]:
        dx = self.cfg.get("dx", 1.0)
        mass = sum(xi) * dx
        if abs(mass) < 1e-14:
            return [1.0 / (len(xi) * dx) for _ in xi]
        return [v / mass for v in xi]

    def evolve_classical(self, steps: int = 100) -> list[list[float]]:
        xi = [1.0 / (self.n_spatial * self.cfg.get("dx", 1.0)) for _ in range(self.n_spatial)]
        history: list[list[float]] = []
        for _ in range(steps):
            # local smoothing + entropy-like damping, then re-normalize mass
            xi_next: list[float] = []
            for i, val in enumerate(xi):
                left = xi[(i - 1) % len(xi)]
                right = xi[(i + 1) % len(xi)]
                lap = left - 2.0 * val + right
                ent = -val * math.log(max(val * val, 1e-12))
                xi_next.append(val + 0.01 * (lap + self.lambda_ent * ent))
            xi = self._normalize_mass(xi_next)
            history.append(xi.copy())
        return history

    def encode_snapshot(self, xi_snap: list[float], theta: float = 0.1) -> Any:
        probs = [min(max(abs(v), 0.0), 1.0) for v in xi_snap[: self.n_spatial]]
        total = sum(probs) or 1.0
        probs = [p / total for p in probs]

        # Fallback circuit object (works in test/runtime without qiskit)
        circuit = _SimpleCircuit(num_qubits=self.total_qubits, depth_value=self.n_spatial + 3)
        circuit.encoded_probs = probs
        return circuit

    def measure_observables(self, qc: Any, shots: int = 4096) -> tuple[list[float], dict[str, int]]:
        probs = getattr(qc, "encoded_probs", None) or [1.0 / self.n_spatial] * self.n_spatial
        counts: dict[str, int] = {}

        # Sample synthetic bitstrings from local probabilities.
        for _ in range(shots):
            idx = random.choices(range(len(probs)), weights=probs, k=1)[0]
            bitstring = format(idx, f"0{self.total_qubits}b")
            counts[bitstring] = counts.get(bitstring, 0) + 1

        norm = float(shots)
        p = [counts.get(format(i, f"0{self.total_qubits}b"), 0) / norm for i in range(min(32, 2**self.total_qubits))]
        # Lightweight frequency proxy: DFT magnitude for first bins.
        spectrum: list[float] = []
        n = len(p)
        for k in range(n):
            re = 0.0
            im = 0.0
            for t, pt in enumerate(p):
                ang = -2.0 * math.pi * k * t / n
                re += pt * math.cos(ang)
                im += pt * math.sin(ang)
            spectrum.append(math.sqrt(re * re + im * im))
        return spectrum, counts

    def run_full_pipeline(self, classical_steps: int = 80, shots: int = 4096) -> list[float]:
        Path("outputs").mkdir(exist_ok=True)

        history = self.evolve_classical(classical_steps)
        final_xi = history[-1]

        qc = self.encode_snapshot(final_xi[: self.n_spatial])
        spectrum, counts = self.measure_observables(qc, shots)

        Path("outputs/quantum_spectrum.json").write_text(json.dumps(spectrum))
        top_counts = dict(sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:20])
        Path("outputs/quantum_counts.json").write_text(json.dumps(top_counts, indent=2))

        print("✅ Pipeline complete")
        print(f"   Final max|Ξ|: {max(abs(v) for v in final_xi):.5f}")
        print(f"   Quantum spectrum bins: {len(spectrum)}")
        print("   Saved to outputs/")
        return spectrum
