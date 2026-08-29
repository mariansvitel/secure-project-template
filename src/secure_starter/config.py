from functools import lru_cache
from typing import Literal

from pydantic import Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings loaded from environment variables and `.env.local`."""

    app_name: str = "Secure AI Decision Desk"
    app_env: Literal["development", "test", "production"] = "development"
    openai_api_key: SecretStr | None = None
    openai_model: str = "gpt-5-mini"
    ai_enabled: bool = True
    allowed_hosts: str = "127.0.0.1,localhost,testserver"
    max_input_chars: int = Field(default=4000, ge=500, le=20_000)
    request_timeout_seconds: float = Field(default=30.0, ge=1.0, le=120.0)

    model_config = SettingsConfigDict(
        env_file=".env.local",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @computed_field
    @property
    def ai_configured(self) -> bool:
        if not self.ai_enabled or self.openai_api_key is None:
            return False
        return bool(self.openai_api_key.get_secret_value().strip())

    @property
    def trusted_hosts(self) -> list[str]:
        return [host.strip() for host in self.allowed_hosts.split(",") if host.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
