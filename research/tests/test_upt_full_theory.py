"""Integration tests for the full UPT reference model."""
import unittest
from one_time_field.upt_full_theory import FullUPTConfig, run_full_theory


class FullUPTTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = run_full_theory(FullUPTConfig(
            continuous_steps=80, bootstrap_replicates=20,
            null_replicates=99, seed=15115,
        ))

    def test_potential_domain_expands_and_closes(self):
        sizes = self.result["potential_space"]["domain_sizes_by_renewal_round"]
        self.assertGreater(sizes[-1], sizes[0])
        self.assertTrue(self.result["potential_space"]["closure_reached"])

    def test_reversible_memory_is_normalized_and_detailed_balanced(self):
        layer = self.result["reversible_memory"]
        self.assertAlmostEqual(layer["stationary_probability_sum"], 1.0, places=12)
        self.assertLess(layer["detailed_balance_max_residual"], 1e-12)

    def test_continuous_field_energy_does_not_increase(self):
        layer = self.result["continuous_field"]
        self.assertLessEqual(layer["final_energy"], layer["initial_energy"] + 1e-12)

    def test_continuum_refinement_error_decreases(self):
        errors = [row["field_rms_error"]
                  for row in self.result["continuum_refinement"]["coarse_to_fine"]]
        self.assertTrue(all(errors[i + 1] < errors[i] for i in range(len(errors) - 1)))

    def test_noisy_inference_reports_uncertainty_and_null_test(self):
        layer = self.result["observation_and_inference"]
        self.assertGreaterEqual(layer["fit"]["fitted_relaxation_rate"], 0.0)
        self.assertLessEqual(layer["bootstrap_interval"]["interval_low"],
                             layer["bootstrap_interval"]["interval_high"])
        self.assertGreater(layer["null_test"]["null_bootstrap_p_value"], 0.0)

    def test_layers_are_explicitly_not_equated(self):
        contract = self.result["integration_contract"]
        self.assertIn("distinct", contract["potential_domain_to_ctmc"])
        self.assertIn("not a derived", contract["ctmc_to_gradient_flow"])


if __name__ == "__main__":
    unittest.main()
