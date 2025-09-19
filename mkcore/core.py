"""High level orchestration for MKone thin-line simulations."""
from __future__ import annotations

from dataclasses import dataclass
from random import Random
from typing import List

from .config import DecoderConfig, FeedbackConfig, QuantumConfig, SignalConfig
from .dynamics import apply_single_qubit_gate, entangle_chain, rz
from .measurement import counts_to_signal, sample_counts
from .signal import SimpleSpectrumDecoder, SpectrumResult, fourier_spectrum
from .state import StateVector, normalize, uniform_superposition

ALPHA = 1 / 137  # fine structure constant approximation


@dataclass
class StepResult:
    """Result of a single simulation step."""

    step: int
    detected_pattern: bool
    peak_ratio: float
    spectrum: List[float]


class ThinLineCore:
    """Coordinate the thin-line feedback loop."""

    def __init__(
        self,
        quantum: QuantumConfig | None = None,
        signal: SignalConfig | None = None,
        feedback: FeedbackConfig | None = None,
        decoder: DecoderConfig | None = None,
    ) -> None:
        self._quantum = quantum or QuantumConfig()
        self._signal = signal or SignalConfig()
        self._feedback = feedback or FeedbackConfig()
        self._decoder_config = decoder or DecoderConfig()
        self._rng = Random(self._quantum.random_seed)

        self._decoder = SimpleSpectrumDecoder(self._decoder_config)
        self._state: StateVector = normalize(
            uniform_superposition(self._quantum.n_qubits)
        )

    @property
    def state(self) -> StateVector:
        return list(self._state)

    def _apply_feedback(self, detected_pattern: bool) -> None:
        angle = (
            self._feedback.pattern_rotation
            if detected_pattern
            else self._feedback.noise_rotation
        )
        target = (
            self._feedback.target_qubit
            if detected_pattern
            else self._feedback.perturb_qubit
        )
        gate = rz(angle)
        self._state = apply_single_qubit_gate(
            self._state, gate, target, self._quantum.n_qubits
        )

    def step(self, step_index: int) -> StepResult:
        """Advance the simulation by one iteration."""

        self._state = entangle_chain(self._state, self._quantum.n_qubits)
        rotation = rz(self._quantum.coupling_strength * ALPHA)
        self._state = apply_single_qubit_gate(
            self._state, rotation, 0, self._quantum.n_qubits
        )

        counts = sample_counts(self._state, shots=self._quantum.shots, rng=self._rng)
        signal = counts_to_signal(counts)
        spectrum = fourier_spectrum(signal, self._signal)
        spectrum_result: SpectrumResult = self._decoder.update(spectrum)
        detected = self._decoder.detect()
        self._apply_feedback(detected)
        self._state = normalize(self._state)
        return StepResult(
            step=step_index,
            detected_pattern=detected,
            peak_ratio=spectrum_result.peak_ratio,
            spectrum=spectrum_result.spectrum,
        )

    def run(self, num_steps: int) -> List[StepResult]:
        """Run the full simulation for a number of steps."""

        if num_steps <= 0:
            raise ValueError("num_steps must be positive")
        results: List[StepResult] = []
        for idx in range(num_steps):
            results.append(self.step(idx))
        return results
