
from backend.services.sample_data import PROJECTS, RISKS
from backend.services.risk_engine import assess_risk


def get_project_risk_summary(project_id: str):
    project = next(
        (p for p in PROJECTS if p.project_id == project_id),
        None,
    )

    if project is None:
        return None

    project_risks = [
        risk for risk in RISKS
        if risk.project_id == project_id
    ]

    assessed_risks = []

    for risk in project_risks:
        assessment = assess_risk(
            risk.probability,
            risk.impact,
        )

        assessed_risks.append({
            "risk_id": risk.risk_id,
            "title": risk.title,
            "owner": risk.owner,
            "status": risk.status.value,
            **assessment,
        })

    levels = ["Low", "Medium", "High", "Critical"]

    risk_counts = {
        level: sum(
            1 for risk in assessed_risks
            if risk["risk_level"] == level
        )
        for level in levels
    }

    assessed_risks.sort(
        key=lambda risk: risk["risk_score"],
        reverse=True,
    )

    return {
        "project_id": project.project_id,
        "project_name": project.project_name,
        "total_risks": len(assessed_risks),
        "risk_counts": risk_counts,
        "risks": assessed_risks,
    }