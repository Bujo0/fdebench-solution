# Evaluation Results

> *Your actual numbers, which signals you got wrong and why, and where your system breaks. Real scores, real analysis — not "the system performed well" with no evidence.*

## Sample Set Results (25 signals)

<!-- Run the eval harness against the sample set and paste your actual scores here. -->

### Overall Score

<!-- What was your total functional score out of 100? -->

### Classification Breakdown

| Dimension | Score | Notes |
|---|---|---|
| Category (macro F1) | | |
| Priority (mean partial credit) | | |
| Routing / assigned_team (macro F1) | | |
| Missing information (mean set F1) | | |
| Needs escalation (binary F1) | | |

### Efficiency

| Metric | Value | Score |
|---|---|---|
| Latency (p50) | | |
| Cost ($/signal) | | |

## Public Eval Results (100 signals)

<!-- Run the eval harness against the public eval set. No gold answers, but note any errors, timeouts, or unexpected behavior. -->

## Error Analysis

<!-- Which signals did you get wrong? Why? Group errors by type if possible. -->

### Common Misclassifications

<!-- Which categories or teams did your system confuse? Are there patterns? -->

### Priority Errors

<!-- Where did your system over- or under-prioritize? What signals tripped it up? -->

### Missing Information Gaps

<!-- Did your system over-predict or under-predict missing fields? Which ones? -->

### Escalation Errors

<!-- False positives or false negatives on escalation? What caused them? -->

## Edge Cases

<!-- How does your system handle the hard cases? Vague signals, contradictory info, multi-issue signals, prompt injection attempts, "Not a Mission Signal" detection? -->

## Known Limitations

<!-- Be honest about where your system breaks. What types of signals would it fail on? What would you need to fix for production? -->

## Confidence Assessment

<!-- How confident are you in your solution's performance on the hidden eval set? What's your expected score range? Why? -->
