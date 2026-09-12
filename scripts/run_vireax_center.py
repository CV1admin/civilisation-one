from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.vireax import VireaxCenterNode


if __name__ == "__main__":
    result = VireaxCenterNode().run()
    print("✅ Vireax center node run complete")
    print(f"Quantum backend: {result['quantum']['backend']}")
    print(f"EM rows processed: {result['em_rows']}")
