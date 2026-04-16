"""Shared utilities used across modules."""

import json

# Model name mapping: deployment name → display name for X-Model-Name header
_MODEL_DISPLAY_NAMES: dict[str, str] = {
    "gpt-5-4-nano": "gpt-5.4-nano",
    "gpt-5-4": "gpt-5.4",
    "gpt-5-4-mini": "gpt-5.4-mini",
    "gpt-4-1-nano": "gpt-4.1-nano",
    "gpt-4-1-mini": "gpt-4.1-mini",
    "gpt-4-1": "gpt-4.1",
}


def display_model(deployment: str) -> str:
    """Convert a deployment name to its display name."""
    return _MODEL_DISPLAY_NAMES.get(deployment, deployment)


def parse_json_response(text: str | None) -> dict | None:
    """Parse JSON from LLM response, handling markdown code blocks and multi-object responses."""
    if not text:
        return None
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    elif text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        decoder = json.JSONDecoder()
        try:
            result, _ = decoder.raw_decode(text)
            if isinstance(result, dict):
                return result
        except (json.JSONDecodeError, ValueError):
            pass
        return None
