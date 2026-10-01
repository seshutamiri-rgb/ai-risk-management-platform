
from unittest.mock import patch

import pytest

from langgraph.risk_workflow import build_risk_workflow
from backend.agents.llm_client import LLMConfigurationError


@patch("langgraph.risk_workflow.generate_llm_response")
def test_risk_workflow_success(mock_llm):
    mock_llm.return_value = (
        "The payment gateway integration delay is a critical risk."
    )

    workflow = build_risk_workflow()

    result = workflow.invoke({
        "project_id": "PRJ-001",
        "status": "pending",
        "analysis_data": None,
        "ai_analysis": None,
        "error": None,
    })

    assert result["status"] == "completed"
    assert result["analysis_data"]["project_name"] == "Banking Mobile App"
    assert result["analysis_data"]["total_risks"] == 2
    assert "critical risk" in result["ai_analysis"].lower()
    assert result["error"] is None
    mock_llm.assert_called_once()


@patch("langgraph.risk_workflow.generate_llm_response")
def test_risk_workflow_unknown_project(mock_llm):
    workflow = build_risk_workflow()

    result = workflow.invoke({
        "project_id": "UNKNOWN-PROJECT",
        "status": "pending",
        "analysis_data": None,
        "ai_analysis": None,
        "error": None,
    })

    assert result["status"] == "failed"
    assert result["analysis_data"] is None
    assert result["ai_analysis"] is None
    assert result["error"] == "Project not found."
    mock_llm.assert_not_called()


@patch("langgraph.risk_workflow.generate_llm_response")
def test_risk_workflow_llm_configuration_error(mock_llm):
    mock_llm.side_effect = LLMConfigurationError(
        "LLM API key is not configured."
    )

    workflow = build_risk_workflow()

    with pytest.raises(LLMConfigurationError):
        workflow.invoke({
            "project_id": "PRJ-001",
            "status": "pending",
            "analysis_data": None,
            "ai_analysis": None,
            "error": None,
        })

    mock_llm.assert_called_once()


def test_risk_workflow_passes_mcp_evidence_to_prompt():
    mcp_data = {
        "tool_name": "get_project_risks",
        "content": [
            {
                "found": True,
                "project_id": "PRJ-001",
                "total_risks": 2,
            }
        ],
    }

    with (
        patch(
            "langgraph.risk_workflow.call_mcp_tool",
            return_value=mcp_data,
        ) as mock_mcp,
        patch(
    "langgraph.risk_workflow.call_mcp_tool",
    side_effect=[
        mcp_data,
        {
            "tool_name": "search_project_knowledge",
            "content": [
                {
                    "documents": [
                        {
                            "document_id": "DOC-001",
                            "title": "Project Risk Management Policy",
                            "category": "Policy",
                            "content": "Review critical risks regularly.",
                        }
                    ],
                    "count": 1,
                }
            ],
        },
    ],
) as mock_mcp,
        patch(
            "langgraph.risk_workflow.build_risk_analysis_prompt",
            return_value="Mock risk analysis prompt",
        ) as mock_prompt,
        patch(
            "langgraph.risk_workflow.generate_llm_response",
            return_value="Risk analysis completed.",
        ),
    ):
        workflow = build_risk_workflow()

        result = workflow.invoke({
            "project_id": "PRJ-001",
            "status": "pending",
            "analysis_data": None,
            "ai_analysis": None,
            "error": None,
        })

        assert result["status"] == "completed"

    assert mock_mcp.call_count == 2

    assert mock_mcp.call_args_list[0].args == (
        "get_project_risks",
        {"project_id": "PRJ-001"},
    )

    assert mock_mcp.call_args_list[1].args[0] == (
        "search_project_knowledge"
    )

    assert mock_mcp.call_args_list[1].args[1]["top_k"] == 3

    mock_prompt.assert_called_once()

    assert (
        mock_prompt.call_args.kwargs["mcp_risk_data"]
        == mcp_data
    )