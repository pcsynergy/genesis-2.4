import sys
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from one_time_field.symphony_numerics import integrate, order_parameter, phase_error

N = 6
A = [[0.0 if i == j else 1.0 for j in range(N)] for i in range(N)]
Y = [0.0, 0.3, 0.9, 1.4, 2.0, 3.1]
W = [1.0 + 0.02*(i-2.5) for i in range(N)]


class SymphonyNumericsTests(unittest.TestCase):
    def test_rk4_refinement_reduces_error_against_fine_reference(self):
        ref = integrate(Y, A, W, 1.1, 0.000625, 16000, "rk4")
        coarse = integrate(Y, A, W, 0.02, 1.1, 500, "rk4")
        medium = integrate(Y, A, W, 0.01, 1.1, 1000, "rk4")
        fine = integrate(Y, A, W, 0.005, 1.1, 2000, "rk4")
        self.assertGreater(phase_error(ref, coarse), phase_error(ref, medium))
        self.assertGreater(phase_error(ref, medium), phase_error(ref, fine))

    def test_rk4_outperforms_euler_at_same_step(self):
        ref = integrate(Y, A, W, 1.1, 0.000625, 16000, "rk4")
        euler = integrate(Y, A, W, 1.1, 0.01, 1000, "euler")
        rk4 = integrate(Y, A, W, 1.1, 0.01, 1000, "rk4")
        self.assertLess(phase_error(ref, rk4), phase_error(ref, euler))

    def test_equal_frequency_complete_graph_relaxes_perturbation(self):
        perturbed = [0.1 + 0.08*(i-2.5) for i in range(N)]
        final = integrate(perturbed, A, [1.0]*N, 1.0, 0.005, 3000, "rk4")
        self.assertGreater(order_parameter(final), order_parameter(perturbed))

    def test_integrator_rejects_invalid_method(self):
        with self.assertRaises(ValueError):
            integrate(Y, A, W, 1.0, 0.01, 10, "midpoint")

    def test_integrator_rejects_nonpositive_step(self):
        with self.assertRaises(ValueError):
            integrate(Y, A, W, 1.0, 0.0, 10, "rk4")


if __name__ == "__main__":
    unittest.main()
