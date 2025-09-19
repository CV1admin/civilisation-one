from math import isclose

import pytest

from mkcore.state import normalize, uniform_superposition


def test_uniform_superposition_is_normalized():
    state = uniform_superposition(3)
    norm_sq = sum(abs(amplitude) ** 2 for amplitude in state)
    assert isclose(norm_sq, 1.0)


def test_normalize_rejects_zero_vector():
    with pytest.raises(ValueError):
        normalize([0j, 0j, 0j, 0j])
