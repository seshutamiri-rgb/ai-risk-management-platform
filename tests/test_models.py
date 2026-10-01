
from datetime import date

import pytest
from pydantic import ValidationError

from backend.models.project import Project
from backend.models.risk import Risk


def test_project_model():
    project = Project(
        project_id="PRJ-001",
        project_name="Banking Mobile App",
        project_manager="Project Manager A",
        start_date=date(2026, 10, 1),
        planned_end_date=date(2027, 3, 31),
        budget=500000,
    )

    assert project.project_name == "Banking Mobile App"


def test_risk_model():
    risk = Risk(
        risk_id="RSK-001",
        project_id="PRJ-001",
        title="Payment gateway integration delay",
        description="Third-party integration may miss the deadline.",
        probability=4,
        impact=5,
        owner="Technical Lead",
        mitigation_plan="Start integration testing early.",
    )

    assert risk.probability == 4
    assert risk.impact == 5


def test_risk_rejects_invalid_probability():
    with pytest.raises(ValidationError):
        Risk(
            risk_id="RSK-002",
            project_id="PRJ-001",
            title="Invalid probability test",
            description="Testing validation.",
            probability=6,
            impact=3,
            owner="Technical Lead",
            mitigation_plan="Review the risk.",
        )