"""UPT-16 tests: hybrid-state contracts and conservative/dissipative compatibility."""
import unittest

from one_time_field.upt16_unified_principle import (
    HybridUPTState, PotentialEnergyOntology, classify_common_energy_compatibility,
    energy_rate, gradient_flow_rhs, hamiltonian_rhs, observation_map,
    potential_energy_status,
)


class UPT16Tests(unittest.TestCase):
    def test_hybrid_state_validates_shared_dimensions(self):
        state = HybridUPTState(((0, 1), (1, 0)), (0.2, 0.8), 0.5,
                               ((0.0, 1.0), (1.0, 0.0)))
        self.assertEqual(len(state.admissible_states), 2)

    def test_hybrid_state_rejects_asymmetric_relations(self):
        with self.assertRaises(ValueError):
            HybridUPTState(((0, 1),), (0.0, 1.0), 0.0,
                           ((0.0, 1.0), (0.0, 0.0)))

    def test_gradient_flow_dissipates_for_positive_mobility(self):
        grad = (2.0, -1.0)
        velocity = gradient_flow_rhs(grad, ((2.0, 0.0), (0.0, 1.0)))
        self.assertAlmostEqual(energy_rate(grad, velocity), -9.0)

    def test_hamiltonian_flow_conserves_energy(self):
        grad = (2.0, -1.0)
        velocity = hamiltonian_rhs(grad, ((0.0, 1.0), (-1.0, 0.0)))
        self.assertAlmostEqual(energy_rate(grad, velocity), 0.0, places=12)

    def test_dual_nontrivial_flow_cannot_be_same_for_positive_mobility(self):
        result = classify_common_energy_compatibility(
            (2.0, -1.0), ((1.0, 0.0), (0.0, 1.0)),
            ((0.0, 1.0), (-1.0, 0.0)))
        self.assertLess(result["gradient_flow_energy_rate"], 0.0)
        self.assertAlmostEqual(result["hamiltonian_energy_rate"], 0.0)
        self.assertFalse(result["nontrivial_dual_dynamics_compatible"])

    def test_stationary_point_is_degenerate_compatibility(self):
        result = classify_common_energy_compatibility(
            (0.0, 0.0), ((1.0, 0.0), (0.0, 1.0)),
            ((0.0, 1.0), (-1.0, 0.0)))
        self.assertTrue(result["stationary_gradient"])
        self.assertTrue(result["same_velocity"])

    def test_observation_is_explicit_map(self):
        self.assertAlmostEqual(observation_map((1.0, 2.0, 3.0)), 6.0)
        self.assertAlmostEqual(observation_map((1.0, 2.0), (2.0, -1.0)), 0.0)

    def test_ontology_remains_unresolved_and_distinct(self):
        result = potential_energy_status(PotentialEnergyOntology.POTENTIAL_FIRST)
        self.assertFalse(result["ontological_potential_equals_energy_functional"])
        self.assertEqual(result["decision"], "unresolved by the current mathematical prototypes")

    def test_indefinite_mobility_rejected(self):
        with self.assertRaises(ValueError):
            gradient_flow_rhs((1.0, 1.0), ((1.0, 2.0), (2.0, 1.0)))


if __name__ == "__main__":
    unittest.main()
