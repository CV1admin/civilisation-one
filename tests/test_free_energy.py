def free_energy(x):
    return float(sum(v * v for v in x))


def gradient_step(x, dt=0.1):
    return [v - dt * 2 * v for v in x]


def test_free_energy_monotonicity():
    x = [1.0, -0.5, 0.25, -0.125]
    e0 = free_energy(x)
    x1 = gradient_step(x)
    e1 = free_energy(x1)
    assert e1 <= e0 + 1e-12


if __name__ == "__main__":
    test_free_energy_monotonicity()
    print("free energy monotonicity: PASS")
