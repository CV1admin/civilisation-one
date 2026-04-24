from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scripts.run_phase_diagram import run


def test_quick_run_writes_outputs_csv():
    out = run(quick=True)
    assert out == Path("outputs/phase_diagram.csv")
    assert out.exists()
