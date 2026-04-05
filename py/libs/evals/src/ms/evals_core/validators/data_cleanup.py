# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup validation for triage responses.

Verifies that the triage system correctly handles noisy/dirty input data
by producing valid, well-formed outputs regardless of input quality.
"""

import re

from ms.evals_core.constants import Category
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team


def _normalize(value: str) -> str:
    return value.strip().lower()


class DataCleanupIssue:
    """A data cleanup validation finding."""

    def __init__(self, ticket_id: str, check: str, message: str, *, severity: str = "error") -> None:
        self.ticket_id = ticket_id
        self.check = check
        self.message = message
        self.severity = severity

    def __repr__(self) -> str:
        return f"DataCleanupIssue({self.ticket_id}, {self.check}: {self.message})"


def check_output_not_contaminated(ticket_id: str, response: dict[str, object]) -> list[DataCleanupIssue]:
    """Check that noise from the input did not leak into the output fields.

    Detects base64 fragments, HTML tags, excessive whitespace, email headers,
    and other artifacts that should have been cleaned from the input before
    generating the output.
    """
    issues: list[DataCleanupIssue] = []

    text_fields = ["category", "priority", "assigned_team", "next_best_action"]
    list_text_fields = ["remediation_steps", "missing_information"]

    all_text_values: list[tuple[str, str]] = []
    for field in text_fields:
        val = response.get(field)
        if isinstance(val, str):
            all_text_values.append((field, val))

    for field in list_text_fields:
        val = response.get(field)
        if isinstance(val, list):
            for i, item in enumerate(val):
                if isinstance(item, str):
                    all_text_values.append((f"{field}[{i}]", item))

    for field_name, text in all_text_values:
        # Check for HTML tags leaking into output
        if re.search(r"<\s*(html|body|head|div|span|p|br|style|script|table|tr|td)\b", text, re.IGNORECASE):
            issues.append(
                DataCleanupIssue(ticket_id, "html_contamination", f"HTML tags detected in {field_name}: {text[:80]!r}")
            )

        # Check for base64 data leaking into output
        if re.search(r"[A-Za-z0-9+/]{40,}={0,2}", text):
            issues.append(
                DataCleanupIssue(
                    ticket_id, "base64_contamination", f"Base64-like data detected in {field_name}: {text[:80]!r}"
                )
            )

        # Check for email headers leaking into output
        if re.search(r"^(From|To|Subject|Date|Content-Type|MIME-Version|Return-Path):\s", text, re.MULTILINE):
            issues.append(
                DataCleanupIssue(
                    ticket_id, "email_header_contamination", f"Email headers detected in {field_name}: {text[:80]!r}"
                )
            )

        # Check for excessive whitespace (more than 3 consecutive newlines or many tabs)
        if re.search(r"\n{4,}", text) or re.search(r"\t{3,}", text):
            issues.append(
                DataCleanupIssue(
                    ticket_id,
                    "whitespace_contamination",
                    f"Excessive whitespace in {field_name}",
                    severity="warning",
                )
            )

    return issues


def check_classification_despite_noise(
    ticket_id: str,
    response: dict[str, object],
    gold: dict[str, object],
) -> list[DataCleanupIssue]:
    """Check that the system correctly classified a noisy ticket.

    Verifies that despite dirty input, the triage decision matches the gold
    answer for the critical classification fields (category, priority, team).
    """
    issues: list[DataCleanupIssue] = []

    # Check category
    pred_cat = str(response.get("category", ""))
    gold_cat = str(gold.get("category", ""))
    if _normalize(pred_cat) != _normalize(gold_cat):
        issues.append(
            DataCleanupIssue(
                ticket_id,
                "category_mismatch",
                f"Expected {gold_cat!r}, got {pred_cat!r} (noise may have confused classification)",
            )
        )

    # Check priority
    pred_pri = str(response.get("priority", ""))
    gold_pri = str(gold.get("priority", ""))
    if _normalize(pred_pri) != _normalize(gold_pri):
        issues.append(
            DataCleanupIssue(
                ticket_id,
                "priority_mismatch",
                f"Expected {gold_pri!r}, got {pred_pri!r} (noise may have confused priority assignment)",
            )
        )

    # Check routing
    pred_team = str(response.get("assigned_team", ""))
    gold_team = str(gold.get("assigned_team", ""))
    if _normalize(pred_team) != _normalize(gold_team):
        issues.append(
            DataCleanupIssue(
                ticket_id,
                "routing_mismatch",
                f"Expected {gold_team!r}, got {pred_team!r} (noise may have confused routing)",
            )
        )

    return issues


def check_enum_values_clean(ticket_id: str, response: dict[str, object]) -> list[DataCleanupIssue]:
    """Check that enum field values are clean (no extra whitespace, valid casing).

    Ensures the system outputs properly formatted enum values even when
    processing dirty input.
    """
    issues: list[DataCleanupIssue] = []

    valid_categories = {c.value for c in Category}
    valid_priorities = {p.value for p in Priority}
    valid_teams = {t.value for t in Team}

    category = response.get("category")
    if isinstance(category, str) and category != category.strip():
        issues.append(
            DataCleanupIssue(
                ticket_id, "category_whitespace", f"Category has leading/trailing whitespace: {category!r}"
            )
        )
    if isinstance(category, str) and category.strip() not in valid_categories:
        normalized = _normalize(category)
        matching = [c for c in valid_categories if _normalize(c) == normalized]
        if matching:
            issues.append(
                DataCleanupIssue(
                    ticket_id,
                    "category_casing",
                    f"Category has wrong casing: {category!r} (expected {matching[0]!r})",
                    severity="warning",
                )
            )

    priority = response.get("priority")
    if isinstance(priority, str) and priority != priority.strip():
        issues.append(
            DataCleanupIssue(
                ticket_id, "priority_whitespace", f"Priority has leading/trailing whitespace: {priority!r}"
            )
        )
    if isinstance(priority, str) and priority.strip() not in valid_priorities:
        normalized = _normalize(priority)
        matching = [p for p in valid_priorities if _normalize(p) == normalized]
        if matching:
            issues.append(
                DataCleanupIssue(
                    ticket_id,
                    "priority_casing",
                    f"Priority has wrong casing: {priority!r} (expected {matching[0]!r})",
                    severity="warning",
                )
            )

    assigned_team = response.get("assigned_team")
    if isinstance(assigned_team, str) and assigned_team != assigned_team.strip():
        issues.append(
            DataCleanupIssue(
                ticket_id, "team_whitespace", f"Assigned team has leading/trailing whitespace: {assigned_team!r}"
            )
        )
    if isinstance(assigned_team, str) and assigned_team.strip() not in valid_teams:
        normalized = _normalize(assigned_team)
        matching = [t for t in valid_teams if _normalize(t) == normalized]
        if matching:
            issues.append(
                DataCleanupIssue(
                    ticket_id,
                    "team_casing",
                    f"Assigned team has wrong casing: {assigned_team!r} (expected {matching[0]!r})",
                    severity="warning",
                )
            )

    return issues


def validate_data_cleanup_response(
    ticket_id: str,
    response: dict[str, object],
    gold: dict[str, object],
) -> list[DataCleanupIssue]:
    """Run all data cleanup validations on a single triage response.

    Returns a combined list of all issues found.
    """
    issues: list[DataCleanupIssue] = []
    issues.extend(check_output_not_contaminated(ticket_id, response))
    issues.extend(check_classification_despite_noise(ticket_id, response, gold))
    issues.extend(check_enum_values_clean(ticket_id, response))
    return issues
