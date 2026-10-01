
from fastapi.testclient import TestClient

from backend.app.main import app
from backend.app.routes import snowflake_routes

client = TestClient(app)


def test_snowflake_projects_success(monkeypatch):
    monkeypatch.setattr(
        snowflake_routes,
        "fetch_projects",
        lambda: [
            {
                "project_id": "PRJ-001",
                "project_name": "Banking Mobile App",
            },
            {
                "project_id": "PRJ-002",
                "project_name": "Cloud Migration",
            },
        ],
    )

    response = client.get("/snowflake/projects")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "snowflake"
    assert body["total_projects"] == 2


def test_snowflake_risks_success(monkeypatch):
    monkeypatch.setattr(
        snowflake_routes,
        "fetch_risks",
        lambda: [
            {"risk_id": "RSK-001"},
            {"risk_id": "RSK-002"},
            {"risk_id": "RSK-003"},
        ],
    )

    response = client.get("/snowflake/risks")

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "snowflake"
    assert body["total_risks"] == 3


def test_snowflake_risk_summary_success(monkeypatch):
    monkeypatch.setattr(
        snowflake_routes,
        "fetch_project_risk_summary",
        lambda project_id: {
            "project_id": project_id,
            "total_risks": 2,
            "low": 0,
            "medium": 1,
            "high": 0,
            "critical": 1,
        },
    )

    response = client.get(
        "/snowflake/projects/PRJ-001/risk-summary"
    )

    assert response.status_code == 200
    body = response.json()
    assert body["source"] == "snowflake"
    assert body["summary"]["project_id"] == "PRJ-001"
    assert body["summary"]["total_risks"] == 2
    assert body["summary"]["critical"] == 1
    assert body["summary"]["medium"] == 1