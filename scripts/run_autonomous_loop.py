from __future__ import annotations

import json
import sys
from dataclasses import asdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.automation import run_agent_loop


if __name__ == "__main__":
    Path("outputs").mkdir(exist_ok=True)
    results = run_agent_loop(iterations=5)
    payload = [asdict(r) for r in results]
    out = Path("outputs/mkone_autofit.json")
    out.write_text(json.dumps(payload, indent=2))
    print(f"✅ Saved → {out}")
