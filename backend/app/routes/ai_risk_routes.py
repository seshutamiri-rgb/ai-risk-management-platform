
from fastapi import APIRouter, HTTPException

from backend.agents.llm_client import (
    LLMClientError,
    LLMConfigurationError,
)
from backend.services.ai_risk_analysis import (
    analyze_project_risks,
)

router = APIRouter(
    prefix="/ai",
    tags=["AI Risk Analysis"],
)


@router.get("/projects/{project_id}/risk-analysis")
def get_ai_risk_analysis(project_id: str):
    """Generate an AI explanation of a project's risks."""

    try:
        result = analyze_project_risks(project_id)

    except LLMConfigurationError:
        raise HTTPException(
            status_code=503,
            detail="AI analysis is not configured. "
                   "Please configure the LLM API key.",
        ) from None

    except LLMClientError:
        raise HTTPException(
            status_code=502,
            detail="The AI provider could not complete "
                   "the risk analysis request.",
        ) from None

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Project not found.",
        )

    return result