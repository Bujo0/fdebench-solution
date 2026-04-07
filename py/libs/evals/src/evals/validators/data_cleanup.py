# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup validators for triage responses.

Checks that triage responses properly handle noisy, malformed, or unusually
formatted ticket content without regurgitating the noise or failing to
classify.
"""

import re

from evals.models import EvalScenario
from evals.models import ScenarioTag


class DataCleanupViolation:
    """A data cleanup validation failure."""

    def __init__(self, check: str, message: str) -> None:
        self.check = check
        self.message = message

    def __repr__(self) -> str:
        return f"DataCleanupViolation(check={self.check!r}, message={self.message!r})"


# Pattern indicating base64 data leaked into the response
_BASE64_BLOCK_PATTERN = re.compile(r"[A-Za-z0-9+/]{50,}={0,2}")

# HTML tags that shouldn't appear in triage responses
_HTML_TAG_PATTERN = re.compile(r"<(?:script|style|div|span|html|body|head|p|img|a|table)\b", re.IGNORECASE)

# Log line patterns that shouldn't be regurgitated
_LOG_LINE_PATTERN = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z\s+(?:ERROR|WARN|INFO)\s+\[")

# Email headers that shouldn't leak into responses
_EMAIL_HEADER_PATTERN = re.compile(r"^(?:From|To|Subject|Date|Cc|Bcc):\s+", re.MULTILINE)


def validate_no_base64_leak(response_text: str) -> list[DataCleanupViolation]:
    """Check that base64 encoded data hasn't leaked into the response."""
    violations = []
    if _BASE64_BLOCK_PATTERN.search(response_text):
        violations.append(
            DataCleanupViolation(
                check="base64_leak",
                message="Response contains base64-encoded data that was likely copied from the ticket",
            )
        )
    return violations


def validate_no_html_leak(response_text: str) -> list[DataCleanupViolation]:
    """Check that HTML tags haven't leaked into the response."""
    violations = []
    if _HTML_TAG_PATTERN.search(response_text):
        violations.append(
            DataCleanupViolation(
                check="html_leak",
                message="Response contains HTML tags that were likely copied from an email ticket",
            )
        )
    return violations


def validate_no_log_dump(response_text: str) -> list[DataCleanupViolation]:
    """Check that raw log lines haven't been regurgitated in the response."""
    violations = []
    matches = _LOG_LINE_PATTERN.findall(response_text)
    if len(matches) > 2:
        violations.append(
            DataCleanupViolation(
                check="log_dump",
                message=f"Response contains {len(matches)} raw log lines — likely regurgitated from ticket",
            )
        )
    return violations


def validate_no_email_headers(response_text: str) -> list[DataCleanupViolation]:
    """Check that email forwarding headers haven't leaked into the response."""
    violations = []
    matches = _EMAIL_HEADER_PATTERN.findall(response_text)
    if len(matches) > 1:
        violations.append(
            DataCleanupViolation(
                check="email_header_leak",
                message="Response contains email headers from the ticket's forwarding chain",
            )
        )
    return violations


def validate_response_for_scenario(
    scenario: EvalScenario,
    response: dict[str, object],
) -> list[DataCleanupViolation]:
    """Run all data cleanup checks appropriate for a given scenario.

    Returns an empty list if all checks pass.
    """
    violations: list[DataCleanupViolation] = []

    # Combine all text fields from the response for checking
    text_fields = [
        str(response.get("next_best_action", "")),
    ]
    remediation = response.get("remediation_steps", [])
    if isinstance(remediation, list):
        text_fields.extend(str(step) for step in remediation)

    combined_text = " ".join(text_fields)

    if ScenarioTag.ENCODING in scenario.tags:
        violations.extend(validate_no_base64_leak(combined_text))
        violations.extend(validate_no_html_leak(combined_text))

    if ScenarioTag.NOISE in scenario.tags:
        violations.extend(validate_no_log_dump(combined_text))
        violations.extend(validate_no_email_headers(combined_text))

    return violations
