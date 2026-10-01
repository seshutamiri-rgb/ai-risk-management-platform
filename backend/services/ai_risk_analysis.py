
from backend.agents.llm_client import generate_llm_response
from backend.agents.risk_analysis_prompt import (
    SYSTEM_PROMPT,
    build_risk_analysis_prompt,
)
from backend.services.risk_analysis import (
    prepare_project_risk_analysis,
)
from rag.context_builder import build_rag_context


def analyze_project_risks(project_id: str) -> dict | None:
    """Prepare project risk evidence and generate an AI analysis."""

    analysis_data = prepare_project_risk_analysis(project_id)

    if analysis_data is None:
        return None

    # Step 1: Retrieve relevant project knowledge using RAG
    rag_query = (
        f"Project risk analysis for {analysis_data['project_name']}. "
        "Identify risk mitigation policies, integration delays, "
        "dependencies, and lessons learned."
    )

    rag_context = build_rag_context(rag_query)

    # Step 2: Add the retrieved knowledge to the LLM prompt
    user_prompt = build_risk_analysis_prompt(
        analysis_data,
        rag_context=rag_context,
    )

    # Step 3: Generate the AI risk analysis
    ai_analysis = generate_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    # Step 4: Return the analysis for human review
    return {
        "project_id": analysis_data["project_id"],
        "project_name": analysis_data["project_name"],
        "risk_counts": analysis_data["risk_counts"],
        "total_risks": analysis_data["total_risks"],
        "ai_analysis": ai_analysis,
        "requires_human_review": True,
    }