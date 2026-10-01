
from backend.services.risk_summary import get_project_risk_summary


def prepare_project_risk_analysis(project_id: str) -> dict | None:
    """Prepare structured risk evidence for a future AI analysis."""

    summary = get_project_risk_summary(project_id)

    if summary is None:
        return None

    risks = summary["risks"]

    critical_risks = [
        risk for risk in risks
        if risk["risk_level"] == "Critical"
    ]

    high_risks = [
        risk for risk in risks
        if risk["risk_level"] == "High"
    ]

    return {
        "project_id": summary["project_id"],
        "project_name": summary["project_name"],
        "total_risks": summary["total_risks"],
        "risk_counts": summary["risk_counts"],
        "critical_risks": critical_risks,
        "high_risks": high_risks,
        "analysis_scope": (
            "Evidence-based analysis of existing project risks. "
            "Do not assume causes or project impacts that are not "
            "supported by the supplied data."
        ),
    }