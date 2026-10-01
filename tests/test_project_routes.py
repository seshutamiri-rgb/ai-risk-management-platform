
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_project_risk_summary_endpoint():
    response = client.get(
        "/projects/PRJ-001/risk-summary"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["total_risks"] == 2
    assert data["risk_counts"]["Critical"] == 1


def test_unknown_project_returns_404():
    response = client.get(
        "/projects/PRJ-999/risk-summary"
    )

    assert response.status_code == 404