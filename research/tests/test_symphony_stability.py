import sys
import unittest
from pathlib import Path
from math import cos, pi
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from one_time_field.symphony_stability import (
    phase_jacobian, symmetric_eigenvalues, classify_transverse_stability,
)


def complete(n):
    return [[0.0 if i == j else 1.0 for j in range(n)] for i in range(n)]


def ring(n):
    a = [[0.0] * n for _ in range(n)]
    for i in range(n):
        j = (i + 1) % n
        a[i][j] = a[j][i] = 1.0
    return a


class SymphonyStabilityTests(unittest.TestCase):
    def test_complete_synchronized_spectrum_matches_closed_form(self):
        n, k = 8, 1.3
        eig = symmetric_eigenvalues(phase_jacobian([0.0]*n, complete(n), k))
        expected = sorted([0.0] + [-k*n/(n-1)]*(n-1))
        for got, want in zip(eig, expected):
            self.assertAlmostEqual(got, want, places=9)

    def test_ring_q1_twist_is_transversely_stable_for_n10(self):
        n, k = 10, 1.0
        phases = [2*pi*i/n for i in range(n)]
        eig = symmetric_eigenvalues(phase_jacobian(phases, ring(n), k))
        self.assertEqual(classify_transverse_stability(eig), "linearly_asymptotically_stable")
        self.assertLess(max(x for x in eig if abs(x) > 1e-9), 0.0)

    def test_ring_q3_twist_is_linearly_unstable_for_n10(self):
        n, k = 10, 1.0
        phases = [6*pi*i/n for i in range(n)]
        eig = symmetric_eigenvalues(phase_jacobian(phases, ring(n), k))
        self.assertEqual(classify_transverse_stability(eig), "linearly_unstable")
        self.assertGreater(max(eig), 0.0)

    def test_jacobian_rows_sum_to_zero_global_phase_symmetry(self):
        j = phase_jacobian([0.1, 0.4, 1.2, 2.0], complete(4), 0.8)
        for row in j:
            self.assertAlmostEqual(sum(row), 0.0, places=12)

    def test_eigensolver_rejects_nonsymmetric_matrix(self):
        with self.assertRaises(ValueError):
            symmetric_eigenvalues([[0.0, 1.0], [0.0, 0.0]])


if __name__ == "__main__":
    unittest.main()
