
from mcp_servers.risk_mcp_server import (
    get_project_risks,
    search_project_knowledge,
)


def test_get_project_risks_returns_existing_project():
    result = get_project_risks("PRJ-001")

    assert result["found"] is True
    assert result["project_id"] == "PRJ-001"
    assert result["total_risks"] == 2
    assert len(result["risks"]) == 2


def test_get_project_risks_handles_unknown_project():
    result = get_project_risks("PRJ-999")

    assert result["found"] is False
    assert result["message"] == "Project not found."


def test_search_project_knowledge_returns_documents():
    result = search_project_knowledge(
        "integration delays",
        top_k=3,
    )

    assert "documents" in result
    assert "count" in result
    assert result["count"] == len(result["documents"])


def test_search_project_knowledge_rejects_blank_query():
    result = search_project_knowledge("   ")

    assert result["documents"] == []
    assert "required" in result["message"]


def test_search_project_knowledge_rejects_invalid_top_k():
    result = search_project_knowledge(
        "project risks",
        top_k=0,
    )

    assert result["documents"] == []
    assert "top_k" in result["message"]