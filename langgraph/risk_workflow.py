
from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from backend.agents.llm_client import generate_llm_response
from backend.agents.risk_analysis_prompt import (
    SYSTEM_PROMPT,
    build_risk_analysis_prompt,
)
from backend.services.risk_analysis import (
    prepare_project_risk_analysis,
)

from backend.agents.mcp_client import call_mcp_tool


class RiskAnalysisState(TypedDict):
    project_id: str
    status: str
    analysis_data: dict | None
    rag_context: str | None
    ai_analysis: str | None
    error: str | None
    mcp_risk_data: dict | None
    mcp_knowledge_data: dict | None

def prepare_analysis(state: RiskAnalysisState) -> dict:
    """Load structured risk evidence for a project."""

    analysis_data = prepare_project_risk_analysis(
        state["project_id"]
    )

    if analysis_data is None:
        return {
            "status": "failed",
            "analysis_data": None,
            "ai_analysis": None,
            "error": "Project not found.",
        }

    return {
        "status": "evidence_prepared",
        "analysis_data": analysis_data,
        "ai_analysis": None,
        "error": None,
    }

 


def retrieve_mcp_project_risks(state: RiskAnalysisState) -> dict:
    """Retrieve project risks through the MCP server."""

    project_id = state["project_id"]

    result = call_mcp_tool(
        "get_project_risks",
        {"project_id": project_id},
    )

    return {"mcp_risk_data": result}  


def retrieve_mcp_project_knowledge(
    state: RiskAnalysisState,
) -> dict:
    """Retrieve project policies and lessons through MCP."""

    analysis_data = state["analysis_data"]

    if analysis_data is None:
        return {"mcp_knowledge_data": None}

    query = (
        f"Project risk analysis for {analysis_data['project_name']}. "
        "Find relevant risk mitigation policies, integration delays, "
        "dependencies, and lessons learned."
    )

    result = call_mcp_tool(
        "search_project_knowledge",
        {
            "query": query,
            "top_k": 3,
        },
    )

    return {"mcp_knowledge_data": result}      



def generate_analysis(state: RiskAnalysisState) -> dict:
    """Generate an AI risk analysis using project evidence and MCP knowledge."""

    analysis_data = state["analysis_data"]

    if analysis_data is None:
        return {
            "status": "failed",
            "error": "Risk evidence is unavailable.",
        }

    knowledge_result = state.get("mcp_knowledge_data") or {}
    knowledge_content = knowledge_result.get("content", [])

    documents = []

    for item in knowledge_content:
        if isinstance(item, dict):
            documents.extend(item.get("documents", []))

    if documents:
        rag_context = "\n\n".join(
            f"Document: {doc.get('title', 'Untitled')}\n"
            f"Category: {doc.get('category', 'Unspecified')}\n"
            f"Content: {doc.get('content', '')}"
            for doc in documents
        )
    else:
        rag_context = (
            "No relevant project knowledge documents were retrieved. "
            "Do not invent supporting evidence."
        )

    user_prompt = build_risk_analysis_prompt(
        analysis_data,
        rag_context=rag_context,
        mcp_risk_data=state.get("mcp_risk_data"),
    )

    ai_analysis = generate_llm_response(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    return {
        "status": "completed",
        "ai_analysis": ai_analysis,
        "error": None,
        "requires_human_review": True,
    }



def build_risk_workflow():
    graph = StateGraph(RiskAnalysisState)

    graph.add_node("prepare_analysis", prepare_analysis)
    graph.add_node("retrieve_mcp_project_risks", retrieve_mcp_project_risks)
    graph.add_node("retrieve_mcp_project_knowledge", retrieve_mcp_project_knowledge)
    graph.add_node("generate_analysis", generate_analysis)

    graph.add_edge(START, "prepare_analysis")

    graph.add_conditional_edges(
        "prepare_analysis",
        lambda state: (
            "retrieve_mcp_project_risks"
            if state["analysis_data"] is not None
            else END
        ),
        {
            "retrieve_mcp_project_risks": "retrieve_mcp_project_risks",
            END: END,
        },
    )

    graph.add_edge(
        "retrieve_mcp_project_risks",
        "retrieve_mcp_project_knowledge",
    )
    graph.add_edge(
        "retrieve_mcp_project_knowledge",
        "generate_analysis",
    )
    graph.add_edge("generate_analysis", END)

    return graph.compile()