
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.agents.llm_client import LLMConfigurationError, LLMClientError

client = TestClient(app)


@patch("backend.app.routes.ai_risk_routes.analyze_project_risks")
def test_ai_risk_analysis_success(mock_analysis):
    mock_analysis.return_value = {
        "project_id": "PRJ-001",
        "project_name": "Banking Mobile App",
        "risk_counts": {
            "Low": 0,
            "Medium": 1,
            "High": 0,
            "Critical": 1,
        },
        "total_risks": 2,
        "ai_analysis": "The critical risk needs management attention.",
        "requires_human_review": True,
    }

    response = client.get(
        "/ai/projects/PRJ-001/risk-analysis"
    )

    assert response.status_code == 200
    assert response.json()["project_id"] == "PRJ-001"
    assert response.json()["total_risks"] == 2
    assert response.json()["requires_human_review"] is True


@patch("backend.app.routes.ai_risk_routes.analyze_project_risks")
def test_ai_risk_analysis_unknown_project(mock_analysis):
    mock_analysis.return_value = None

    response = client.get(
        "/ai/projects/UNKNOWN/risk-analysis"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Project not found."


@patch("backend.app.routes.ai_risk_routes.analyze_project_risks")
def test_ai_risk_analysis_missing_api_key(mock_analysis):
    mock_analysis.side_effect = LLMConfigurationError(
        "LLM API key is not configured."
    )

    response = client.get(
        "/ai/projects/PRJ-001/risk-analysis"
    )

    assert response.status_code == 503


@patch("backend.app.routes.ai_risk_routes.analyze_project_risks")
def test_ai_risk_analysis_provider_error(mock_analysis):
    mock_analysis.side_effect = LLMClientError(
        "Unable to connect to the LLM provider."
    )

    response = client.get(
        "/ai/projects/PRJ-001/risk-analysis"
    )

    assert response.status_code == 502