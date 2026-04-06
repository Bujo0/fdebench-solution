# Copyright (c) Microsoft. All rights reserved.
"""Tests for the EvalDatasetGenerator."""

import random
import tempfile
from pathlib import Path

from ms.eval_generator.generator import EvalDatasetGenerator
from ms.eval_generator.generator import _generate_reporter
from ms.eval_generator.generator import _generate_timestamp
from ms.eval_generator.generator import _pick_attachments
from ms.eval_generator.generator import _pick_channel
from ms.eval_generator.models import VALID_CHANNELS


class TestGenerateTimestamp:
    def test_returns_iso8601_format(self) -> None:
        rng = random.Random(42)
        ts = _generate_timestamp(rng)
        assert ts.startswith("2026-03-")
        assert ts.endswith("Z")

    def test_business_hours_in_range(self) -> None:
        rng = random.Random(42)
        for _ in range(50):
            ts = _generate_timestamp(rng, after_hours=False)
            hour = int(ts.split("T")[1].split(":")[0])
            assert 7 <= hour < 20

    def test_after_hours_in_range(self) -> None:
        rng = random.Random(42)
        for _ in range(50):
            ts = _generate_timestamp(rng, after_hours=True)
            hour = int(ts.split("T")[1].split(":")[0])
            assert hour < 7 or hour >= 20


class TestGenerateReporter:
    def test_returns_valid_reporter(self) -> None:
        rng = random.Random(42)
        reporter = _generate_reporter(rng, ())
        assert reporter.name
        assert reporter.email.endswith("@contoso.com")
        assert reporter.department

    def test_respects_department_constraint(self) -> None:
        rng = random.Random(42)
        departments = ("Engineering", "Trading")
        for _ in range(20):
            reporter = _generate_reporter(rng, departments)
            assert reporter.department in departments


class TestPickChannel:
    def test_returns_valid_channel(self) -> None:
        rng = random.Random(42)
        for _ in range(50):
            channel = _pick_channel(rng, ())
            assert channel in VALID_CHANNELS

    def test_respects_channel_constraint(self) -> None:
        rng = random.Random(42)
        channels = ("email", "chat")
        for _ in range(20):
            channel = _pick_channel(rng, channels)
            assert channel in channels


class TestPickAttachments:
    def test_returns_list(self) -> None:
        rng = random.Random(42)
        attachments = _pick_attachments(rng, ())
        assert isinstance(attachments, list)

    def test_respects_attachment_set_constraint(self) -> None:
        rng = random.Random(42)
        attachment_sets = (("screenshot.png",), ("debug.log",))
        for _ in range(20):
            attachments = _pick_attachments(rng, attachment_sets)
            assert attachments in [["screenshot.png"], ["debug.log"]]


class TestEvalDatasetGenerator:
    def test_generate_produces_matching_counts(self) -> None:
        gen = EvalDatasetGenerator(seed=42)
        tickets, golds = gen.generate()
        assert len(tickets) == len(golds)
        assert len(tickets) > 0

    def test_generate_is_reproducible(self) -> None:
        t1, g1 = EvalDatasetGenerator(seed=42).generate()
        t2, g2 = EvalDatasetGenerator(seed=42).generate()
        assert [t.ticket_id for t in t1] == [t.ticket_id for t in t2]
        assert [g.category for g in g1] == [g.category for g in g2]

    def test_different_seeds_produce_different_order(self) -> None:
        t1, _ = EvalDatasetGenerator(seed=42).generate()
        t2, _ = EvalDatasetGenerator(seed=99).generate()
        ids1 = [t.ticket_id for t in t1]
        ids2 = [t.ticket_id for t in t2]
        # Same set of IDs but different order due to shuffle
        assert set(ids1) == set(ids2)
        assert ids1 != ids2

    def test_ticket_ids_are_unique(self) -> None:
        gen = EvalDatasetGenerator(seed=42)
        tickets, _ = gen.generate()
        ids = [t.ticket_id for t in tickets]
        assert len(ids) == len(set(ids)), "Duplicate ticket IDs found"

    def test_ticket_ids_match_gold_ids(self) -> None:
        gen = EvalDatasetGenerator(seed=42)
        tickets, golds = gen.generate()
        ticket_ids = {t.ticket_id for t in tickets}
        gold_ids = {g.ticket_id for g in golds}
        assert ticket_ids == gold_ids

    def test_max_variants_limits_expansion(self) -> None:
        gen_small = EvalDatasetGenerator(seed=42, max_variants_per_scenario=1)
        gen_large = EvalDatasetGenerator(seed=42, max_variants_per_scenario=6)
        t_small, _ = gen_small.generate()
        t_large, _ = gen_large.generate()
        assert len(t_small) <= len(t_large)

    def test_write_dataset_creates_files(self) -> None:
        gen = EvalDatasetGenerator(seed=42, max_variants_per_scenario=1)
        with tempfile.TemporaryDirectory() as tmpdir:
            tickets_path, golds_path = gen.write_dataset(Path(tmpdir))
            assert tickets_path.exists()
            assert golds_path.exists()
            assert tickets_path.name == "eval_dataset.json"
            assert golds_path.name == "eval_dataset_gold.json"
