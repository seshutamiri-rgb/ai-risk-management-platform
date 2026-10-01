
from unittest.mock import patch

from fastapi.testclient import TestClient

from backend.app.main import app
from backend.agents.llm_client import (
    LLMClientError,
    LLMConfigurationError,
)

client = TestClient(app)


@patch("backend.app.routes.graph_routes.build_risk_workflow")
def test_graph_risk_analysis_success(mock_build):
    mock_build.return_value.invoke.return_value = {
        "project_id": "PRJ-001",
        "status": "completed",
        "analysis_data": {
            "project_id": "PRJ-001",
            "project_name": "Banking Mobile App",
            "total_risks": 2,
            "risk_counts": {
                "Low": 0,
                "Medium": 1,
                "High": 0,
                "Critical": 1,
            },
        },
        "ai_analysis": "The critical risk needs attention.",
        "error": None,
    }

    response = client.get(
        "/graph/projects/PRJ-001/risk-analysis"
    )

    assert response.status_code == 200
    assert response.json()["project_name"] == "Banking Mobile App"
    assert response.json()["total_risks"] == 2
    assert response.json()["requires_human_review"] is True


@patch("backend.app.routes.graph_routes.build_risk_workflow")
def test_graph_risk_analysis_unknown_project(mock_build):
    mock_build.return_value.invoke.return_value = {
        "project_id": "UNKNOWN",
        "status": "failed",
        "analysis_data": None,
        "ai_analysis": None,
        "error": "Project not found.",
    }

    response = client.get(
        "/graph/projects/UNKNOWN/risk-analysis"
    )

    assert response.status_code == 404


@patch("backend.app.routes.graph_routes.build_risk_workflow")
def test_graph_risk_analysis_missing_api_key(mock_build):
    mock_build.return_value.invoke.side_effect = (
        LLMConfigurationError("LLM API key is not configured.")
    )

    response = client.get(
        "/graph/projects/PRJ-001/risk-analysis"
    )

    assert response.status_code == 503


@patch("backend.app.routes.graph_routes.build_risk_workflow")
def test_graph_risk_analysis_provider_error(mock_build):
    mock_build.return_value.invoke.side_effect = (
        LLMClientError("Unable to connect to the LLM provider.")
    )

    response = client.get(
        "/graph/projects/PRJ-001/risk-analysis"
    )

    assert response.status_code == 502