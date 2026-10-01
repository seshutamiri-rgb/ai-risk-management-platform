
from unittest.mock import patch

from backend.services.ai_risk_analysis import analyze_project_risks


@patch("backend.services.ai_risk_analysis.generate_llm_response")
def test_analyze_project_risks_success(mock_llm):
    mock_llm.return_value = (
        "The payment gateway integration delay requires "
        "immediate management attention."
    )

    result = analyze_project_risks("PRJ-001")

    assert result is not None
    assert result["project_id"] == "PRJ-001"
    assert result["project_name"] == "Banking Mobile App"
    assert result["total_risks"] == 2
    assert result["risk_counts"]["Critical"] == 1
    assert "payment gateway" in result["ai_analysis"].lower()
    assert result["requires_human_review"] is True
    mock_llm.assert_called_once()


@patch("backend.services.ai_risk_analysis.generate_llm_response")
def test_unknown_project_does_not_call_llm(mock_llm):
    result = analyze_project_risks("UNKNOWN-PROJECT")

    assert result is None
    mock_llm.assert_not_called()


@patch("backend.services.ai_risk_analysis.generate_llm_response")
def test_llm_error_is_propagated(mock_llm):
    mock_llm.side_effect = RuntimeError("Simulated LLM failure")

    try:
        analyze_project_risks("PRJ-001")
        assert False, "Expected the LLM error to be propagated"
    except RuntimeError as exc:
        assert str(exc) == "Simulated LLM failure"