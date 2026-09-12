from src.quantum.pipeline import XiQuantumPipeline


def test_mass_conservation_in_pipeline():
    pipeline = XiQuantumPipeline(lambda_ent=0.1, n_spatial=2)
    history = pipeline.evolve_classical(steps=50)
    final_mass = sum(history[-1]) * pipeline.cfg["dx"]
    assert abs(final_mass - 1.0) < 1e-8


def test_quantum_encoding_unitary_like_shape():
    pipeline = XiQuantumPipeline(n_spatial=2)
    qc = pipeline.encode_snapshot([0.4, 0.6])
    assert qc.num_qubits == 6
    assert qc.depth() > 3
