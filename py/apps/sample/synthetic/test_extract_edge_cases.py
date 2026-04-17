#!/usr/bin/env python3
"""Edge case tests for Task 2 (Document Extraction) post-processing and scoring."""

import json
import sys
from io import StringIO
from pathlib import Path

# Wire up imports
app_dir = Path(__file__).resolve().parent.parent
py_dir = app_dir.parent.parent.parent  # py/
sys.path.insert(0, str(app_dir))  # noqa: TID251
sys.path.insert(0, str(py_dir))  # noqa: TID251

scorer_root = py_dir / "common" / "libs" / "fdebenchkit" / "src"
sys.path.insert(0, str(scorer_root))  # noqa: TID251

from routers.extract import _postprocess_dates, _postprocess_values, _try_normalize_date  # noqa: E402
from utils import parse_json_response  # noqa: E402
from ms.common.fdebenchkit.scorers.document_extraction import (  # noqa: E402
    score_document,
    score_submission,
    score_value,
)

# ── Collectors ────────────────────────────────────────────────────────

results = StringIO()
total_passed = 0
total_failed = 0
section_results: list[dict] = []


def run_section(name: str, tests: list[tuple], fn):
    """Run a test section, returning (passed, failed, details)."""
    global total_passed, total_failed
    passed = failed = 0
    details: list[str] = []
    for label, test_input, expected in tests:
        result = fn(test_input)
        if result == expected:
            passed += 1
        else:
            failed += 1
            details.append(f"  FAIL [{label}]: input={test_input!r} → got={result!r}  expected={expected!r}")
    total_passed += passed
    total_failed += failed
    section_results.append({"name": name, "passed": passed, "failed": failed, "details": details})
    return passed, failed, details


# ══════════════════════════════════════════════════════════════════════
# SECTION 1: _postprocess_values — Boolean coercion
# ══════════════════════════════════════════════════════════════════════

bool_tests = [
    ("true",           {"checked": "true"},      {"checked": True}),
    ("True",           {"checked": "True"},      {"checked": True}),
    ("yes",            {"checked": "yes"},       {"checked": True}),
    ("Yes",            {"checked": "Yes"},       {"checked": True}),
    ("X mark",         {"checked": "X"},         {"checked": True}),
    ("x lowercase",    {"checked": "x"},         {"checked": True}),
    ("checked word",   {"checked": "checked"},   {"checked": True}),
    ("false",          {"checked": "false"},     {"checked": False}),
    ("False",          {"checked": "False"},     {"checked": False}),
    ("no",             {"checked": "no"},        {"checked": False}),
    ("No",             {"checked": "No"},        {"checked": False}),
    ("unchecked word", {"checked": "unchecked"}, {"checked": False}),
    ("already True",   {"checked": True},        {"checked": True}),
    ("already False",  {"checked": False},       {"checked": False}),
    ("maybe passthru", {"checked": "maybe"},     {"checked": "maybe"}),
    ("1 passthru",     {"checked": "1"},         {"checked": "1"}),
    ("0 passthru",     {"checked": "0"},         {"checked": "0"}),
    ("whitespace yes", {"checked": " yes "},     {"checked": True}),
]

run_section("Boolean Coercion", bool_tests, _postprocess_values)

# ══════════════════════════════════════════════════════════════════════
# SECTION 2: _postprocess_values — Null coercion
# ══════════════════════════════════════════════════════════════════════

null_tests = [
    ("empty string",   {"field": ""},          {"field": None}),
    ("N/A",            {"field": "N/A"},       {"field": None}),
    ("n/a lowercase",  {"field": "n/a"},       {"field": None}),
    ("None string",    {"field": "None"},      {"field": None}),
    ("null string",    {"field": "null"},      {"field": None}),
    ("dash",           {"field": "-"},         {"field": None}),
    ("double dash",    {"field": "--"},        {"field": None}),
    ("na",             {"field": "na"},        {"field": None}),
    ("NA uppercase",   {"field": "NA"},        {"field": None}),
    ("actual value",   {"field": "actual"},    {"field": "actual"}),
    ("zero string",    {"field": "0"},         {"field": "0"}),
    ("already None",   {"field": None},        {"field": None}),
    ("number int",     {"field": 42},          {"field": 42}),
    ("whitespace N/A", {"field": " N/A "},     {"field": None}),
    ("just spaces",    {"field": "   "},       {"field": None}),
]

run_section("Null Coercion", null_tests, _postprocess_values)

# ══════════════════════════════════════════════════════════════════════
# SECTION 3: _postprocess_values — Nested structures
# ══════════════════════════════════════════════════════════════════════

nested_tests = [
    ("nested dict",
     {"outer": {"inner": "true", "val": "N/A"}},
     {"outer": {"inner": True, "val": None}}),
    ("list of dicts",
     {"items": [{"checked": "yes"}, {"checked": "no"}]},
     {"items": [{"checked": True}, {"checked": False}]}),
    ("deeply nested (3 levels)",
     {"a": {"b": {"c": "false", "d": ""}}},
     {"a": {"b": {"c": False, "d": None}}}),
    ("mixed list",
     {"tags": ["true", "hello", "N/A", "false"]},
     {"tags": [True, "hello", None, False]}),
    ("empty dict",
     {},
     {}),
    ("empty list in dict",
     {"items": []},
     {"items": []}),
    ("multi-field flat",
     {"name": "John", "active": "yes", "notes": "N/A", "score": 95},
     {"name": "John", "active": True, "notes": None, "score": 95}),
]

run_section("Nested Structures", nested_tests, _postprocess_values)

# ══════════════════════════════════════════════════════════════════════
# SECTION 4: _try_normalize_date
# ══════════════════════════════════════════════════════════════════════

date_tests = [
    ("already ISO",       "2025-01-15",            "2025-01-15"),
    ("Month DD YYYY",     "November 2, 2025",      "2025-11-02"),
    ("Mon DD YYYY",       "Nov 2, 2025",           "2025-11-02"),
    ("DD Month YYYY",     "2 November 2025",       "2025-11-02"),
    ("no comma variant",  "November 2 2025",       "2025-11-02"),
    ("January 1 2000",    "January 1, 2000",       "2000-01-01"),
    ("non-date string",   "some random text",      "some random text"),
    ("partial date",      "November 2025",         "November 2025"),
    ("empty string",      "",                      ""),
    ("numeric format",    "01/15/2025",            "01/15/2025"),
]

run_section("Date Normalization", date_tests, lambda x: _try_normalize_date(x))

# ══════════════════════════════════════════════════════════════════════
# SECTION 5: _postprocess_dates (with schema context)
# ══════════════════════════════════════════════════════════════════════


def _run_date_postprocess(pair):
    data, schema_str = pair
    return _postprocess_dates(data, schema_str)


date_pp_tests = [
    ("known date field 'date'",
     ({"date": "November 2, 2025"}, json.dumps({"properties": {"date": {"type": "string"}}})),
     {"date": "2025-11-02"}),
    ("known field 'startDate'",
     ({"startDate": "Jan 15, 2025"}, json.dumps({"properties": {"startDate": {"type": "string"}}})),
     {"startDate": "2025-01-15"}),
    ("field ending with Date",
     ({"invoiceDate": "2 November 2025"}, json.dumps({"properties": {"invoiceDate": {"type": "string"}}})),
     {"invoiceDate": "2025-11-02"}),
    ("non-date field untouched",
     ({"name": "November Corp"}, json.dumps({"properties": {"name": {"type": "string"}}})),
     {"name": "November Corp"}),
    ("'as it appears' suppresses normalization",
     ({"date": "November 2, 2025"},
      json.dumps({"properties": {"date": {"type": "string", "description": "Date as it appears on document"}}})),
     {"date": "November 2, 2025"}),
    ("nested date in object",
     ({"period": {"startDate": "Nov 1, 2025", "endDate": "Nov 30, 2025"}},
      json.dumps({"properties": {"period": {"type": "object", "properties": {
          "startDate": {"type": "string"}, "endDate": {"type": "string"}}}}})),
     {"period": {"startDate": "2025-11-01", "endDate": "2025-11-30"}}),
    ("date inside array of objects",
     ({"entries": [{"date": "Jan 1, 2025"}, {"date": "Feb 1, 2025"}]},
      json.dumps({"properties": {"entries": {"type": "array", "items": {"type": "object", "properties": {
          "date": {"type": "string"}}}}}})),
     {"entries": [{"date": "2025-01-01"}, {"date": "2025-02-01"}]}),
    ("empty schema → field-name convention still applies",
     ({"date": "Nov 1, 2025"}, "{}"),
     {"date": "2025-11-01"}),
    ("invalid schema JSON → passthrough",
     ({"date": "Nov 1, 2025"}, "not json"),
     {"date": "Nov 1, 2025"}),
    ("already ISO date unchanged",
     ({"date": "2025-01-15"}, json.dumps({"properties": {"date": {"type": "string"}}})),
     {"date": "2025-01-15"}),
]

run_section("Date Post-Processing with Schema", date_pp_tests, _run_date_postprocess)

# ══════════════════════════════════════════════════════════════════════
# SECTION 6: parse_json_response edge cases
# ══════════════════════════════════════════════════════════════════════

json_parse_tests = [
    ("clean JSON",       '{"a": 1}',                    {"a": 1}),
    ("markdown block",   '```json\n{"a": 1}\n```',      {"a": 1}),
    ("bare markdown",    '```\n{"a": 1}\n```',           {"a": 1}),
    ("trailing text",    '{"a": 1}\nsome extra text',    {"a": 1}),
    ("None input",       None,                           None),
    ("empty string",     "",                             None),
    ("garbage",          "not json at all",              None),
    ("nested markdown",  '```json\n{"nested": {"b": 2}}\n```', {"nested": {"b": 2}}),
    ("whitespace wrap",  '  \n{"a": 1}\n  ',             {"a": 1}),
]

run_section("JSON Response Parsing", json_parse_tests, parse_json_response)

# ══════════════════════════════════════════════════════════════════════
# SECTION 7: Scorer sensitivity analysis
# ══════════════════════════════════════════════════════════════════════

print("\n" + "=" * 72)
print("SCORER SENSITIVITY ANALYSIS")
print("=" * 72)

scorer_findings: list[str] = []

# --- Test: null vs omit vs wrong for a missing field ---
gold = [{"document_id": "T1", "name": "John", "age": 30, "missing_field": "value"}]

pred_null = [{"document_id": "T1", "name": "John", "age": 30, "missing_field": None}]
pred_omit = [{"document_id": "T1", "name": "John", "age": 30}]
pred_wrong = [{"document_id": "T1", "name": "John", "age": 30, "missing_field": "wrong"}]
pred_right = [{"document_id": "T1", "name": "John", "age": 30, "missing_field": "value"}]

s_null = score_submission(pred_null, gold)
s_omit = score_submission(pred_omit, gold)
s_wrong = score_submission(pred_wrong, gold)
s_right = score_submission(pred_right, gold)

line = (
    f"  Missing field: Correct={s_right['resolution']:.1f}  "
    f"Null={s_null['resolution']:.1f}  Omit={s_omit['resolution']:.1f}  "
    f"Wrong={s_wrong['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: number as string vs number vs formatted ---
gold2 = [{"document_id": "T2", "amount": 1234.56}]
pred_num = [{"document_id": "T2", "amount": 1234.56}]
pred_str = [{"document_id": "T2", "amount": "1234.56"}]
pred_fmt = [{"document_id": "T2", "amount": "$1,234.56"}]
pred_int = [{"document_id": "T2", "amount": 1235}]  # close but not exact

s_num = score_submission(pred_num, gold2)
s_str = score_submission(pred_str, gold2)
s_fmt = score_submission(pred_fmt, gold2)
s_int = score_submission(pred_int, gold2)

line = (
    f"  Number format:  Exact={s_num['resolution']:.1f}  "
    f"String={s_str['resolution']:.1f}  Formatted=${s_fmt['resolution']:.1f}  "
    f"Close int={s_int['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: boolean True vs string "true" ---
gold3 = [{"document_id": "T3", "active": True}]
pred_bool = [{"document_id": "T3", "active": True}]
pred_str_true = [{"document_id": "T3", "active": "true"}]
pred_str_yes = [{"document_id": "T3", "active": "yes"}]
pred_false = [{"document_id": "T3", "active": False}]

s_bool = score_submission(pred_bool, gold3)
s_strue = score_submission(pred_str_true, gold3)
s_syes = score_submission(pred_str_yes, gold3)
s_false = score_submission(pred_false, gold3)

line = (
    f"  Boolean match:  True={s_bool['resolution']:.1f}  "
    f"'true'={s_strue['resolution']:.1f}  'yes'={s_syes['resolution']:.1f}  "
    f"False={s_false['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: string similarity (partial match, extra words, typo) ---
gold4 = [{"document_id": "T4", "name": "John Michael Smith"}]
pred_exact = [{"document_id": "T4", "name": "John Michael Smith"}]
pred_partial = [{"document_id": "T4", "name": "John Smith"}]
pred_extra = [{"document_id": "T4", "name": "Mr. John Michael Smith Jr."}]
pred_typo = [{"document_id": "T4", "name": "Jon Michael Smith"}]

s_exact = score_submission(pred_exact, gold4)
s_partial = score_submission(pred_partial, gold4)
s_extra = score_submission(pred_extra, gold4)
s_typo = score_submission(pred_typo, gold4)

line = (
    f"  String match:   Exact={s_exact['resolution']:.1f}  "
    f"Partial={s_partial['resolution']:.1f}  Extra={s_extra['resolution']:.1f}  "
    f"Typo={s_typo['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: list scoring (order, missing, extra) ---
gold5 = [{"document_id": "T5", "tags": ["alpha", "beta", "gamma"]}]
pred_exact5 = [{"document_id": "T5", "tags": ["alpha", "beta", "gamma"]}]
pred_reord = [{"document_id": "T5", "tags": ["gamma", "alpha", "beta"]}]
pred_miss = [{"document_id": "T5", "tags": ["alpha", "beta"]}]
pred_extra5 = [{"document_id": "T5", "tags": ["alpha", "beta", "gamma", "delta"]}]
pred_empty = [{"document_id": "T5", "tags": []}]

s5_exact = score_submission(pred_exact5, gold5)
s5_reord = score_submission(pred_reord, gold5)
s5_miss = score_submission(pred_miss, gold5)
s5_extra = score_submission(pred_extra5, gold5)
s5_empty = score_submission(pred_empty, gold5)

line = (
    f"  List scoring:   Exact={s5_exact['resolution']:.1f}  "
    f"Reordered={s5_reord['resolution']:.1f}  Missing1={s5_miss['resolution']:.1f}  "
    f"Extra1={s5_extra['resolution']:.1f}  Empty={s5_empty['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: nested dict scoring ---
gold6 = [{"document_id": "T6", "address": {"street": "123 Main St", "city": "Springfield", "zip": "62701"}}]
pred_full6 = [{"document_id": "T6", "address": {"street": "123 Main St", "city": "Springfield", "zip": "62701"}}]
pred_partial6 = [{"document_id": "T6", "address": {"street": "123 Main St", "city": "Springfield"}}]
pred_wrong6 = [{"document_id": "T6", "address": {"street": "456 Oak Ave", "city": "Springfield", "zip": "62701"}}]
pred_flat6 = [{"document_id": "T6", "address": "123 Main St, Springfield, 62701"}]

s6_full = score_submission(pred_full6, gold6)
s6_partial = score_submission(pred_partial6, gold6)
s6_wrong = score_submission(pred_wrong6, gold6)
s6_flat = score_submission(pred_flat6, gold6)

line = (
    f"  Nested dict:    Full={s6_full['resolution']:.1f}  "
    f"MissingKey={s6_partial['resolution']:.1f}  WrongVal={s6_wrong['resolution']:.1f}  "
    f"Flat string={s6_flat['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: currency/number normalization in scorer ---
gold7 = [{"document_id": "T7", "total": "$1,234.56"}]
pred_raw = [{"document_id": "T7", "total": "$1,234.56"}]
pred_plain = [{"document_id": "T7", "total": "1234.56"}]
pred_nodollar = [{"document_id": "T7", "total": "1,234.56"}]

s7_raw = score_submission(pred_raw, gold7)
s7_plain = score_submission(pred_plain, gold7)
s7_nodollar = score_submission(pred_nodollar, gold7)

line = (
    f"  Currency norm:  Exact={s7_raw['resolution']:.1f}  "
    f"No symbols={s7_plain['resolution']:.1f}  No dollar={s7_nodollar['resolution']:.1f}"
)
print(line)
scorer_findings.append(line)

# --- Test: post-processing impact on score ---
print("\n── Post-processing impact on scorer ──")

# Simulate: LLM returns "true"/"false" strings for bool gold values
gold_pp = [{"document_id": "PP1", "active": True, "verified": False}]
pred_raw_pp = [{"document_id": "PP1", "active": "true", "verified": "false"}]
pred_processed = [{"document_id": "PP1", "active": True, "verified": False}]

s_pp_raw = score_submission(pred_raw_pp, gold_pp)
s_pp_proc = score_submission(pred_processed, gold_pp)

line = f"  Bool strings raw={s_pp_raw['resolution']:.1f}  → after postprocess={s_pp_proc['resolution']:.1f}"
print(line)
scorer_findings.append(line)

# Simulate: LLM returns "N/A" for null gold values
gold_na = [{"document_id": "PP2", "field1": None, "field2": "real value"}]
pred_na_raw = [{"document_id": "PP2", "field1": "N/A", "field2": "real value"}]
pred_na_proc = [{"document_id": "PP2", "field1": None, "field2": "real value"}]

s_na_raw = score_submission(pred_na_raw, gold_na)
s_na_proc = score_submission(pred_na_proc, gold_na)

line = f"  Null 'N/A' raw={s_na_raw['resolution']:.1f}  → after postprocess={s_na_proc['resolution']:.1f}"
print(line)
scorer_findings.append(line)

# ══════════════════════════════════════════════════════════════════════
# SECTION 8: Combined pipeline test (parse → postprocess → score)
# ══════════════════════════════════════════════════════════════════════

print("\n── Full pipeline simulation (LLM output → parse → postprocess → score) ──")

pipeline_cases = [
    {
        "name": "Clean JSON, all correct",
        "llm_output": '{"document_id": "P1", "name": "Alice", "active": true, "score": 95}',
        "schema": '{"properties": {"name": {"type": "string"}, "active": {"type": "boolean"}, "score": {"type": "integer"}}}',
        "gold": {"document_id": "P1", "name": "Alice", "active": True, "score": 95},
    },
    {
        "name": "Markdown-wrapped, bools as strings",
        "llm_output": '```json\n{"document_id": "P2", "name": "Bob", "active": "yes", "verified": "no"}\n```',
        "schema": '{"properties": {"name": {"type": "string"}, "active": {"type": "boolean"}, "verified": {"type": "boolean"}}}',
        "gold": {"document_id": "P2", "name": "Bob", "active": True, "verified": False},
    },
    {
        "name": "N/A and null strings normalized",
        "llm_output": '{"document_id": "P3", "name": "Carol", "middle_name": "N/A", "suffix": "null"}',
        "schema": '{"properties": {"name": {"type": "string"}, "middle_name": {"type": "string"}, "suffix": {"type": "string"}}}',
        "gold": {"document_id": "P3", "name": "Carol", "middle_name": None, "suffix": None},
    },
    {
        "name": "Date normalization in pipeline",
        "llm_output": '{"document_id": "P4", "startDate": "November 2, 2025", "endDate": "Dec 31, 2025"}',
        "schema": '{"properties": {"startDate": {"type": "string"}, "endDate": {"type": "string"}}}',
        "gold": {"document_id": "P4", "startDate": "2025-11-02", "endDate": "2025-12-31"},
    },
]

for case in pipeline_cases:
    parsed = parse_json_response(case["llm_output"])
    if parsed is None:
        parsed = {}
    processed = _postprocess_dates(parsed, case["schema"])
    processed = _postprocess_values(processed)
    score = score_submission([processed], [case["gold"]])
    status = "✓" if score["resolution"] >= 99.0 else "✗"
    line = f"  {status} {case['name']}: resolution={score['resolution']:.1f}"
    print(line)
    scorer_findings.append(line)

# ══════════════════════════════════════════════════════════════════════
# FINAL SUMMARY
# ══════════════════════════════════════════════════════════════════════

print("\n" + "=" * 72)
print("UNIT TEST SUMMARY")
print("=" * 72)

all_pass = True
for sec in section_results:
    status = "✓" if sec["failed"] == 0 else "✗"
    if sec["failed"] > 0:
        all_pass = False
    print(f"  {status} {sec['name']}: {sec['passed']} passed, {sec['failed']} failed")
    for d in sec["details"]:
        print(d)

print(f"\nTotal: {total_passed} passed, {total_failed} failed")

# ══════════════════════════════════════════════════════════════════════
# Write results to markdown
# ══════════════════════════════════════════════════════════════════════

report_path = Path(__file__).parent / "extract_edge_case_results.md"
with open(report_path, "w") as f:
    f.write("# Task 2 — Document Extraction Edge Case Results\n\n")

    f.write("## Unit Test Results\n\n")
    f.write(f"**Total: {total_passed} passed, {total_failed} failed**\n\n")
    f.write("| Section | Passed | Failed | Status |\n")
    f.write("|---------|--------|--------|--------|\n")
    for sec in section_results:
        status = "✅" if sec["failed"] == 0 else "❌"
        f.write(f"| {sec['name']} | {sec['passed']} | {sec['failed']} | {status} |\n")

    if any(sec["details"] for sec in section_results):
        f.write("\n### Failures\n\n")
        for sec in section_results:
            if sec["details"]:
                f.write(f"**{sec['name']}:**\n```\n")
                for d in sec["details"]:
                    f.write(d + "\n")
                f.write("```\n\n")

    f.write("\n## Scorer Sensitivity Analysis\n\n")
    f.write("How different response patterns affect the 0–100 resolution score.\n\n")
    f.write("```\n")
    for line in scorer_findings:
        f.write(line + "\n")
    f.write("```\n\n")

    f.write("## Key Insights\n\n")
    f.write("1. **Boolean post-processing is critical**: Without coercing `\"true\"`/`\"yes\"` → `True`, ")
    f.write("the scorer gives 0 for boolean fields (string ≠ bool).\n")
    f.write("2. **Null coercion matters**: LLMs often return `\"N/A\"` or `\"null\"` strings; ")
    f.write("these must become `None` to match gold `null` values.\n")
    f.write("3. **Date normalization**: The scorer compares strings; normalizing ")
    f.write("`\"November 2, 2025\"` → `\"2025-11-02\"` is essential when gold uses ISO format.\n")
    f.write("4. **Currency formatting**: The information scorer strips `$`, commas — ")
    f.write("so `\"$1,234.56\"` matches `\"1234.56\"` for information (70%), but not fidelity (30%).\n")
    f.write("5. **Missing fields score 0**: Omitting a gold field scores (0, 0) — same as returning null ")
    f.write("when gold is non-null. Always return all schema fields.\n")
    f.write("6. **List order doesn't matter**: Set-based F1 means reordered lists score perfectly.\n")
    f.write("7. **Partial string matches still score**: Token F1 gives partial credit ")
    f.write("(e.g., 2/3 name tokens → ~0.8 info score).\n")

print(f"\nResults written to {report_path}")

sys.exit(1 if total_failed > 0 else 0)
