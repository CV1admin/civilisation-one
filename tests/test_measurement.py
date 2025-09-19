from math import isclose
from random import Random

from mkcore.measurement import counts_to_signal, probabilities, sample_counts
from mkcore.state import uniform_superposition


def test_sample_counts_sums_to_shots():
    state = uniform_superposition(2)
    shots = 100
    counts = sample_counts(state, shots=shots, rng=Random(0))
    assert sum(counts.values()) == shots


def test_counts_to_signal_orders_keys():
    counts = {"11": 3, "00": 1, "01": 2, "10": 4}
    signal = counts_to_signal(counts)
    assert signal == [1.0, 2.0, 4.0, 3.0]


def test_probabilities_are_normalized():
    state = uniform_superposition(3)
    probs = probabilities(state)
    assert isclose(sum(probs), 1.0)
