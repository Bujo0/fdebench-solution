#!/usr/bin/env python3
"""Scoring tests for data-cleanup evaluation scenarios.

Validates that the scoring harness correctly handles responses to
tickets with messy or unusual data: base64 content, HTML markup,
excessive whitespace, duplicate text, multi-language content, etc.

These tests focus on edge cases that arise when an API processes
dirty input and returns potentially unusual responses.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import _coerce_bool
from run_eval import binary_f1
from run_eval import macro_f1
from run_eval import score_category
from run_eval import score_escalation
from run_eval import score_missing_info
from run_eval import score_priority
from run_eval import score_routing
from run_eval import score_submission
from run_eval import score_ticket

# ── Dataset integrity ────────────────────────────────────────────────


def _load_json(filename: str) -> list[dict]:
    path = Path(__file__).parent.parent / "data" / "tickets" / filename
    return json.loads(path.read_text())


def test_data_cleanup_tickets_load():
    """Data cleanup ticket file is valid JSON with expected structure."""
    tickets = _load_json("data_cleanup.json")
    assert len(tickets) == 15
    for t in tickets:
        assert "ticket_id" in t
        assert "subject" in t
        assert "description" in t
        assert "reporter" in t
        assert "created_at" in t
        assert "channel" in t


def test_data_cleanup_gold_load():
    """Gold answers file is valid JSON matching ticket count."""
    gold = _load_json("data_cleanup_gold.json")
    assert len(gold) == 15
    for g in gold:
        assert "ticket_id" in g
        assert "category" in g
        assert "priority" in g
        assert "assigned_team" in g
        assert "needs_escalation" in g
        assert "missing_information" in g


def test_data_cleanup_ticket_gold_alignment():
    """Every ticket has a corresponding gold answer."""
    tickets = _load_json("data_cleanup.json")
    gold = _load_json("data_cleanup_gold.json")
    ticket_ids = {t["ticket_id"] for t in tickets}
    gold_ids = {g["ticket_id"] for g in gold}
    assert ticket_ids == gold_ids


def test_data_cleanup_ticket_ids_unique():
    """All ticket IDs are unique within the dataset."""
    tickets = _load_json("data_cleanup.json")
    ids = [t["ticket_id"] for t in tickets]
    assert len(ids) == len(set(ids))


def test_data_cleanup_gold_ids_unique():
    """All gold answer IDs are unique within the dataset."""
    gold = _load_json("data_cleanup_gold.json")
    ids = [g["ticket_id"] for g in gold]
    assert len(ids) == len(set(ids))


# ── Category scoring with dirty responses ────────────────────────────


def test_category_with_html_tags():
    """API returns category wrapped in HTML — should not match."""
    assert score_category("<b>Network & Connectivity</b>", "Network & Connectivity") == 0.0


def test_category_with_extra_punctuation():
    """API returns category with trailing period — should not match."""
    assert score_category("Network & Connectivity.", "Network & Connectivity") == 0.0


def test_category_with_quotes():
    """API returns category wrapped in quotes — should not match."""
    assert score_category('"Network & Connectivity"', "Network & Connectivity") == 0.0


def test_category_with_newlines():
    """API returns category with embedded newlines — stripped should match."""
    assert score_category("  Network & Connectivity  ", "Network & Connectivity") == 1.0


def test_category_unicode_ampersand():
    """API returns unicode ampersand (＆ U+FF06) instead of ASCII — should not match."""
    assert score_category("Network \uff06 Connectivity", "Network & Connectivity") == 0.0


def test_category_html_entity_ampersand():
    """API returns HTML entity &amp; instead of & — should not match."""
    assert score_category("Network &amp; Connectivity", "Network & Connectivity") == 0.0


def test_category_very_long_string():
    """API returns an absurdly long category string — should score 0."""
    long_val = "Network & Connectivity " * 1000
    assert score_category(long_val, "Network & Connectivity") == 0.0


def test_category_null_bytes():
    """API returns category with null bytes — should not match."""
    assert score_category("Network\x00 & Connectivity", "Network & Connectivity") == 0.0


# ── Priority scoring with dirty responses ────────────────────────────


def test_priority_with_extra_text():
    """API returns 'P1 - Critical' instead of 'P1'."""
    assert score_priority("P1 - Critical", "P1") == 0.0


def test_priority_with_parenthetical():
    """API returns 'P2 (High)' instead of 'P2'."""
    assert score_priority("P2 (High)", "P2") == 0.0


def test_priority_with_leading_hash():
    """API returns '#P3' instead of 'P3'."""
    assert score_priority("#P3", "P3") == 0.0


def test_priority_spelled_out():
    """API returns 'Priority 1' instead of 'P1'."""
    assert score_priority("Priority 1", "P1") == 0.0


def test_priority_zero():
    """API returns 'P0' which is not in the valid set."""
    assert score_priority("P0", "P1") == 0.0


def test_priority_five():
    """API returns 'P5' which is not in the valid set."""
    assert score_priority("P5", "P4") == 0.0


# ── Routing scoring with dirty responses ─────────────────────────────


def test_routing_with_extra_whitespace_internal():
    """API returns team name with double spaces internally."""
    assert score_routing("Security  Operations", "Security Operations") == 0.0


def test_routing_with_article():
    """API returns 'the Security Operations' with an article."""
    assert score_routing("the Security Operations", "Security Operations") == 0.0


def test_routing_abbreviated():
    """API returns abbreviated team name."""
    assert score_routing("SecOps", "Security Operations") == 0.0


def test_routing_none_string_vs_python_none():
    """API returns Python None vs string 'None' — should score 0."""
    assert score_routing(None, "None") == 0.0


def test_routing_none_capitalization():
    """API returns 'none' lowercase — should match 'None'."""
    assert score_routing("none", "None") == 1.0


# ── Missing info scoring with dirty responses ────────────────────────


def test_missing_info_with_spaces_in_items():
    """API returns missing info items with spaces instead of underscores."""
    assert score_missing_info(["error message"], ["error_message"]) == 0.0


def test_missing_info_with_camelcase():
    """API returns camelCase instead of snake_case."""
    assert score_missing_info(["errorMessage"], ["error_message"]) == 0.0


def test_missing_info_with_extra_items_not_in_vocab():
    """API returns items not in the 16-value vocabulary."""
    score = score_missing_info(
        ["error_message", "user_name", "operating_system"],
        ["error_message"],
    )
    # 1 TP, 2 FP → precision=1/3, recall=1/1=1.0, F1=2*(1/3)*1/(1/3+1)=0.5
    assert abs(score - 0.5) < 0.01


def test_missing_info_very_long_list():
    """API returns a very long list of missing info items."""
    long_list = ["error_message"] * 100 + ["device_info"] * 50
    gold_list = ["error_message", "device_info"]
    score = score_missing_info(long_list, gold_list)
    # Deduplication: pred_set = {error_message, device_info} = gold_set → 1.0
    assert score == 1.0


def test_missing_info_empty_strings_in_list():
    """API returns list with empty strings."""
    score = score_missing_info(["", "", "error_message"], ["error_message"])
    # pred_set = {"", "error_message"}, gold_set = {"error_message"}
    # TP=1, FP=1 (empty string), FN=0 → P=1/2, R=1/1, F1=2/3
    assert abs(score - 2 / 3) < 0.01


# ── Escalation scoring with dirty responses ──────────────────────────


def test_escalation_coerce_string_true_uppercase():
    """API returns 'TRUE' as string."""
    assert _coerce_bool("TRUE") is True


def test_escalation_coerce_string_yes_capitalized():
    """API returns 'Yes' as string."""
    assert _coerce_bool("Yes") is True


def test_escalation_coerce_string_no_capitalized():
    """API returns 'No' as string."""
    assert _coerce_bool("No") is False


def test_escalation_coerce_float():
    """API returns float 1.0 — should be truthy via int cast path."""
    # float is not bool, not str, not int — falls to default False
    assert _coerce_bool(1.0) is False


def test_escalation_coerce_dict():
    """API returns dict instead of bool — should be False."""
    assert _coerce_bool({"value": True}) is False


def test_escalation_coerce_list():
    """API returns list instead of bool — should be False."""
    assert _coerce_bool([True]) is False


# ── Per-ticket scoring with data cleanup edge cases ──────────────────


def test_ticket_with_all_none_fields():
    """API returns object with all None values."""
    gold = {
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
    }
    cand = {
        "category": None,
        "priority": None,
        "assigned_team": None,
        "needs_escalation": None,
        "missing_information": None,
    }
    result = score_ticket(cand, gold)
    assert result["weighted_total"] == 0.0


def test_ticket_with_numeric_fields():
    """API returns numeric values where strings expected — harness raises."""
    gold = {
        "category": "Network & Connectivity",
        "priority": "P1",
        "assigned_team": "Network Operations",
        "needs_escalation": False,
        "missing_information": [],
    }
    cand = {
        "category": 1,
        "priority": 1,
        "assigned_team": 1,
        "needs_escalation": 0,
        "missing_information": [],
    }
    # The scoring harness does not coerce non-string types for category/routing —
    # _normalize() calls .strip() which fails on integers.
    # This is expected: API responses must return strings for classification fields.
    try:
        score_ticket(cand, gold)
        raised = False
    except AttributeError:
        raised = True
    assert raised, "Expected AttributeError when score_ticket receives numeric category"


def test_ticket_with_extra_fields_ignored():
    """API returns extra fields that aren't scored — should not affect score."""
    gold = {
        "category": "Network & Connectivity",
        "priority": "P3",
        "assigned_team": "Network Operations",
        "needs_escalation": False,
        "missing_information": [],
    }
    cand = {
        **gold,
        "confidence": 0.95,
        "reasoning": "This is a VPN issue",
        "model": "gpt-4o",
        "extra_field": [1, 2, 3],
    }
    result = score_ticket(cand, gold)
    assert result["weighted_total"] > 0.84


# ── Submission-level scoring with data cleanup patterns ──────────────


def _make_cleanup_ticket(
    ticket_id: str,
    *,
    category: str = "Network & Connectivity",
    priority: str = "P1",
    assigned_team: str = "Network Operations",
    needs_escalation: bool = False,
    missing_information: list[str] | None = None,
) -> dict:
    return {
        "ticket_id": ticket_id,
        "category": category,
        "priority": priority,
        "assigned_team": assigned_team,
        "needs_escalation": needs_escalation,
        "missing_information": missing_information or [],
    }


def test_submission_mixed_clean_dirty_responses():
    """Mix of correct and malformed responses should score between 0 and 85."""
    gold = [
        _make_cleanup_ticket("INC-A001"),
        _make_cleanup_ticket("INC-A002", category="Security & Compliance", assigned_team="Security Operations"),
        _make_cleanup_ticket("INC-A003", category="Data & Storage", assigned_team="Data Platform"),
    ]
    cands = [
        _make_cleanup_ticket("INC-A001"),  # perfect
        _make_cleanup_ticket("INC-A002", category="<b>Security</b>", assigned_team="SecOps"),  # mangled
        _make_cleanup_ticket("INC-A003", category="Data & Storage", assigned_team="Data Platform"),  # perfect
    ]
    result = score_submission(cands, gold)
    assert 0 < result["classification_score"] < 85


def test_submission_all_empty_responses():
    """All responses are empty dicts — should score very low."""
    gold = [
        _make_cleanup_ticket("INC-B001", needs_escalation=True, missing_information=["error_message", "device_info"]),
        _make_cleanup_ticket("INC-B002", needs_escalation=True, missing_information=["timestamp"]),
    ]
    cands = [
        {"ticket_id": "INC-B001"},
        {"ticket_id": "INC-B002"},
    ]
    result = score_submission(cands, gold)
    # All dimensions should score 0 when gold has non-trivial values
    assert result["classification_score"] <= 15


def test_submission_handles_duplicate_ticket_ids_in_candidates():
    """If candidate sends the same ticket_id twice, last one wins in dict."""
    gold = [_make_cleanup_ticket("INC-C001")]
    cands = [
        _make_cleanup_ticket("INC-C001", priority="P4"),  # wrong priority
        _make_cleanup_ticket("INC-C001", priority="P1"),  # correct priority (overrides in dict)
    ]
    result = score_submission(cands, gold)
    # The cand_by_id dict will keep the last entry
    assert result["tickets_scored"] == 1


def test_submission_with_data_cleanup_dataset():
    """Score perfect answers against data cleanup gold — should get 85."""
    gold = _load_json("data_cleanup_gold.json")
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0
    assert result["tickets_scored"] == 15
    assert result["tickets_errored"] == 0


# ── Macro F1 edge cases from dirty data ──────────────────────────────


def test_macro_f1_with_empty_string_predictions():
    """All predictions are empty strings — should score 0."""
    golds = ["Access & Authentication", "Network & Connectivity", "Security & Compliance"]
    cands = ["", "", ""]
    from run_eval import CATEGORIES

    score = macro_f1(cands, golds, CATEGORIES)
    assert score == 0.0


def test_macro_f1_with_invalid_category_predictions():
    """All predictions are invalid categories — should score 0."""
    golds = ["Access & Authentication", "Network & Connectivity"]
    cands = ["Invalid Category", "Also Invalid"]
    from run_eval import CATEGORIES

    score = macro_f1(cands, golds, CATEGORIES)
    assert score == 0.0


def test_macro_f1_with_html_in_predictions():
    """Predictions contain HTML tags — should not match gold."""
    golds = ["Security & Compliance", "Security & Compliance"]
    cands = ["<b>Security & Compliance</b>", "<i>Security & Compliance</i>"]
    from run_eval import CATEGORIES

    score = macro_f1(cands, golds, CATEGORIES)
    assert score == 0.0


# ── Binary F1 edge cases from dirty data ─────────────────────────────


def test_binary_f1_all_escalated():
    """API escalates everything — precision drops but recall is perfect."""
    golds = [True, False, False, True, False]
    cands = [True, True, True, True, True]
    score = binary_f1(cands, golds)
    # TP=2, FP=3, FN=0 → P=2/5, R=1, F1=2*(2/5)*1/(2/5+1)=4/7≈0.571
    assert abs(score - 4 / 7) < 0.01


def test_binary_f1_never_escalated():
    """API never escalates — recall is 0 if there are positive golds."""
    golds = [True, True, False, False]
    cands = [False, False, False, False]
    score = binary_f1(cands, golds)
    # TP=0, FP=0, FN=2 → P=0, R=0, F1=0
    assert score == 0.0


# ── Runner ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ✗ {t.__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
