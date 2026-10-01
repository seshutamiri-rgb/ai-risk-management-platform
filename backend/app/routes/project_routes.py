
from fastapi import APIRouter, HTTPException

from backend.services.risk_summary import get_project_risk_summary

router = APIRouter(
    prefix="/projects",
    tags=["Project Management"],
)


@router.get("/{project_id}/risk-summary")
def project_risk_summary(project_id: str):
    summary = get_project_risk_summary(project_id)

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found",
        )

    return summary