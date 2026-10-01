
from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_assess_risk_endpoint():
    response = client.get(
        "/risks/assess",
        params={"probability": 4, "impact": 5},
    )

    assert response.status_code == 200
    assert response.json()["risk_score"] == 20
    assert response.json()["risk_level"] == "Critical"


def test_assess_risk_rejects_invalid_probability():
    response = client.get(
        "/risks/assess",
        params={"probability": 6, "impact": 5},
    )

    assert response.status_code == 422