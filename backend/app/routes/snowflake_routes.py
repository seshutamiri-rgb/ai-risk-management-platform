
from fastapi import APIRouter, HTTPException

from backend.services.snowflake_service import (
    fetch_projects,
    fetch_risks,
    fetch_project_risk_summary,
)

router = APIRouter(
    prefix="/snowflake",
    tags=["Snowflake Integration"],
)


@router.get("/projects")
def get_snowflake_projects():
    """Retrieve project records from Snowflake."""
    try:
        projects = fetch_projects()
        return {
            "source": "snowflake",
            "total_projects": len(projects),
            "projects": projects,
        }
    except Exception:
        # Do not expose database errors or credentials.
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve project data from Snowflake.",
        )


@router.get("/risks")
def get_snowflake_risks():
    """Retrieve risk records from Snowflake."""
    try:
        risks = fetch_risks()
        return {
            "source": "snowflake",
            "total_risks": len(risks),
            "risks": risks,
        }
    except Exception:
        # Do not expose database errors or credentials.
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve risk data from Snowflake.",
        )

    
@router.get("/projects/{project_id}/risk-summary")
def get_snowflake_project_risk_summary(project_id: str):
    """Retrieve a project's risk summary from Snowflake."""
    try:
        summary = fetch_project_risk_summary(project_id)

        return {
            "source": "snowflake",
            "summary": summary,
        }

    except Exception:
        # Do not expose database errors or credentials.
        raise HTTPException(
            status_code=503,
            detail="Unable to retrieve project risk summary from Snowflake.",
        )    