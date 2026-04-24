from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt


def plot() -> Path:
    input_path = Path("outputs/phase_diagram.csv")
    if not input_path.exists():
        raise FileNotFoundError("Run scripts/run_phase_diagram.py first")

    lambdas = []
    d_eff = []
    with input_path.open() as f:
        reader = csv.DictReader(f)
        for row in reader:
            lambdas.append(float(row["lambda"]))
            d_eff.append(float(row["d_eff"]))

    Path("outputs").mkdir(exist_ok=True)
    out_path = Path("outputs/phase_diagram.png")
    plt.figure(figsize=(6, 4))
    plt.plot(lambdas, d_eff, marker="o")
    plt.xlabel("lambda")
    plt.ylabel("D_eff")
    plt.title("Phase Diagram (Synthetic)")
    plt.tight_layout()
    plt.savefig(out_path, dpi=150)
    print(f"✅ Saved → {out_path}")
    return out_path


if __name__ == "__main__":
    plot()
