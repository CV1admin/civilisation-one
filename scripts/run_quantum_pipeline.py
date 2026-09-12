from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.quantum.pipeline import XiQuantumPipeline


if __name__ == "__main__":
    pipeline = XiQuantumPipeline(lambda_ent=0.15, n_spatial=4)
    spectrum = pipeline.run_full_pipeline(classical_steps=100, shots=2048)

    mean_amp = sum(spectrum) / len(spectrum)
    peak_bin = max(range(len(spectrum)), key=lambda i: spectrum[i])
    print(f"Mean spectrum amplitude: {mean_amp:.6f}")
    print(f"Peak frequency bin: {peak_bin}")
