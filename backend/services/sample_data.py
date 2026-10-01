
from backend.models.project import Project
from backend.models.risk import Risk


PROJECTS = [
    Project(
        project_id="PRJ-001",
        project_name="Banking Mobile App",
        project_manager="Project Manager A",
        start_date="2026-10-01",
        planned_end_date="2027-03-31",
        budget=500000,
        status="in_progress",
    ),
    Project(
        project_id="PRJ-002",
        project_name="Cloud Migration",
        project_manager="Project Manager B",
        start_date="2026-09-15",
        planned_end_date="2027-02-28",
        budget=750000,
        status="planning",
    ),
]


RISKS = [
    Risk(
        risk_id="RSK-001",
        project_id="PRJ-001",
        title="Payment gateway integration delay",
        description="Third-party integration may miss the deadline.",
        probability=4,
        impact=5,
        owner="Technical Lead",
        mitigation_plan="Start integration testing early.",
        status="open",
    ),
    Risk(
        risk_id="RSK-002",
        project_id="PRJ-001",
        title="Shortage of testers",
        description="Testing capacity may be insufficient.",
        probability=3,
        impact=3,
        owner="QA Lead",
        mitigation_plan="Arrange additional testing resources.",
        status="in_progress",
    ),
    Risk(
        risk_id="RSK-003",
        project_id="PRJ-002",
        title="Data migration errors",
        description="Legacy data may fail validation.",
        probability=4,
        impact=4,
        owner="Data Migration Lead",
        mitigation_plan="Perform trial migrations and reconciliation.",
        status="open",
    ),
]