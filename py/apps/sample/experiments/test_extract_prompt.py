#!/usr/bin/env python3
"""Focused Task 2 extraction experiment runner.

Sends extract requests to the running server, scores the responses,
and reports per-document and aggregate metrics.

Usage:
    python test_extract_prompt.py --endpoint http://localhost:8030 [--limit 10]
"""

import argparse
import asyncio
import json
import sys
import time
from pathlib import Path

import httpx

_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "py" / "common" / "libs" / "fdebenchkit" / "src"))

from ms.common.fdebenchkit.scorers.document_extraction import score_submission

_DATA_DIR = _REPO_ROOT / "py" / "data" / "task2"
_INPUT_PATH = _DATA_DIR / "public_eval_50.json"
_GOLD_PATH = _DATA_DIR / "public_eval_50_gold.json"


async def run_extract(endpoint: str, items: list[dict], concurrency: int = 5, timeout: float = 60.0) -> list[dict]:
    """Send extract requests concurrently and collect responses."""
    sem = asyncio.Semaphore(concurrency)
    responses: list[dict] = []

    async def _call(client: httpx.AsyncClient, item: dict) -> dict:
        async with sem:
            doc_id = item["document_id"]
            try:
                t0 = time.monotonic()
                resp = await client.post(
                    f"{endpoint}/extract",
                    json=item,
                    timeout=timeout,
                )
                elapsed = time.monotonic() - t0
                data = resp.json()
                print(f"  {doc_id}: {resp.status_code} ({elapsed:.1f}s)")
                return data
            except Exception as e:
                print(f"  {doc_id}: ERROR {e}")
                return {"document_id": doc_id}

    async with httpx.AsyncClient() as client:
        tasks = [_call(client, item) for item in items]
        responses = await asyncio.gather(*tasks)

    return list(responses)


def print_results(results: dict, label: str = "Experiment") -> None:
    """Pretty-print scoring results."""
    print()
    print("=" * 80)
    print(f"  {label}")
    print("=" * 80)
    print(f"  Resolution:            {results['resolution']:6.1f} / 100")
    dims = results["dimension_scores"]
    print(f"  Information Accuracy:  {dims['information_accuracy']:.4f}")
    print(f"  Text Fidelity:         {dims['text_fidelity']:.4f}")
    print(f"  Documents scored:      {results['documents_scored']}")
    print(f"  Documents errored:     {results['documents_errored']}")
    print()

    # Per-document breakdown sorted by composite score (worst first)
    per_doc = sorted(
        results["per_document"],
        key=lambda d: 0.7 * d["information_accuracy"] + 0.3 * d["text_fidelity"],
    )
    print("  Per-document (worst first):")
    print(f"  {'Document ID':<20} {'Info':>8} {'Fidelity':>10} {'Composite':>10}")
    print("  " + "-" * 50)
    for d in per_doc:
        comp = 0.7 * d["information_accuracy"] + 0.3 * d["text_fidelity"]
        print(f"  {d['document_id']:<20} {d['information_accuracy']:>8.4f} {d['text_fidelity']:>10.4f} {comp:>10.4f}")
    print("=" * 80)


async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="http://localhost:8030")
    parser.add_argument("--limit", type=int, default=0, help="Limit number of docs (0=all)")
    parser.add_argument("--concurrency", type=int, default=5)
    parser.add_argument("--timeout", type=float, default=60.0)
    parser.add_argument("--label", default="Baseline")
    args = parser.parse_args()

    input_data = json.loads(_INPUT_PATH.read_text())
    gold_data = json.loads(_GOLD_PATH.read_text())

    if args.limit > 0:
        input_data = input_data[: args.limit]
        doc_ids = {item["document_id"] for item in input_data}
        gold_data = [g for g in gold_data if g["document_id"] in doc_ids]

    print(f"Running {len(input_data)} extraction requests against {args.endpoint}...")
    t0 = time.monotonic()
    responses = await run_extract(args.endpoint, input_data, args.concurrency, args.timeout)
    elapsed = time.monotonic() - t0
    print(f"Completed in {elapsed:.1f}s")

    results = score_submission(responses, gold_data)
    print_results(results, label=args.label)

    return results


if __name__ == "__main__":
    asyncio.run(main())
