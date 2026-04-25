from __future__ import annotations

import csv
from pathlib import Path


class PhysicsEquationFramework:
    """Minimal equation index for cross-domain lookup and synthesis."""

    def __init__(self, csv_path: str = "Physics_Equations_Table.csv") -> None:
        self.csv_path = Path(csv_path)

    def load_equations(self, limit: int | None = None) -> list[dict[str, str]]:
        if not self.csv_path.exists():
            return []
        with self.csv_path.open() as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        return rows if limit is None else rows[:limit]

    def synthesize_relation(self, keyword: str) -> dict[str, str]:
        rows = self.load_equations()
        keyword_l = keyword.lower()
        for row in rows:
            joined = " ".join(str(v) for v in row.values()).lower()
            if keyword_l in joined:
                return row
        return {"status": "no_match", "keyword": keyword}
