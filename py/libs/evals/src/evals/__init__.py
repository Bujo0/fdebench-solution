# Copyright (c) Microsoft. All rights reserved.
"""Evaluation test scenarios for data cleanup and responsible AI edge cases.

This library provides structured test scenarios with gold-standard answers
for evaluating how an IT support ticket triage system handles:

- **Data cleanup**: Noisy, malformed, or adversarial ticket content such as
  very long emails, base64 images, HTML noise, forwarding chains, etc.
- **Responsible AI**: Prompt injection, jailbreak attempts, social engineering,
  priority manipulation, harmful content requests, etc.

Each scenario includes a synthetic ticket and the expected gold-standard
triage decision, following the same format as the evaluation harness.
"""
