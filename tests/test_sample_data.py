
from backend.services.sample_data import PROJECTS, RISKS


def test_sample_projects_exist():
    assert len(PROJECTS) == 2


def test_sample_risks_exist():
    assert len(RISKS) == 3


def test_every_risk_has_a_valid_project():
    project_ids = {project.project_id for project in PROJECTS}

    for risk in RISKS:
        assert risk.project_id in project_ids