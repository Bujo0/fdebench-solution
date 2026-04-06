"""Tests for responsible AI evaluation scenarios."""

from ms.evals_core.scenarios.responsible_ai import get_scenarios


class TestResponsibleAiScenarios:
    """Verify that all responsible AI scenarios are well-formed."""

    def test_returns_scenarios(self) -> None:
        scenarios = get_scenarios()
        assert len(scenarios) > 0, "No responsible AI scenarios returned"

    def test_all_scenario_ids_unique(self) -> None:
        scenarios = get_scenarios()
        ids = [s.scenario_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_all_scenarios_have_required_fields(self) -> None:
        scenarios = get_scenarios()
        for s in scenarios:
            assert s.subject, f"{s.scenario_id}: empty subject"
            assert s.description, f"{s.scenario_id}: empty description"
            assert s.reporter_name, f"{s.scenario_id}: empty reporter_name"
            assert s.reporter_email, f"{s.scenario_id}: empty reporter_email"
            assert s.reporter_department, f"{s.scenario_id}: empty reporter_department"
            assert s.next_best_action, f"{s.scenario_id}: empty next_best_action"
            assert len(s.remediation_steps) > 0, f"{s.scenario_id}: no remediation_steps"

    def test_all_scenarios_have_responsible_ai_tag(self) -> None:
        scenarios = get_scenarios()
        for s in scenarios:
            assert len(s.tags) > 0, f"{s.scenario_id}: no tags"
            assert "responsible-ai" in s.tags, f"{s.scenario_id}: missing 'responsible-ai' tag"

    def test_scenarios_convert_to_scenario_model(self) -> None:
        scenarios = get_scenarios()
        for idx, s in enumerate(scenarios):
            scenario = s.to_scenario(f"INC-RAI-{idx:04d}")
            assert scenario.ticket.ticket_id == f"INC-RAI-{idx:04d}"
            assert scenario.gold.ticket_id == f"INC-RAI-{idx:04d}"
            assert scenario.gold.category is not None
            assert scenario.gold.priority is not None
            assert scenario.gold.assigned_team is not None

    def test_known_scenario_ids(self) -> None:
        """Verify expected scenario IDs exist."""
        scenarios = get_scenarios()
        ids = {s.scenario_id for s in scenarios}
        expected = {f"RAI-{i:03d}" for i in range(1, 331)}
        assert expected.issubset(ids), f"Missing IDs: {expected - ids}"

    def test_minimum_scenario_count(self) -> None:
        """Responsible AI should have at least 330 scenarios."""
        scenarios = get_scenarios()
        assert len(scenarios) >= 330, f"Expected >= 330 RAI scenarios, got {len(scenarios)}"

    def test_covers_key_attack_categories(self) -> None:
        """Verify that key adversarial categories are covered."""
        scenarios = get_scenarios()
        all_tags = set()
        for s in scenarios:
            all_tags.update(s.tags)

        expected_tags = {
            # Core prompt injection / jailbreak (RAI-001..030)
            "prompt-injection",
            "jailbreak",
            "authority-manipulation",
            "social-engineering",
            "credential-harvesting",
            "encoding-obfuscation",
            "multi-language-obfuscation",
            "indirect-injection",
            "data-exfiltration",
            "compliance-bypass",
            "homoglyph-attack",
            "nested-injection",
            "discriminatory-content",
            "flattery-attack",
            # New attack patterns (RAI-031..050)
            "token-smuggling",
            "payload-splitting",
            "instruction-hierarchy",
            "fake-error-injection",
            "gradual-escalation",
            "weaponized-empathy",
            "fake-compliance",
            "markdown-injection",
            "conditional-trigger",
            "gaslighting",
            "reverse-psychology",
            "vendor-impersonation",
            "tool-abuse",
            "bribery",
            "multi-persona",
            "ip-theft",
            "sabotage",
            "social-proof",
            "fake-emergency",
            "chained-request",
            # Advanced adversarial (RAI-051..075)
            "recursive-injection",
            "cross-tenant-request",
            "adversarial-suffix",
            "code-block-injection",
            "hypothetical-abuse",
            "retaliation-attempt",
            "context-manipulation",
            "complexity-attack",
            "deepfake-transcript",
            "mass-credential-reset",
            "model-extraction",
            "prompt-exfiltration",
            "accessibility-pretext",
            "crypto-mining",
            "policy-violation",
            "unauthorized-software",
            "insider-trading",
            "dlp-bypass",
            "data-reclassification",
            "pii-extraction",
            "privacy-pretext",
            "competitive-intelligence",
            "ransomware-threat",
            "extortion",
            "physical-harm",
            "safety-concern",
            "multi-vector",
            "combined-attack",
            "regulatory-pretext",
            "urgency-manipulation",
            "whistleblower-retaliation",
            "unauthorized-surveillance",
            "legal-concern",
            "fake-scanner",
            "supply-chain-timing",
            "persistent-backdoor",
            "firewall-manipulation",
            "hallucination-exploit",
            "false-context",
            "fabricated-policy",
            # New attack patterns (RAI-076..090)
            "timing-pressure",
            "credential-bypass",
            "fake-approval-chain",
            "appeal-to-policy",
            "sql-injection",
            "code-injection",
            "vulnerability-exploit",
            "phishing-creation",
            "social-engineering-tools",
            "stalking-concern",
            "debugging-pretext",
            "ransomware-pretext",
            "destructive-request",
            "fake-incident-response",
            "deepfake-creation",
            "executive-impersonation",
            "bundled-requests",
            "audit-disable",
            "performance-pretext",
            "cultural-authority",
            "intimidation",
            "fake-compliance-deadline",
            "gdpr-pretext",
            "mass-data-export",
            "invisible-injection",
            "zero-width-unicode",
            # New attack patterns (RAI-131..140)
            "unicode-tag-injection",
            "conversation-fabrication",
            "persona-hijack",
            "base64-hidden-payload",
            "fabricated-process",
            "chain-of-thought-coercion",
            "json-response-injection",
            "xss-payload",
            "persistent-manipulation",
            "cjk-obfuscation",
            # New attack patterns (RAI-141..150)
            "reward-hacking",
            "framing-attack",
            "sycophancy",
            "flattery-exploit",
            "system-prompt-extraction",
            "self-referential-loop",
            "adversarial-filename",
            "metadata-injection",
            "context-stuffing",
            "token-exhaustion",
            "code-switch-injection",
            "structured-output-attack",
            "reasoning-manipulation",
            # New attack patterns (RAI-151..160)
            "time-based-injection",
            "fake-system-message",
            "self-referential",
            "emotional-exploitation",
            "disability-claim",
            "fake-training-feedback",
            "model-manipulation",
            "malware-request",
            "disguised-harmful",
            "zero-width-injection",
            "unicode-steganography",
            "consensus-manipulation",
            "consent-manipulation",
            "fake-terms",
            "context-poisoning",
            "fake-history",
            "progressive-escalation",
            "multi-stage",
            # New attack patterns (RAI-191..200)
            "dan-jailbreak",
            "fake-pentest",
            "emotional-manipulation",
            "authority-spoofing",
            "base64-injection",
            # New attack patterns (RAI-291..305)
            "constitutional-ai-bypass",
            "transparency-exploitation",
            "steganographic-acrostic",
            "hidden-instruction",
            "token-boundary-exploit",
            "fake-audit-context",
            "memory-manipulation",
            "false-prior-agreement",
            "adversarial-few-shot",
            "classification-override",
            "output-formatting-exploit",
            "html-injection",
            "meta-reasoning-attack",
            "content-filter-bypass",
            "sandboxing-escape",
            "destructive-command",
            "accessibility-exploitation",
            "credential-extraction",
            "cross-session-reference",
            "fabricated-ticket",
            "prompt-chaining",
            "false-paper-trail",
            "time-delayed-payload",
            "automated-reclassification",
            "helpful-correction-exploit",
            "policy-override",
            "social-proof-aggregation",
            "peer-pressure-exploit",
            # New tags from RAI-316..RAI-330
            "acrostic-instruction",
            "steganographic-attack",
            "phishing-content-request",
            "harmful-content",
            "fake-audit-bypass",
            "dlp-circumvention",
            "regulatory-coercion",
            "fake-regulation",
            "few-shot-attack",
            "example-injection",
            "pii-harvesting",
            "hr-impersonation",
            "monitoring-disable",
            "audit-tampering",
            "token-flooding",
            "multi-vector-attack",
            "combined-adversarial",
            "prompt-extraction-attempt",
            "system-prompt-leak",
            "rot13-injection",
            "encoding-evasion",
            "ransomware-disguise",
            "recovery-pretext",
            "translation-injection",
            "multilingual-evasion",
            "self-modification-request",
            "rule-change-injection",
        }
        assert expected_tags.issubset(all_tags), f"Missing attack tags: {expected_tags - all_tags}"
