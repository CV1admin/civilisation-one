from __future__ import annotations

import argparse
import csv
from pathlib import Path


def run(quick: bool = False) -> Path:
    Path("outputs").mkdir(exist_ok=True)
    lambdas = [0.0, 0.3, 0.5, 1.0] if quick else [i / 10 for i in range(0, 11)]

    out_path = Path("outputs/phase_diagram.csv")
    with out_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["lambda", "d_eff"])
        writer.writeheader()
        for lam in lambdas:
            writer.writerow({"lambda": lam, "d_eff": round(2.0 * (1 + lam) ** 2, 6)})

    print(f"✅ Completed → {out_path}")
    return out_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true", help="Run a short sanity sweep")
    args = parser.parse_args()
    run(quick=args.quick)
