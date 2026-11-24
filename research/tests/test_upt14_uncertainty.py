"""Tests for UPT-14 noisy inference and null calibration."""
import math
import unittest
from one_time_field.upt14_uncertainty import (
    bootstrap_null_test, bootstrap_rate_interval, fit_relaxation_rate,
    predict_memory, simulate_observations,
)


def fixture(rate=0.75, sigma=0.015, seed=14):
    times = [i * 0.12 for i in range(36)]
    mean = [0.25 + 0.18 * math.sin(i * 0.37) for i in range(36)]
    return times, mean, simulate_observations(times, mean, 0.72, rate, sigma, seed)


class UPT14Tests(unittest.TestCase):
    def test_exact_trajectory_and_zero_rate(self):
        t, u = [0.0, 0.5, 1.0], [1.0, 2.0, 3.0]
        for value in predict_memory(t, u, 0.4, 0.0):
            self.assertAlmostEqual(value, 0.4, places=14)
        self.assertGreater(predict_memory(t, u, 0.4, 1.0)[1], 0.4)

    def test_recovers_noisy_positive_rate(self):
        t, u, y = fixture()
        result = fit_relaxation_rate(t, u, y, 0.015, max_rate=3.0)
        self.assertAlmostEqual(result["fitted_relaxation_rate"], 0.75, delta=0.12)

    def test_null_rate_is_nonnegative(self):
        t, u, y = fixture(rate=0.0, sigma=0.01, seed=77)
        self.assertGreaterEqual(fit_relaxation_rate(t, u, y, 0.01, 3.0)["fitted_relaxation_rate"], 0.0)

    def test_bootstrap_interval_is_ordered(self):
        t, u, y = fixture()
        result = bootstrap_rate_interval(t, u, y, 0.015, max_rate=3.0, replicates=40, seed=3)
        self.assertLessEqual(result["interval_low"], result["interval_high"])
        self.assertEqual(result["bootstrap_replicates"], 40)

    def test_null_calibration_returns_valid_p_value(self):
        t, u, y = fixture(rate=0.0, sigma=0.02, seed=19)
        result = bootstrap_null_test(t, u, y, 0.02, max_rate=3.0, replicates=99, seed=21)
        self.assertGreater(result["null_bootstrap_p_value"], 0.0)
        self.assertLessEqual(result["null_bootstrap_p_value"], 1.0)

    def test_simulation_reproducible(self):
        t, u, _ = fixture()
        self.assertEqual(simulate_observations(t, u, 0.72, 0.5, 0.02, 123),
                         simulate_observations(t, u, 0.72, 0.5, 0.02, 123))

    def test_rejects_invalid_noise_and_time(self):
        t, u, y = fixture()
        with self.assertRaises(ValueError):
            fit_relaxation_rate(t, u, y, 0.0)
        bad = list(t); bad[4] = bad[3]
        with self.assertRaises(ValueError):
            fit_relaxation_rate(bad, u, y, 0.02)

    def test_rejects_too_few_null_replicates(self):
        t, u, y = fixture()
        with self.assertRaises(ValueError):
            bootstrap_null_test(t, u, y, 0.02, replicates=20)


if __name__ == "__main__":
    unittest.main()
