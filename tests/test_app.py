from fastapi.testclient import TestClient

from secure_starter.advisor import Advice
from secure_starter.app import create_app
from secure_starter.config import Settings


class FakeAdvisor:
    def __init__(self) -> None:
        self.last_objective = ""
        self.last_context = ""

    async def advise(self, *, mode: str, objective: str, context: str) -> Advice:
        self.last_objective = objective
        self.last_context = context
        return Advice(text=f"Mode: {mode}. Test the riskiest assumption.", model="fake-model")


def test_health_reveals_configuration_state_not_secret() -> None:
    settings = Settings(app_env="test", openai_api_key=None)
    with TestClient(create_app(settings=settings)) as client:
        response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "ai_configured": False, "environment": "test"}
    assert "api_key" not in response.text.lower()


def test_assist_uses_fake_advisor_and_redacts_before_call() -> None:
    fake = FakeAdvisor()
    settings = Settings(app_env="test", openai_api_key=None)
    with TestClient(create_app(settings=settings, advisor=fake)) as client:
        response = client.post(
            "/api/assist",
            json={
                "mode": "pre-mortem",
                "objective": "Review the private beta decision for builder@example.com",
                "context": "token:super-secret-token should never leave this server",
                "confirmed_safe_input": True,
            },
        )

    assert response.status_code == 200
    assert response.json()["requires_human_review"] is True
    assert response.json()["redactions_applied"] == 2
    assert "builder@example.com" not in fake.last_objective
    assert "super-secret-token" not in fake.last_context


def test_assist_requires_explicit_safety_confirmation() -> None:
    fake = FakeAdvisor()
    settings = Settings(app_env="test", openai_api_key=None)
    with TestClient(create_app(settings=settings, advisor=fake)) as client:
        response = client.post(
            "/api/assist",
            json={
                "objective": "Review this bounded product decision",
                "confirmed_safe_input": False,
            },
        )

    assert response.status_code == 422


def test_assist_returns_503_without_advisor() -> None:
    settings = Settings(app_env="test", openai_api_key=None)
    with TestClient(create_app(settings=settings)) as client:
        response = client.post(
            "/api/assist",
            json={
                "objective": "Review this bounded product decision",
                "confirmed_safe_input": True,
            },
        )

    assert response.status_code == 503
    assert "key" in response.json()["detail"].lower()


def test_assist_rejects_combined_input_above_runtime_limit() -> None:
    fake = FakeAdvisor()
    settings = Settings(app_env="test", openai_api_key=None, max_input_chars=500)
    with TestClient(create_app(settings=settings, advisor=fake)) as client:
        response = client.post(
            "/api/assist",
            json={
                "objective": "A" * 490,
                "context": "B" * 20,
                "confirmed_safe_input": True,
            },
        )

    assert response.status_code == 413


def test_settings_report_a_non_empty_secret_as_configured(monkeypatch) -> None:
    monkeypatch.delenv("AI_ENABLED", raising=False)
    settings = Settings(app_env="test", openai_api_key="synthetic-test-value")

    assert settings.ai_configured is True
    assert "testserver" in settings.trusted_hosts


def test_security_headers_are_applied() -> None:
    settings = Settings(app_env="test", openai_api_key=None)
    with TestClient(create_app(settings=settings)) as client:
        response = client.get("/")

    assert response.status_code == 200
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in response.headers["content-security-policy"]
    assert len(response.headers["x-request-id"]) == 32
