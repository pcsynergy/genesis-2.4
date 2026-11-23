import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from one_time_field.upt6_continuum import (
    diffusion_rate, massless_wave_acceleration, periodic_laplacian,
    periodic_wave_energy, shift_noether_charge, shift_symmetry_status,
)

class UPT6ContinuumTests(unittest.TestCase):
    def test_periodic_laplacian_has_zero_spatial_sum(self):
        lap = periodic_laplacian([0.2, 1.1, -0.4, 0.7, 1.8, -0.2], 0.3)
        self.assertAlmostEqual(sum(lap), 0.0, places=12)

    def test_noether_shift_charge_is_unchanged_by_wave_acceleration(self):
        values = [0.0, 1.0, 0.0, -1.0, 0.0, 0.5]
        velocities = [0.2, -0.1, 0.4, 0.3, -0.2, 0.1]
        dx, dt = 0.25, 0.01
        acceleration = massless_wave_acceleration(values, dx, wave_speed=1.7)
        updated = [v + dt*a for v, a in zip(velocities, acceleration)]
        self.assertAlmostEqual(shift_noether_charge(updated, dx), shift_noether_charge(velocities, dx), places=12)

    def test_diffusion_rate_sums_to_zero_on_periodic_domain(self):
        rate = diffusion_rate([0.0, 1.0, 0.0, -1.0], 0.5, diffusivity=0.3)
        self.assertAlmostEqual(sum(rate), 0.0, places=12)

    def test_wave_and_diffusion_use_distinct_time_orders(self):
        values = [0.0, 1.0, 0.0, -1.0]
        self.assertNotEqual(massless_wave_acceleration(values, 1.0, wave_speed=2.0), diffusion_rate(values, 1.0))

    def test_massless_wave_energy_is_nonnegative(self):
        energy = periodic_wave_energy([0.0, 1.0, 0.0, -1.0], [0.1, 0.0, -0.1, 0.0], 0.5)
        self.assertGreaterEqual(energy, 0.0)

    def test_shift_symmetry_requires_shift_invariant_potential(self):
        self.assertEqual(shift_symmetry_status(True), "shift_symmetric")
        self.assertEqual(shift_symmetry_status(False), "explicitly_broken")

    def test_validation_rejects_nonpositive_spacing(self):
        with self.assertRaises(ValueError):
            periodic_laplacian([0.0, 1.0, 0.0], 0.0)

if __name__ == "__main__":
    unittest.main()
