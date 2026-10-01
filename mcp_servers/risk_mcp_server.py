
from mcp.server.fastmcp import FastMCP

from backend.services.risk_summary import get_project_risk_summary
from rag.retriever import retrieve_relevant_documents


mcp = FastMCP("AI Risk Management Tools")


@mcp.tool()
def get_project_risks(project_id: str) -> dict:
    """Retrieve the existing risk summary for a project."""

    summary = get_project_risk_summary(project_id)

    if summary is None:
        return {
            "found": False,
            "message": "Project not found.",
        }

    return {
        "found": True,
        "project_id": summary["project_id"],
        "project_name": summary["project_name"],
        "total_risks": summary["total_risks"],
        "risk_counts": summary["risk_counts"],
        "risks": summary["risks"],
    }


@mcp.tool()
def search_project_knowledge(query: str, top_k: int = 3) -> dict:
    """Search project governance documents and lessons learned."""

    if not query or not query.strip():
        return {
            "documents": [],
            "message": "A non-empty search query is required.",
        }

    if not 1 <= top_k <= 10:
        return {
            "documents": [],
            "message": "top_k must be between 1 and 10.",
        }

    documents = retrieve_relevant_documents(query, top_k=top_k)

    return {
        "documents": [
            {
                "document_id": document["document_id"],
                "title": document["title"],
                "category": document["category"],
                "content": document["content"],
            }
            for document in documents
        ],
        "count": len(documents),
    }


if __name__ == "__main__":
    mcp.run(transport="stdio")