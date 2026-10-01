
from backend.services.risk_analysis import (
    prepare_project_risk_analysis,
)


def test_prepare_project_risk_analysis():
    result = prepare_project_risk_analysis("PRJ-001")

    assert result is not None
    assert result["project_id"] == "PRJ-001"
    assert result["project_name"] == "Banking Mobile App"
    assert result["total_risks"] == 2

    assert len(result["critical_risks"]) == 1
    assert result["critical_risks"][0]["risk_id"] == "RSK-001"

    assert len(result["high_risks"]) == 0
    assert "not supported" in result["analysis_scope"]


def test_prepare_project_risk_analysis_unknown_project():
    result = prepare_project_risk_analysis("PRJ-999")

    assert result is None


def test_prepare_project_risk_analysis_preserves_risk_counts():
    result = prepare_project_risk_analysis("PRJ-001")

    assert result is not None
    assert result["risk_counts"]["Critical"] == 1
    assert result["risk_counts"]["Medium"] == 1
    assert result["risk_counts"]["High"] == 0
    assert result["risk_counts"]["Low"] == 0