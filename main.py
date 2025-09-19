"""Entry point demonstrating the MK core thin-line simulation."""
from __future__ import annotations

from mkcore import QuantumConfig, ThinLineCore


def run_demo(steps: int = 5) -> None:
    """Run the thin-line simulation and print a short report."""

    core = ThinLineCore(quantum=QuantumConfig(random_seed=7))
    results = core.run(steps)
    print("MKone Thin-Line Core Demo")
    print("==========================")
    for result in results:
        status = "Pattern" if result.detected_pattern else "Noise"
        print(
            f"Step {result.step:02d} | {status:<7} | Peak ratio: {result.peak_ratio:6.3f}"
        )


if __name__ == "__main__":
    run_demo()
