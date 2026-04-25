from __future__ import annotations

import csv
from pathlib import Path
from typing import Any


class EMSpectrumPipeline:
    """CSV ingestion with optional TensorFlow-backed dataset creation."""

    def __init__(self, csv_path: str = "Electromagnetic_Spectrum.csv") -> None:
        self.csv_path = Path(csv_path)

    def load_rows(self, limit: int | None = None) -> list[dict[str, str]]:
        if not self.csv_path.exists():
            return []
        rows: list[dict[str, str]] = []
        with self.csv_path.open() as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                rows.append(row)
                if limit is not None and i + 1 >= limit:
                    break
        return rows

    def to_tensor_dataset(self, batch_size: int = 16) -> Any:
        """Return tf.data dataset when TensorFlow is available; else return list batches."""
        rows = self.load_rows()
        if not rows:
            return []

        try:
            import tensorflow as tf  # type: ignore
        except Exception:
            batches: list[list[dict[str, str]]] = []
            for i in range(0, len(rows), batch_size):
                batches.append(rows[i : i + batch_size])
            return batches

        tensor_rows = {k: [r.get(k, "") for r in rows] for k in rows[0].keys()}
        ds = tf.data.Dataset.from_tensor_slices(tensor_rows)
        return ds.batch(batch_size)
