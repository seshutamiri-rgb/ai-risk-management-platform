
from backend.services.risk_summary import get_project_risk_summary


def test_project_risk_summary():
    summary = get_project_risk_summary("PRJ-001")

    assert summary is not None
    assert summary["total_risks"] == 2
    assert summary["risk_counts"]["Critical"] == 1
    assert summary["risk_counts"]["Medium"] == 1


def test_risks_are_sorted_by_score():
    summary = get_project_risk_summary("PRJ-001")

    scores = [
        risk["risk_score"]
        for risk in summary["risks"]
    ]

    assert scores == sorted(scores, reverse=True)


def test_unknown_project_returns_none():
    assert get_project_risk_summary("PRJ-999") is None