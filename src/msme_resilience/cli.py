"""Command-line interface for repeatable MSME climate-risk screening."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .assessment import HazardAssessment, assess_business


def load_assessment(path: Path) -> tuple[str, dict[str, object]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict) or not isinstance(payload.get("hazards"), list):
        raise ValueError("input JSON must be an object containing a hazards array")
    business_name = str(payload.get("business_name", "Unspecified MSME"))
    hazards = [HazardAssessment(**item) for item in payload["hazards"]]
    result = assess_business(hazards, payload.get("scenario_multipliers", {}))
    report = {
        "business_name": business_name,
        "assessment": result.to_dict(),
    }
    return business_name, report


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an explainable MSME climate-resilience screening report."
    )
    parser.add_argument("input", type=Path, help="Path to a JSON assessment file")
    parser.add_argument("--output", type=Path, default=Path("assessment-report.json"))
    args = parser.parse_args()

    try:
        _, report = load_assessment(args.input)
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as error:
        parser.error(str(error))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    assessment = report["assessment"]
    print(f"Saved report to {args.output}")
    print(f"Screening score: {assessment['overall_score']}/100 ({assessment['risk_band']})")


if __name__ == "__main__":
    main()
