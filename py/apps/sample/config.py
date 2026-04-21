"""Application configuration loaded from environment variables."""

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    azure_openai_endpoint: str = ""
    azure_openai_api_key: str = ""
    azure_openai_api_version: str = "2025-01-01-preview"
    triage_model: str = "gpt-5-4-nano"
    extract_model: str = "gpt-5-4"
    orchestrate_model: str = "gpt-5-4"
    triage_strategy: str = "multi-step"
    extract_preprocessor: str = "document-intelligence"
    orchestrate_strategy: str = "react"
    di_endpoint: str = ""
    di_api_key: str = ""
    max_concurrent_requests: int = 10
    llm_timeout_seconds: int = 60

    @field_validator("*", mode="before")
    @classmethod
    def strip_whitespace(cls, v: object) -> object:
        if isinstance(v, str):
            return v.strip()
        return v

    model_config = {"env_file": "../../.env", "env_file_encoding": "utf-8", "extra": "ignore"}
