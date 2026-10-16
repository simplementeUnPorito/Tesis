import json
import math
import unittest

from ftm_masw_geometry import (
    along_axis_interval,
    build_results,
    minimum_zero_failure_trials,
    phase_error_deg,
)


class GeometryTests(unittest.TestCase):
    def test_along_axis_interval_analytic_cases(self):
        self.assertEqual(along_axis_interval(5, 0, 2), (3, 5))
        self.assertEqual(along_axis_interval(5, 1, 0), (4, 6))
        self.assertEqual(along_axis_interval(0.5, 1, 0.2), (0, 1.5))
        self.assertEqual(along_axis_interval(5, 0, 0, 3), (4, 5))
        measured = math.hypot(0.2, 0.4)
        lower, upper = along_axis_interval(measured, 0, 0.2)
        self.assertAlmostEqual(lower, 0.2)
        self.assertAlmostEqual(upper, measured)

    def test_bounds_contain_independently_constructed_3d_layouts(self):
        for spacing in (0.0, 0.5, 2.0, 10.0):
            for lateral in (0.0, 0.1, 0.4):
                for height in (0.0, 0.3):
                    measured = math.dist((0, 0, 0), (spacing, lateral, height))
                    for offset in (-0.05, 0.0, 0.05):
                        observed = max(0, measured + offset)
                        lower, upper = along_axis_interval(observed, 0.05, 0.2, 0.3)
                        self.assertLessEqual(lower, spacing + 1e-12)
                        self.assertGreaterEqual(upper, spacing - 1e-12)

    def test_phase_error_and_zero_failure_trials(self):
        self.assertEqual(phase_error_deg(0.5, 2), 90)
        self.assertEqual(minimum_zero_failure_trials(), 59)

    def test_invalid_numeric_inputs_are_rejected(self):
        bad = (-1, math.nan, math.inf)
        interval_args = ("range_m", "error_m", "half_width_m",
                         "height_difference_max_m")
        for name in interval_args:
            for value in bad:
                values = dict(range_m=1, error_m=0, half_width_m=0,
                              height_difference_max_m=0)
                values[name] = value
                with self.subTest(helper="interval", argument=name, value=value):
                    with self.assertRaises(ValueError):
                        along_axis_interval(**values)
        for value in bad:
            with self.subTest(helper="phase-error", value=value):
                with self.assertRaises(ValueError):
                    phase_error_deg(value, 1)
        for wavelength in (0, -1, math.nan, math.inf):
            with self.subTest(wavelength=wavelength):
                with self.assertRaises(ValueError):
                    phase_error_deg(1, wavelength)
        for coverage, confidence in ((0, 0.95), (1, 0.95), (0.95, 0),
                                     (0.95, 1), (math.nan, 0.95),
                                     (0.95, math.inf)):
            with self.subTest(coverage=coverage, confidence=confidence):
                with self.assertRaises(ValueError):
                    minimum_zero_failure_trials(coverage, confidence)

    def test_results_are_complete_and_strict_json(self):
        results = build_results()
        self.assertEqual(len(results["range_excess_scenarios"]), 20)
        self.assertEqual(len(results["phase_error_scenarios"]), 16)
        self.assertEqual(len(results["zero_failure_trials"]), 3)
        self.assertEqual(len(results["bound_examples"]), 3)
        self.assertIn("no measured performance", results["metadata"]["scope"])
        json.dumps(results, allow_nan=False)


if __name__ == "__main__":
    unittest.main()
