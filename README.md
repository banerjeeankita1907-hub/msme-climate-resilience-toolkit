# MSME Climate Resilience Toolkit

An explainable Python screening tool for helping small businesses structure
conversations about climate-related operational risks and adaptation options.

The project accepts transparent ordinal ratings for hazards, exposure,
sensitivity and adaptive capacity, then produces weighted screening scores and
action prompts. It is a decision-support scaffold—not a hazard forecast,
probability of financial loss, engineering design or official risk map.

## Features

- Validated 1-to-5 ratings for likelihood, intensity, exposure, sensitivity and
  adaptive capacity.
- Transparent score formula and configurable hazard weights.
- Optional scenario multipliers for simple sensitivity exercises.
- Hazard-specific adaptation prompts for heat, flood, drought, cyclone,
  water stress and power outage.
- JSON input/output for auditability and integration.
- Reusable Python package, command-line interface and automated unit tests.
- No third-party runtime dependencies.

## Quick start

Python 3.10 or newer:

```bash
python -m venv .venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
python -m pip install -e .

msme-risk-assess examples/food-processing-msme.json --output assessment-report.json
python -m unittest discover -s tests -v
```

The example file is synthetic and must not be treated as an assessment of a
real company or location.

## Scoring method

For each hazard, the baseline score is the product of four ordinal inputs,
normalized to 0–100:

```text
baseline = (likelihood × intensity × exposure × sensitivity) / 625 × 100
```

A capacity factor is then applied:

```text
capacity_factor = 1 − (adaptive_capacity − 1) / 5
residual_score = min(100, baseline × scenario_multiplier) × capacity_factor
```

The capacity factor ranges from 1.0 at rating 1 to 0.2 at rating 5. Weighted
hazard scores are aggregated into a 0–100 portfolio screening score. Bands are
low (below 25), moderate (25–49.99), high (50–74.99) and very high (75–100).

These calculations are transparent ordinal heuristics. They are not calibrated
loss models, calibrated probabilities, return periods or projections of future
climate conditions.

## Example input

See [examples/food-processing-msme.json](examples/food-processing-msme.json).
Every number in that file is illustrative. For a real assessment, document the
rating rationale, local data source, assessment date, business boundary and
uncertainty for each hazard.

## Project structure

```text
src/msme_resilience/
  assessment.py     # validated scoring model and recommendations
  cli.py            # JSON command-line interface
tests/
  test_assessment.py
examples/
  food-processing-msme.json
docs/
  methodology.md    # score interpretation, safeguards and extension plan
.github/workflows/
  tests.yml
```

## Limitations and responsible use

- No local climate observations, hazard maps, asset locations or loss history
  are bundled.
- The input ratings are supplied by the assessor; no geospatial inference is
  performed.
- The model does not estimate annual loss, hazard probability, expected
  downtime, insurance premium or compliance status.
- Adaptation prompts are general planning questions, not engineering advice.
- The same score can arise from different underlying factors; inspect the
  hazard-level breakdown and retain the notes behind each rating.

Use the toolkit to organize discussion and identify data gaps. Consult local
authorities, qualified engineers, climate-risk specialists and insurers before
making investment, safety or compliance decisions.

## License

No separate license file is currently provided. Ask before reusing or
redistributing this repository's code.
