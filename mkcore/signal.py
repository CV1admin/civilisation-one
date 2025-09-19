"""Signal processing utilities for the thin-line core."""
from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import isfinite, pi
from statistics import mean, median
from typing import Deque, Iterable, List

from cmath import exp

from .config import DecoderConfig, SignalConfig


@dataclass
class SpectrumResult:
    """Container for processed spectra and diagnostic metrics."""

    spectrum: List[float]
    peak_ratio: float


def _real_fft(signal: Iterable[float]) -> List[complex]:
    values = list(signal)
    n = len(values)
    result: List[complex] = []
    for k in range(n // 2 + 1):
        total = 0j
        for t, value in enumerate(values):
            angle = -2j * pi * k * t / n
            total += value * exp(angle)
        result.append(total)
    return result


def fourier_spectrum(signal: Iterable[float], config: SignalConfig) -> List[float]:
    """Compute the magnitude spectrum of a discrete signal."""

    complex_spectrum = _real_fft(signal)
    magnitudes = [abs(value) for value in complex_spectrum]
    if config.normalize and magnitudes:
        maximum = max(magnitudes)
        scale = maximum + config.epsilon
        magnitudes = [value / scale for value in magnitudes]
    return magnitudes


class SimpleSpectrumDecoder:
    """A lightweight adaptive decoder for identifying spectral patterns."""

    def __init__(self, config: DecoderConfig) -> None:
        self._config = config
        self._history: Deque[float] = deque(maxlen=config.history)
        self._baseline = 1.0

    def update(self, spectrum: List[float]) -> SpectrumResult:
        """Update the decoder state with a new spectrum."""

        if not spectrum:
            raise ValueError("spectrum cannot be empty")
        peak = max(spectrum)
        med = median(spectrum)
        ratio = peak / (med + 1e-9)
        if not isfinite(ratio):
            ratio = 0.0

        self._history.append(ratio)
        averaged = mean(self._history)
        self._baseline = (
            self._config.smoothing * averaged
            + (1 - self._config.smoothing) * self._baseline
        )
        return SpectrumResult(spectrum=list(spectrum), peak_ratio=ratio)

    def detect(self) -> bool:
        """Return True when the adaptive ratio exceeds the threshold."""

        return self._baseline >= self._config.threshold
