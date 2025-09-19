from mkcore import DecoderConfig, FeedbackConfig, QuantumConfig, SignalConfig, ThinLineCore


def test_thin_line_core_runs_deterministically():
    core = ThinLineCore(
        quantum=QuantumConfig(n_qubits=3, shots=64, random_seed=42),
        signal=SignalConfig(normalize=True),
        feedback=FeedbackConfig(pattern_rotation=0.1, noise_rotation=0.05, target_qubit=1, perturb_qubit=2),
        decoder=DecoderConfig(threshold=1.0, smoothing=0.5, history=3),
    )
    results = core.run(3)
    assert len(results) == 3
    assert all(result.step == idx for idx, result in enumerate(results))
    assert all(len(result.spectrum) > 0 for result in results)
