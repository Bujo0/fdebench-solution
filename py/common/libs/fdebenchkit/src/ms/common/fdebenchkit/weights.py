# Copyright (c) Microsoft. All rights reserved.
"""FDEBench scoring functions — Tier 1 composite and cross-task aggregation.

All formulas match ``docs/context/10-fdebench.md`` exactly.
"""

import logging

from ms.common.fdebenchkit.models import EfficiencyResult
from ms.common.fdebenchkit.models import FDEBenchComposite
from ms.common.fdebenchkit.models import RobustnessResult
from ms.common.fdebenchkit.models import TaskResolutionResult
from ms.common.fdebenchkit.models import Tier1Score

logger = logging.getLogger(__name__)

# ── Tier 1 weights (from 10-fdebench.md) ─────────────────────────────

TIER1_WEIGHT_RESOLUTION = 0.50
TIER1_WEIGHT_EFFICIENCY = 0.20
TIER1_WEIGHT_ROBUSTNESS = 0.30

# ── Efficiency sub-weights ────────────────────────────────────────────

EFFICIENCY_WEIGHT_LATENCY = 0.60
EFFICIENCY_WEIGHT_COST = 0.40

# ── Efficiency normalization thresholds ───────────────────────────────
# Calibrated for LLM workloads: nano models achieve ~400-600ms,
# full models ~1-3s, reasoning models ~3-10s.

LATENCY_BEST_MS = 500.0  # P95 < 500ms → 1.0
LATENCY_WORST_MS = 5000.0  # P95 > 5000ms → 0.0

# ── Robustness sub-weights ────────────────────────────────────────────

ROBUSTNESS_WEIGHT_ADVERSARIAL = 0.60
ROBUSTNESS_WEIGHT_API_RESILIENCE = 0.40


# ══════════════════════════════════════════════════════════════════════
#  TIER 2: LLM-as-Judge Agent Weights
# ══════════════════════════════════════════════════════════════════════
# Tier 2 is advisory (judge-only, not on public leaderboard).
# Four agents run in parallel, each scoring independent dimensions.

TIER2_AGENT_WEIGHTS: dict[str, float] = {
    "code-quality": 0.25,
    "architecture-design": 0.30,
    "ai-problem-solving": 0.25,
    "engineering-maturity": 0.20,
}

# Per-agent dimension weights (must sum to 1.0 within each agent).

TIER2_CODE_QUALITY_DIMENSIONS: dict[str, float] = {
    "structure_modularity": 0.20,
    "type_safety": 0.20,
    "error_handling": 0.20,
    "testing": 0.20,
    "readability": 0.10,
    "documentation": 0.10,
}

TIER2_ARCHITECTURE_DESIGN_DIMENSIONS: dict[str, float] = {
    "ai_pipeline_design": 0.25,
    "system_decomposition": 0.20,
    "api_design": 0.20,
    "tradeoff_reasoning": 0.15,
    "scalability_thinking": 0.10,
    "integration": 0.10,
}

TIER2_AI_PROBLEM_SOLVING_DIMENSIONS: dict[str, float] = {
    "prompt_engineering": 0.30,
    "evaluation_methodology": 0.25,
    "problem_solving_approach": 0.20,
    "documentation_communication": 0.15,
    "model_cost_awareness": 0.10,
}

TIER2_ENGINEERING_MATURITY_DIMENSIONS: dict[str, float] = {
    "deployment_readiness": 0.25,
    "configuration_secrets": 0.20,
    "observability": 0.15,
    "security_awareness": 0.20,
    "dependency_management": 0.10,
    "ci_cd": 0.10,
}

TIER2_ALL_DIMENSIONS: dict[str, dict[str, float]] = {
    "code-quality": TIER2_CODE_QUALITY_DIMENSIONS,
    "architecture-design": TIER2_ARCHITECTURE_DESIGN_DIMENSIONS,
    "ai-problem-solving": TIER2_AI_PROBLEM_SOLVING_DIMENSIONS,
    "engineering-maturity": TIER2_ENGINEERING_MATURITY_DIMENSIONS,
}


def _normalize_linear(value: float, best: float, worst: float) -> float:
    """Linearly normalize a value between best (1.0) and worst (0.0).

    Values beyond the range are clamped to [0.0, 1.0].
    """
    if best == worst:
        return 1.0 if value <= best else 0.0
    score = (worst - value) / (worst - best)
    return max(0.0, min(1.0, score))


def validate_resolution_result(result: TaskResolutionResult) -> list[str]:
    """Validate that a resolution result conforms to the FDEBench contract.

    Returns a list of violations (empty = valid).
    """
    violations: list[str] = []

    if not (0.0 <= result.resolution <= 100.0):
        violations.append(f"resolution {result.resolution} not in [0, 100]")

    for dim, score in result.dimension_scores.items():
        if not (0.0 <= score <= 1.0):
            violations.append(f"dimension '{dim}' score {score} not in [0, 1]")

    weight_sum = sum(result.dimension_weights.values())
    if abs(weight_sum - 1.0) > 0.01:
        violations.append(f"dimension weights sum to {weight_sum:.4f}, expected 1.0")

    for dim in result.dimension_scores:
        if dim not in result.dimension_weights:
            violations.append(f"dimension '{dim}' in scores but not in weights")

    # Verify resolution ≈ weighted sum × 100
    recomputed = (
        sum(result.dimension_weights.get(dim, 0) * score for dim, score in result.dimension_scores.items()) * 100
    )
    if abs(result.resolution - recomputed) > 1.0:
        violations.append(f"resolution {result.resolution:.1f} != recomputed {recomputed:.1f}")

    return violations


def compute_efficiency(
    latency_p95_ms: float,
    cost_score: float,
) -> EfficiencyResult:
    """Compute the efficiency score from P95 latency and model-tier cost.

    Formula:
      efficiency = 0.60 × latency_score + 0.40 × cost_score

    Latency: P95 < 500ms → 1.0, P95 > 5000ms → 0.0 (linear)
    Cost: deterministic model-tier score (0.0–1.0) from ``_MODEL_TIER_SCORES``
    """
    latency_score = _normalize_linear(latency_p95_ms, LATENCY_BEST_MS, LATENCY_WORST_MS)

    efficiency = EFFICIENCY_WEIGHT_LATENCY * latency_score + EFFICIENCY_WEIGHT_COST * cost_score

    return EfficiencyResult(
        latency_score=round(latency_score, 4),
        cost_score=round(cost_score, 4),
        efficiency=round(efficiency, 4),
        latency_p50_ms=latency_p95_ms,  # Field name kept for compat; value is P95
        cost_per_item_usd=0.0,  # Deprecated: model-tier scoring replaces per-item cost
    )


def compute_robustness(
    adversarial_accuracy: float,
    probes_passed: int,
    probes_total: int,
) -> RobustnessResult:
    """Compute the robustness score from adversarial accuracy and API probes.

    Formula:
      robustness = 0.60 × adversarial_accuracy + 0.40 × api_resilience
      api_resilience = probes_passed / probes_total

    ``adversarial_accuracy`` is the resolution score on the adversarial
    subset only (0.0–1.0). It uses the same task-specific scorer but
    filtered to adversarial instances.
    """
    api_resilience = probes_passed / probes_total if probes_total > 0 else 0.0

    robustness = (
        ROBUSTNESS_WEIGHT_ADVERSARIAL * adversarial_accuracy + ROBUSTNESS_WEIGHT_API_RESILIENCE * api_resilience
    )

    return RobustnessResult(
        adversarial_accuracy=round(adversarial_accuracy, 4),
        api_resilience=round(api_resilience, 4),
        robustness=round(robustness, 4),
        probes_passed=probes_passed,
        probes_total=probes_total,
    )


def compute_tier1(
    task_id: str,
    resolution: float,
    efficiency: float,
    robustness: float,
) -> Tier1Score:
    """Compute the Tier 1 composite for a single task.

    Formula:
      tier1 = 0.50 × resolution + 0.20 × efficiency + 0.30 × robustness

    All inputs are 0–100. Output is 0–100.
    """
    tier1 = (
        TIER1_WEIGHT_RESOLUTION * resolution
        + TIER1_WEIGHT_EFFICIENCY * efficiency
        + TIER1_WEIGHT_ROBUSTNESS * robustness
    )

    return Tier1Score(
        task_id=task_id,
        resolution=round(resolution, 1),
        efficiency=round(efficiency, 1),
        robustness=round(robustness, 1),
        tier1=round(tier1, 1),
    )


def compute_fdebench_composite(
    task_scores: list[Tier1Score],
    *,
    aggregation: str = "mean",
) -> FDEBenchComposite:
    """Compute the FDEBench composite across all tasks.

    Aggregation methods:
      - "mean": average of per-task Tier 1 scores (default)
      - "min":  worst-task score (rewards consistency)

    Raises ValueError if no task scores provided.
    """
    if not task_scores:
        msg = "At least one task score is required"
        raise ValueError(msg)

    tier1_values = [ts.tier1 for ts in task_scores]

    if aggregation == "mean":
        fdebench = sum(tier1_values) / len(tier1_values)
    elif aggregation == "min":
        fdebench = min(tier1_values)
    else:
        msg = f"Unknown aggregation: {aggregation!r}. Use 'mean' or 'min'."
        raise ValueError(msg)

    return FDEBenchComposite(
        task_scores=task_scores,
        aggregation=aggregation,
        fdebench=round(fdebench, 1),
    )
