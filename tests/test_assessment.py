import unittest

from msme_resilience.assessment import (
    HazardAssessment,
    assess_business,
    risk_band,
    score_hazard,
)


class HazardScoringTests(unittest.TestCase):
    def test_maximum_baseline_and_capacity_reduction(self):
        weak_capacity = HazardAssessment("heat", 5, 5, 5, 5, 1)
        strong_capacity = HazardAssessment("heat", 5, 5, 5, 5, 5)
        self.assertEqual(score_hazard(weak_capacity).baseline_score, 100.0)
        self.assertEqual(score_hazard(weak_capacity).residual_score, 100.0)
        self.assertEqual(score_hazard(strong_capacity).residual_score, 20.0)

    def test_scenario_multiplier_is_capped(self):
        hazard = HazardAssessment("flood", 4, 4, 4, 4, 1)
        result = score_hazard(hazard, scenario_multiplier=3.0)
        self.assertEqual(result.baseline_score, 100.0)
        self.assertEqual(result.residual_score, 100.0)

    def test_weighted_aggregation(self):
        low = HazardAssessment("heat", 1, 1, 1, 1, 1, weight=1.0)
        high = HazardAssessment("flood", 5, 5, 5, 5, 1, weight=3.0)
        result = assess_business([low, high])
        self.assertGreater(result.overall_score, 70.0)
        self.assertEqual(result.risk_band, "very_high")

    def test_scenario_applies_by_hazard_name(self):
        hazard = HazardAssessment("heat", 2, 2, 2, 2, 1)
        baseline = assess_business([hazard])
        scenario = assess_business([hazard], {"heat": 2.0})
        self.assertGreater(scenario.overall_score, baseline.overall_score)

    def test_hazard_recommendations_are_explainable(self):
        result = assess_business([HazardAssessment("flood", 5, 5, 5, 5, 1)])
        self.assertTrue(any("drainage" in item.lower() for item in result.recommendations))

    def test_rejects_invalid_inputs(self):
        with self.assertRaises(ValueError):
            HazardAssessment("heat", 6, 2, 2, 2, 2)
        with self.assertRaises(ValueError):
            HazardAssessment("heat", 2, 2, 2, 2, 2, weight=0)
        with self.assertRaises(ValueError):
            score_hazard(HazardAssessment("heat", 1, 1, 1, 1, 1), -1)
        with self.assertRaises(ValueError):
            assess_business([])

    def test_risk_bands(self):
        self.assertEqual(risk_band(0), "low")
        self.assertEqual(risk_band(25), "moderate")
        self.assertEqual(risk_band(50), "high")
        self.assertEqual(risk_band(75), "very_high")


if __name__ == "__main__":
    unittest.main()
