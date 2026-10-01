
from fastapi import APIRouter, HTTPException

from backend.agents.llm_client import (
    LLMClientError,
    LLMConfigurationError,
)
from langgraph.risk_workflow import build_risk_workflow

router = APIRouter(
    prefix="/graph",
    tags=["LangGraph Risk Analysis"],
)


@router.get("/projects/{project_id}/risk-analysis")
def get_graph_risk_analysis(project_id: str):
    """Run the LangGraph project risk analysis workflow."""

    workflow = build_risk_workflow()

    try:
        result = workflow.invoke({
            "project_id": project_id,
            "status": "pending",
            "analysis_data": None,
            "ai_analysis": None,
            "error": None,
            "mcp_risk_data": None,
            "mcp_knowledge_data": None
        })

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

    if result["status"] == "failed":
        raise HTTPException(
            status_code=404,
            detail=result["error"] or "Project not found.",
        )

    return {
        "project_id": result["project_id"],
        "project_name": result["analysis_data"]["project_name"],
        "total_risks": result["analysis_data"]["total_risks"],
        "risk_counts": result["analysis_data"]["risk_counts"],
        "ai_analysis": result["ai_analysis"],
        "requires_human_review": True,
    }