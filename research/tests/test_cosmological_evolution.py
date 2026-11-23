import unittest
from research.one_time_field.cosmological_evolution import evolve_cosmology
from research.one_time_field.lorentz_covariant import CovariantParameters

class TestCosmologicalEvolution(unittest.TestCase):
    def setUp(self):
        self.params = CovariantParameters(
            field_mass=0.7, clock_kinetic=1.0,
            clock_mass_squared=0.5, coupling=0.02
        )

    def test_initial_friedmann_constraint(self):
        rows = evolve_cosmology(self.params, duration=0.2, steps=40)
        self.assertAlmostEqual(rows[0]["friedmann_residual"], 0.0, places=14)

    def test_scale_factor_positive_and_expanding(self):
        rows = evolve_cosmology(self.params, duration=1.0, steps=500)
        self.assertTrue(all(row["scale_factor"] > 0 for row in rows))
        self.assertGreater(rows[-1]["scale_factor"], rows[0]["scale_factor"])

    def test_hubble_evolves_by_acceleration_equation(self):
        rows = evolve_cosmology(self.params, duration=0.1, steps=100)
        self.assertNotEqual(rows[-1]["hubble"], rows[0]["hubble"])
        self.assertTrue(all(row["hubble"] > 0 for row in rows))

    def test_constraint_drift_converges_under_refinement(self):
        coarse = evolve_cosmology(self.params, duration=1.0, steps=100)
        fine = evolve_cosmology(self.params, duration=1.0, steps=200)
        coarse_error = abs(coarse[-1]["friedmann_residual"])
        fine_error = abs(fine[-1]["friedmann_residual"])
        self.assertGreater(coarse_error, 0.0)
        self.assertLess(fine_error, coarse_error)

    def test_uncoupled_limit(self):
        p = CovariantParameters(field_mass=0.7, clock_kinetic=1.0,
                                clock_mass_squared=0.5, coupling=0.0)
        rows = evolve_cosmology(p, duration=0.5, steps=100)
        self.assertTrue(all(abs(r["friedmann_residual"]) < 1e-8 for r in rows))

    def test_contracting_branch(self):
        rows = evolve_cosmology(self.params, duration=0.1, steps=50, expanding=False)
        self.assertLess(rows[0]["hubble"], 0.0)
        self.assertLess(rows[-1]["scale_factor"], rows[0]["scale_factor"])

    def test_invalid_initial_data(self):
        with self.assertRaises(ValueError):
            evolve_cosmology(self.params, scale_factor_0=0)
        with self.assertRaises(ValueError):
            evolve_cosmology(self.params, duration=0)
        with self.assertRaises(ValueError):
            evolve_cosmology(self.params, steps=0)

if __name__ == "__main__":
    unittest.main()
