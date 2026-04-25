from src.vireax import VireaxCenterNode


def test_vireax_center_node_runs_and_writes_output():
    result = VireaxCenterNode().run()
    assert "quantum" in result
    assert "api" in result
    assert result["api"]["status"] == "ok"
    assert result["em_rows"] >= 0
