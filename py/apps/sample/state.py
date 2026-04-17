"""Global application state populated during lifespan."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import httpx
    from config import Settings
    from openai import AsyncAzureOpenAI

settings: "Settings" = None  # type: ignore[assignment]
aoai_client: "AsyncAzureOpenAI" = None  # type: ignore[assignment]
tool_http_client: "httpx.AsyncClient" = None  # type: ignore[assignment]
ROUTING_GUIDE: str = ""
FEW_SHOT_EXAMPLES: str = ""
