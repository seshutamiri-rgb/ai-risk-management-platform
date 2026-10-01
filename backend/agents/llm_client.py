
import httpx

from backend.app.config import settings


class LLMConfigurationError(Exception):
    """Raised when the LLM configuration is incomplete."""


class LLMClientError(Exception):
    """Raised when an LLM request fails."""


def generate_llm_response(
    system_prompt: str,
    user_prompt: str,
) -> str:
    """Send prompts to an OpenAI-compatible LLM API."""

    api_key = settings.llm_api_key.get_secret_value().strip()

    if not api_key:
        raise LLMConfigurationError(
            "LLM API key is not configured."
        )

    if not settings.llm_model.strip():
        raise LLMConfigurationError(
            "LLM model is not configured."
        )

    base_url = settings.llm_base_url.rstrip("/")
    url = f"{base_url}/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    payload = {
        "model": settings.llm_model,
        "messages": [
            {
                "role": "system",
                "content": system_prompt,
            },
            {
                "role": "user",
                "content": user_prompt,
            },
        ],
        "temperature": 0.2,
    }

    try:
        response = httpx.post(
            url,
            headers=headers,
            json=payload,
            timeout=30.0,
        )
    except httpx.TimeoutException:
        raise LLMClientError(
            "The LLM request timed out."
        ) from None
    except httpx.RequestError:
        raise LLMClientError(
            "Unable to connect to the LLM provider."
        ) from None

    if response.is_error:
        raise LLMClientError(
            f"The LLM provider returned HTTP {response.status_code}."
        )

    try:
        result = response.json()
        content = result["choices"][0]["message"]["content"]
    except (ValueError, KeyError, IndexError, TypeError):
        raise LLMClientError(
            "The LLM provider returned an unexpected response."
        ) from None

    if not isinstance(content, str) or not content.strip():
        raise LLMClientError(
            "The LLM provider returned an empty response."
        )

    return content.strip()