from __future__ import annotations

import math


def _z_grid(start: float = 0.0, stop: float = 2.0, n: int = 100) -> list[float]:
    step = (stop - start) / (n - 1)
    return [start + i * step for i in range(n)]


def h_lcdm(z: list[float], omega_m: float = 0.3) -> list[float]:
    omega_x = 1.0 - omega_m
    return [math.sqrt(omega_m * (1.0 + zi) ** 3 + omega_x) for zi in z]


def h_mkone(z: list[float], delta: float, omega_m: float = 0.3) -> list[float]:
    omega_x = 1.0 - omega_m
    values: list[float] = []
    for zi in z:
        denom = 1.0 - delta * math.log1p(zi)
        if denom <= 0:
            raise ValueError("Invalid delta: denominator becomes non-positive")
        num = omega_m * (1.0 + zi) ** 3 + omega_x
        values.append(math.sqrt(num / denom))
    return values


def fitness(delta: float, z: list[float] | None = None) -> float:
    z = _z_grid() if z is None else z
    baseline = h_lcdm(z)
    candidate = h_mkone(z, delta)
    return sum((a - b) ** 2 for a, b in zip(candidate, baseline)) / len(z)


def best_delta(search_min: float = -0.1, search_max: float = 0.1, n: int = 100) -> tuple[float, float]:
    deltas = _z_grid(search_min, search_max, n)
    best_d = deltas[0]
    best_score = fitness(best_d)
    for d in deltas[1:]:
        score = fitness(d)
        if score < best_score:
            best_d, best_score = d, score
    return best_d, best_score
