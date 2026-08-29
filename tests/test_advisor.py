import asyncio

import pytest
from pydantic import SecretStr

from secure_starter import advisor as advisor_module
from secure_starter.advisor import AdvisorResponseError, OpenAIAdvisor
from secure_starter.config import Settings


class FakeResponses:
    def __init__(self) -> None:
        self.arguments: dict[str, object] = {}

    async def create(self, **kwargs):
        self.arguments = kwargs
        return type("FakeResponse", (), {"output_text": "  Bounded advice.  "})()


class FakeOpenAIClient:
    def __init__(self) -> None:
        self.responses = FakeResponses()


def test_advisor_requires_a_key() -> None:
    with pytest.raises(ValueError, match="API key"):
        OpenAIAdvisor(Settings(app_env="test", openai_api_key=None))


def test_advisor_uses_responses_api_without_storage(monkeypatch) -> None:
    fake_client = FakeOpenAIClient()
    monkeypatch.setattr(advisor_module, "AsyncOpenAI", lambda **_kwargs: fake_client)
    settings = Settings(
        app_env="test",
        openai_api_key=SecretStr("synthetic-test-value"),
        openai_model="test-model",
    )
    advisor = OpenAIAdvisor(settings)

    result = asyncio.run(
        advisor.advise(
            mode="challenge",
            objective="Choose a smaller beta scope",
            context="Only synthetic context",
        )
    )

    assert result.text == "Bounded advice."
    assert result.model == "test-model"
    assert fake_client.responses.arguments["store"] is False
    assert fake_client.responses.arguments["max_output_tokens"] == 800
    assert fake_client.responses.arguments["reasoning"] == {"effort": "minimal"}
    assert "untrusted_user_input" in str(fake_client.responses.arguments["input"])


def test_advisor_rejects_an_empty_provider_response(monkeypatch) -> None:
    fake_client = FakeOpenAIClient()
    monkeypatch.setattr(advisor_module, "AsyncOpenAI", lambda **_kwargs: fake_client)
    fake_client.responses.create = _empty_response
    advisor = OpenAIAdvisor(
        Settings(app_env="test", openai_api_key=SecretStr("synthetic-test-value"))
    )

    with pytest.raises(AdvisorResponseError, match="no usable text"):
        asyncio.run(advisor.advise(mode="challenge", objective="Synthetic choice", context=""))


async def _empty_response(**_kwargs):
    return type("EmptyResponse", (), {"output_text": ""})()
