"""Explainable ordinal screening model for MSME climate resilience.

Scores are structured decision-support indicators, not probabilities,
engineering design values or official hazard maps.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from math import isfinite
from typing import Mapping


RECOMMENDATIONS: dict[str, tuple[str, ...]] = {
    "heat": (
        "Map indoor heat hotspots and protect worker rest and hydration breaks.",
        "Evaluate shading, insulation, ventilation and efficient cooling for critical work areas.",
        "Shift heat-sensitive tasks away from the hottest hours where operationally feasible.",
    ),
    "flood": (
        "Identify floor-level equipment, inventory and electrical assets exposed to water.",
        "Review drainage, safe storage elevation, flood barriers and safe shutdown procedures.",
        "Document reopening criteria and keep supplier and customer contact backups.",
    ),
    "drought": (
        "Measure water use by process and identify the largest avoidable losses.",
        "Evaluate reuse, leak detection, efficient fixtures and a water-continuity plan.",
        "Assess dependence on water-stressed suppliers and alternative sourcing.",
    ),
    "cyclone": (
        "Inspect roof, glazing, signage and outdoor equipment vulnerability.",
        "Prepare safe shutdown, document protection and staff communication procedures.",
        "Review backup power, supplier continuity and business interruption cover.",
    ),
    "power_outage": (
        "List critical loads and estimate the minimum power required to protect them.",
        "Evaluate safe backup power and staged restart procedures.",
        "Maintain offline copies of key records and emergency contact information.",
    ),
    "water_stress": (
        "Track water use, storage and process-critical minimum requirements.",
        "Set a water-efficiency target and evaluate reuse or recycling options.",
        "Prepare a continuity plan for supply interruption and quality changes.",
    ),
}


@dataclass(frozen=True)
class HazardAssessment:
    name: str
    likelihood: int
    intensity: int
    exposure: int
    sensitivity: int
    adaptive_capacity: int
    weight: float = 1.0
    notes: str = ""

    def __post_init__(self) -> None:
        if not self.name or not self.name.strip():
            raise ValueError("hazard name must be a non-empty string")
        for field_name in ("likelihood", "intensity", "exposure", "sensitivity", "adaptive_capacity"):
            value = getattr(self, field_name)
            if not isinstance(value, int) or isinstance(value, bool) or not 1 <= value <= 5:
                raise ValueError(f"{field_name} must be an integer from 1 to 5")
        if not isfinite(self.weight) or self.weight <= 0:
            raise ValueError("weight must be positive and finite")


@dataclass(frozen=True)
class HazardScore:
    name: str
    baseline_score: float
    residual_score: float
    weight: float
    scenario_multiplier: float


@dataclass(frozen=True)
class AssessmentResult:
    overall_score: float
    risk_band: str
    hazards: tuple[HazardScore, ...]
    recommendations: tuple[str, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "overall_score": self.overall_score,
            "risk_band": self.risk_band,
            "hazards": [asdict(item) for item in self.hazards],
            "recommendations": list(self.recommendations),
            "score_interpretation": (
                "Ordinal screening score for prioritization; not a probability "
                "of loss, forecast, official hazard classification or engineering design value."
            ),
        }


def score_hazard(
    hazard: HazardAssessment,
    scenario_multiplier: float = 1.0,
) -> HazardScore:
    """Score one hazard with a transparent multiplicative ordinal rubric.

    The baseline is the product of four 1-to-5 ratings, normalized to 0-100.
    Capacity reduces residual score by up to 80% at rating 5. The optional
    scenario multiplier scales the baseline before it is capped at 100.
    """
    if not isfinite(scenario_multiplier) or scenario_multiplier < 0:
        raise ValueError("scenario_multiplier must be non-negative and finite")
    raw = (
        hazard.likelihood
        * hazard.intensity
        * hazard.exposure
        * hazard.sensitivity
        / 625.0
        * 100.0
    )
    baseline = min(100.0, raw * scenario_multiplier)
    capacity_factor = 1.0 - (hazard.adaptive_capacity - 1) / 5.0
    residual = baseline * capacity_factor
    return HazardScore(
        name=hazard.name,
        baseline_score=round(baseline, 2),
        residual_score=round(residual, 2),
        weight=hazard.weight,
        scenario_multiplier=float(scenario_multiplier),
    )


def risk_band(score: float) -> str:
    if not isfinite(score) or not 0 <= score <= 100:
        raise ValueError("score must be finite and between 0 and 100")
    if score < 25:
        return "low"
    if score < 50:
        return "moderate"
    if score < 75:
        return "high"
    return "very_high"


def assess_business(
    hazards: list[HazardAssessment],
    scenario_multipliers: Mapping[str, float] | None = None,
) -> AssessmentResult:
    """Aggregate weighted residual hazard scores and return action prompts."""
    if not hazards:
        raise ValueError("at least one hazard assessment is required")
    multipliers = scenario_multipliers or {}
    scored = tuple(
        score_hazard(hazard, multipliers.get(hazard.name, 1.0))
        for hazard in hazards
    )
    total_weight = sum(item.weight for item in scored)
    overall = sum(item.residual_score * item.weight for item in scored) / total_weight

    recommendations: list[str] = []
    ordered = sorted(scored, key=lambda item: item.residual_score * item.weight, reverse=True)
    for item in ordered:
        key = item.name.lower().replace("-", "_").replace(" ", "_")
        for action in RECOMMENDATIONS.get(key, ()):
            if action not in recommendations:
                recommendations.append(action)

    return AssessmentResult(
        overall_score=round(overall, 2),
        risk_band=risk_band(round(overall, 2)),
        hazards=scored,
        recommendations=tuple(recommendations),
    )
