import math
import unittest

from research.one_time_field.upt13_falsifiability import compare_memory_relaxation


def make_series(rate, count=41, dt=0.1):
    times = [i * dt for i in range(count)]
    means = [0.2 + 0.15 * math.sin(i * 0.31) for i in range(count)]
    memory = [0.7]
    for i in range(count - 1):
        decay = math.exp(-rate * dt)
        memory.append(means[i] + (memory[-1] - means[i]) * decay)
    return times, means, memory


class UPT13Tests(unittest.TestCase):
    def test_recovers_coupled_rate_and_predicts_held_out_data(self):
        times, means, memory = make_series(0.8)
        result = compare_memory_relaxation(times, means, memory, max_rate=3.0)
        self.assertAlmostEqual(result["fitted_relaxation_rate"], 0.8, places=5)
        self.assertLess(result["test_rmse_coupled"], result["test_rmse_null"])
        self.assertLess(result["train_aicc_coupled"], result["train_aicc_null"])

    def test_zero_coupling_null_is_not_outperformed(self):
        times, means, memory = make_series(0.0)
        result = compare_memory_relaxation(times, means, memory, max_rate=3.0)
        self.assertLess(result["fitted_relaxation_rate"], 1e-5)
        self.assertAlmostEqual(result["test_rmse_coupled"], result["test_rmse_null"], places=8)

    def test_rejects_nonmonotonic_time(self):
        with self.assertRaises(ValueError):
            compare_memory_relaxation([0, 1, 2, 1, 4, 5, 6, 7, 8],
                                      [0] * 9, [1] * 9)

    def test_rejects_mismatched_or_short_series(self):
        with self.assertRaises(ValueError):
            compare_memory_relaxation([0, 1, 2], [0, 1], [1, 1, 1])

    def test_rejects_invalid_split_and_rate_bound(self):
        times, means, memory = make_series(0.4)
        with self.assertRaises(ValueError):
            compare_memory_relaxation(times, means, memory, train_fraction=0.3)
        with self.assertRaises(ValueError):
            compare_memory_relaxation(times, means, memory, max_rate=0)


if __name__ == "__main__":
    unittest.main()
