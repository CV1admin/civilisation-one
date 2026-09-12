from src.vireax.research_engine import VireaxResearchEngine


def test_research_engine_generates_iterations_and_log():
    engine = VireaxResearchEngine(mode="simulation")
    results = engine.run(iterations=3)
    assert len(results) == 3
    assert all(r.mode == "simulation" for r in results)
    assert all("Q/D/E/I" in r.conceptual_insight for r in results)
