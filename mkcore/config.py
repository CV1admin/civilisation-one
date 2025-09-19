"""Configuration dataclasses for the MK core simulation."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class QuantumConfig:
    """Configuration describing the base quantum model parameters."""

    n_qubits: int = 6
    shots: int = 256
    coupling_strength: float = 0.1
    random_seed: Optional[int] = None

    def __post_init__(self) -> None:
        if self.n_qubits <= 0:
            raise ValueError("n_qubits must be positive")
        if self.shots <= 0:
            raise ValueError("shots must be positive")
        if self.coupling_strength < 0:
            raise ValueError("coupling_strength must be non-negative")


@dataclass(frozen=True)
class SignalConfig:
    """Configuration for converting measurements into spectra."""

    normalize: bool = True
    epsilon: float = 1e-12

    def __post_init__(self) -> None:
        if self.epsilon <= 0:
            raise ValueError("epsilon must be positive")


@dataclass(frozen=True)
class FeedbackConfig:
    """Configuration of the feedback actions applied to the circuit."""

    pattern_rotation: float = 0.05
    noise_rotation: float = 0.02
    target_qubit: int = 1
    perturb_qubit: int = 2

    def __post_init__(self) -> None:
        for angle_name in ("pattern_rotation", "noise_rotation"):
            if getattr(self, angle_name) < 0:
                raise ValueError(f"{angle_name} must be non-negative")
        if self.target_qubit < 0:
            raise ValueError("target_qubit must be non-negative")
        if self.perturb_qubit < 0:
            raise ValueError("perturb_qubit must be non-negative")


@dataclass(frozen=True)
class DecoderConfig:
    """Configuration for the lightweight spectrum decoder."""

    threshold: float = 1.5
    smoothing: float = 0.25
    history: int = 5

    def __post_init__(self) -> None:
        if self.threshold <= 0:
            raise ValueError("threshold must be positive")
        if not 0 <= self.smoothing <= 1:
            raise ValueError("smoothing must be between 0 and 1")
        if self.history <= 0:
            raise ValueError("history must be positive")
