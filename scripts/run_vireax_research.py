from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.vireax.research_engine import VireaxResearchEngine


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="simulation", choices=["simulation", "synthesis", "discovery", "optimization"])
    parser.add_argument("--iterations", type=int, default=2)
    args = parser.parse_args()

    engine = VireaxResearchEngine(mode=args.mode)
    results = engine.run(iterations=args.iterations)
    print("✅ Vireax research loop complete")
    print(f"Mode: {args.mode}")
    print(f"Iterations: {len(results)}")
