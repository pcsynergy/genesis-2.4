import unittest

from research.one_time_field.upt12_observability import (
    DimensionfulParameters, PhysicalScales, compare_memory_coupling,
    infer_memory_relaxation_product,
)


class UPT12Tests(unittest.TestCase):
    def test_dimensionless_scaling_is_unit_consistent(self):
        scales = PhysicalScales(length=2.0, time=3.0, field=4.0, energy=5.0)
        params = DimensionfulParameters(10.0, 15.0, 20.0, 30.0, 35.0)
        result = params.dimensionless(scales)
        self.assertAlmostEqual(result["relational_strength"], 16.0)
        self.assertAlmostEqual(result["memory_strength"], 96.0)
        self.assertAlmostEqual(result["bistable_strength"], 2048.0)
        self.assertAlmostEqual(result["field_mobility"], 56.25)
        self.assertAlmostEqual(result["memory_mobility"], 65.625)

    def test_invalid_scales_and_parameters_rejected(self):
        with self.assertRaises(ValueError):
            PhysicalScales(1, 0, 1, 1)
        with self.assertRaises(ValueError):
            DimensionfulParameters(-1, 1, 1, 1, 1)

    def test_matched_coupled_and_uncoupled_runs_differ(self):
        result = compare_memory_coupling(node_count=32, final_time=0.01)
        self.assertGreater(abs(result["difference"]["memory"]), 0.0)
        self.assertGreater(abs(result["difference"]["mean_field"]), 0.0)

    def test_recovers_only_relaxation_product(self):
        times = [0.0, 0.1, 0.2, 0.3, 0.4]
        mismatch = [1.0, 0.9, 0.8, 0.7, 0.6]
        # dm/dt = 0.3 * mismatch, represented with midpoint-integrated data.
        memory = [0.0]
        for i in range(4):
            memory.append(memory[-1] + 0.1 * 0.3 * (mismatch[i]+mismatch[i+1])/2)
        fit = infer_memory_relaxation_product(times, memory, mismatch)
        self.assertAlmostEqual(fit["gamma_m_times_kappa"], 0.3, places=12)
        self.assertFalse(fit["separately_identifiable"])

    def test_zero_mismatch_is_unidentifiable(self):
        with self.assertRaises(ValueError):
            infer_memory_relaxation_product([0, 1, 2], [0, 0, 0], [0, 0, 0])

    def test_observation_validation(self):
        with self.assertRaises(ValueError):
            infer_memory_relaxation_product([0, 1, 1], [0, 1, 2], [1, 1, 1])


if __name__ == "__main__":
    unittest.main()
