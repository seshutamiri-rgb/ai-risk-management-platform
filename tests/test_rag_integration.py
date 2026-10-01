
from unittest.mock import patch

from backend.services.ai_risk_analysis import analyze_project_risks


@patch("backend.services.ai_risk_analysis.generate_llm_response")
@patch("backend.services.ai_risk_analysis.build_rag_context")
def test_rag_context_reaches_llm_prompt(
    mock_build_context,
    mock_generate,
):
    mock_build_context.return_value = (
        "PROJECT KNOWLEDGE REFERENCES\n"
        "Document ID: DOC-002\n"
        "Lesson: Confirm external integration dates."
    )

    mock_generate.return_value = (
        "Executive summary: Review the integration dependency."
    )

    result = analyze_project_risks("PRJ-001")

    assert result is not None
    mock_build_context.assert_called_once()

    _, kwargs = mock_generate.call_args
    prompt = kwargs["user_prompt"]

    assert "DOC-002" in prompt
    assert "Confirm external integration dates" in prompt
    assert result["requires_human_review"] is True