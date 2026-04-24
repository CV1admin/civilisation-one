from src.automation import run_agent_loop
from src.extensions.cosmology_solver import best_delta, fitness, h_lcdm, h_mkone


def test_h_mkone_matches_lcdm_at_zero_delta():
    z = [i / 25 for i in range(51)]
    a = h_mkone(z, 0.0)
    b = h_lcdm(z)
    assert all(abs(x - y) < 1e-12 for x, y in zip(a, b))


def test_best_delta_close_to_zero_for_lcdm_target():
    delta, err = best_delta()
    assert abs(delta) < 0.01
    assert err <= fitness(0.05)


def test_agent_loop_returns_fixed_iteration_count():
    results = run_agent_loop(iterations=4)
    assert len(results) == 4
    assert all(r.error >= 0.0 for r in results)
