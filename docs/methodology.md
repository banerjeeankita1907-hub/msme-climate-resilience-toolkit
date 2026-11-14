# Methodology, interpretation and extension plan

## Purpose

The toolkit turns qualitative business-context assessments into a repeatable,
transparent screening record. It is designed to prompt structured discussions
about climate-related operational continuity at a small business. It is not a
climate model and contains no observed hazard data.

## Input rubric

Each hazard receives five ordinal ratings from 1 to 5:

- Likelihood: assessor's relative judgment of how often the hazard may affect
  the business within a stated planning horizon.
- Intensity: relative severity of the event or condition.
- Exposure: extent to which people, assets, processes or suppliers are in the
  affected area or dependent on the affected resource.
- Sensitivity: degree to which the business is affected if exposed.
- Adaptive capacity: existing ability to prepare, respond, recover and adapt.

The rating anchors are intentionally configurable by the assessor and must be
written down for a real use case. A consistent project should publish its
rating guide before collecting assessments and use a documented planning
horizon.

## Score definition

The baseline score is

    100 × likelihood × intensity × exposure × sensitivity / 5⁴

The scenario multiplier scales that baseline and the result is capped at 100.
The capacity factor is

    1 − (adaptive_capacity − 1) / 5

The residual score is the capped baseline multiplied by this factor. This
reduces the score by 0–80% over the adaptive-capacity rating range. Hazard
weights are positive user-provided importance weights. The portfolio score is
the weighted mean of residual hazard scores.

A multiplier greater than one is a sensitivity exercise, not a forecast. It
does not imply a future climate projection or a probability distribution.

## Interpretation safeguards

The output is an ordinal prioritization indicator. It is not a probability,
expected annual loss, return period, hazard map, engineering safety threshold,
insurance rating or regulatory compliance result. The 1-to-5 values are not
assumed to be interval-scale physical measurements. The arithmetic is a
transparent aggregation rule, not a statistically calibrated model.

Two businesses can receive the same summary score for different reasons.
Decision makers should inspect the per-hazard details, notes, data quality and
context before selecting an action. A high adaptive-capacity rating should be
supported by evidence such as tested plans, funding, equipment and staff
training, not optimism alone.

## Research-grade evaluation plan

1. Define a sector-specific rating rubric and planning horizon before scoring.
2. Collect assessor-independent ratings and measure inter-rater agreement.
3. Compare the score with documented interruption, damage and recovery data.
4. Test alternative aggregation rules and sensitivity to weights.
5. Separate current climate baseline from future climate scenarios sourced
   from named, versioned datasets.
6. Publish uncertainty, missing-data policy, assumptions and subgroup results.
7. Co-design recommendations with MSME owners, workers and local experts.

## Data responsibility

Do not upload identifiable employee, customer, supplier or financial records
into example files. Prefer aggregated business-level information. Clearly mark
all synthetic inputs and distinguish assessor judgments from measured data.
