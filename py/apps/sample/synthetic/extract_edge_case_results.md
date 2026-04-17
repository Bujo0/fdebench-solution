# Task 2 — Document Extraction Edge Case Results

## Unit Test Results

**Total: 69 passed, 0 failed**

| Section | Passed | Failed | Status |
|---------|--------|--------|--------|
| Boolean Coercion | 18 | 0 | ✅ |
| Null Coercion | 15 | 0 | ✅ |
| Nested Structures | 7 | 0 | ✅ |
| Date Normalization | 10 | 0 | ✅ |
| Date Post-Processing with Schema | 10 | 0 | ✅ |
| JSON Response Parsing | 9 | 0 | ✅ |

## Scorer Sensitivity Analysis

How different response patterns affect the 0–100 resolution score.

```
  Missing field: Correct=100.0  Null=66.7  Omit=66.7  Wrong=66.7
  Number format:  Exact=100.0  String=100.0  Formatted=$0.0  Close int=100.0
  Boolean match:  True=100.0  'true'=0.0  'yes'=0.0  False=0.0
  String match:   Exact=100.0  Partial=56.0  Extra=52.5  Typo=46.7
  List scoring:   Exact=100.0  Reordered=100.0  Missing1=80.0  Extra1=85.7  Empty=0.0
  Nested dict:    Full=100.0  MissingKey=66.7  WrongVal=66.7  Flat string=0.0
  Currency norm:  Exact=100.0  No symbols=70.0  No dollar=70.0
  Bool strings raw=0.0  → after postprocess=100.0
  Null 'N/A' raw=50.0  → after postprocess=100.0
  ✓ Clean JSON, all correct: resolution=100.0
  ✓ Markdown-wrapped, bools as strings: resolution=100.0
  ✓ N/A and null strings normalized: resolution=100.0
  ✓ Date normalization in pipeline: resolution=100.0
```

## Key Insights

1. **Boolean post-processing is critical**: Without coercing `"true"`/`"yes"` → `True`, the scorer gives 0 for boolean fields (string ≠ bool).
2. **Null coercion matters**: LLMs often return `"N/A"` or `"null"` strings; these must become `None` to match gold `null` values.
3. **Date normalization**: The scorer compares strings; normalizing `"November 2, 2025"` → `"2025-11-02"` is essential when gold uses ISO format.
4. **Currency formatting**: The information scorer strips `$`, commas — so `"$1,234.56"` matches `"1234.56"` for information (70%), but not fidelity (30%).
5. **Missing fields score 0**: Omitting a gold field scores (0, 0) — same as returning null when gold is non-null. Always return all schema fields.
6. **List order doesn't matter**: Set-based F1 means reordered lists score perfectly.
7. **Partial string matches still score**: Token F1 gives partial credit (e.g., 2/3 name tokens → ~0.8 info score).
