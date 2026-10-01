
import pytest
from pydantic import SecretStr

from backend.app.config import settings
from backend.agents.llm_client import (
    LLMConfigurationError,
    generate_llm_response,
)


def test_missing_api_key_prevents_llm_request(monkeypatch):
    monkeypatch.setattr(
        settings,
        "llm_api_key",
        SecretStr(""),
    )

    def unexpected_request(*args, **kwargs):
        pytest.fail("An HTTP request must not be made without an API key.")

    monkeypatch.setattr(
        "backend.agents.llm_client.httpx.post",
        unexpected_request,
    )

    with pytest.raises(
        LLMConfigurationError,
        match="LLM API key is not configured",
    ):
        generate_llm_response(
            system_prompt="Test system prompt",
            user_prompt="Test user prompt",
        )

    
from unittest.mock import Mock

from backend.agents.llm_client import LLMClientError


def test_successful_llm_response(monkeypatch):
    monkeypatch.setattr(
        settings,
        "llm_api_key",
        SecretStr("test-key"),
    )

    mock_response = Mock()
    mock_response.is_error = False
    mock_response.json.return_value = {
        "choices": [
            {
                "message": {
                    "content": "The critical risk needs attention."
                }
            }
        ]
    }

    def fake_post(url, headers, json, timeout):
        assert url.endswith("/chat/completions")
        assert headers["Authorization"] == "Bearer test-key"
        assert json["model"] == settings.llm_model
        return mock_response

    monkeypatch.setattr(
        "backend.agents.llm_client.httpx.post",
        fake_post,
    )

    result = generate_llm_response(
        system_prompt="You are a risk analyst.",
        user_prompt="Analyze project risks.",
    )

    assert result == "The critical risk needs attention."


def test_llm_provider_http_error(monkeypatch):
    monkeypatch.setattr(
        settings,
        "llm_api_key",
        SecretStr("test-key"),
    )

    mock_response = Mock()
    mock_response.is_error = True
    mock_response.status_code = 401

    monkeypatch.setattr(
        "backend.agents.llm_client.httpx.post",
        lambda *args, **kwargs: mock_response,
    )

    with pytest.raises(LLMClientError, match="HTTP 401"):
        generate_llm_response(
            system_prompt="System",
            user_prompt="User",
        )


def test_unexpected_llm_response(monkeypatch):
    monkeypatch.setattr(
        settings,
        "llm_api_key",
        SecretStr("test-key"),
    )

    mock_response = Mock()
    mock_response.is_error = False
    mock_response.json.return_value = {}

    monkeypatch.setattr(
        "backend.agents.llm_client.httpx.post",
        lambda *args, **kwargs: mock_response,
    )

    with pytest.raises(
        LLMClientError,
        match="unexpected response",
    ):
        generate_llm_response(
            system_prompt="System",
            user_prompt="User",
        )    