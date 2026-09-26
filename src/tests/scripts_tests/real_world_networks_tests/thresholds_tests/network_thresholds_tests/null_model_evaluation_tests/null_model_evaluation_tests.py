import unittest
from types import SimpleNamespace

import numpy as np

from experiments.scripts.real_world_networks.thresholds.network_thresholds.null_model_evaluation import \
    null_model_evaluation as null_model_module
from experiments.scripts.real_world_networks.thresholds.network_thresholds.null_model_evaluation.null_model_evaluation_dataclass import \
    NullModelEvaluation


class CandidateThresholdStub:

    def __init__(self, value, modularity=0.6, conductance=0.2):
        self.value = value
        self.intrinsic_evaluation = SimpleNamespace(
            modularity=modularity,
            conductance=conductance
        )
        self.null_model_evaluation = None


class TestNullModelEvaluation(unittest.TestCase):

    def test_compute_modularity_statistics_with_invalid_results(self):
        candidate = CandidateThresholdStub(
            value=0.2,
            modularity=0.6
        )

        result = null_model_module._compute_null_modularities_statistics(
            candidate_threshold=candidate,
            null_modularities=[0.2, 0.4, 0.8],
            number_of_null_models=4
        )

        expected_mean = np.mean([0.2, 0.4, 0.8])
        expected_std = np.std([0.2, 0.4, 0.8], ddof=1)
        self.assertAlmostEqual(result[0], expected_mean)
        self.assertAlmostEqual(result[1], expected_std)
        self.assertAlmostEqual(
            result[2],
            (0.6 - expected_mean) / expected_std
        )
        self.assertAlmostEqual(result[3], 3 / 5)
        self.assertEqual(result[4], 3)

    def test_compute_modularity_statistics_without_valid_results(self):
        candidate = CandidateThresholdStub(value=0.2)

        result = null_model_module._compute_null_modularities_statistics(
            candidate_threshold=candidate,
            null_modularities=[],
            number_of_null_models=4
        )

        self.assertEqual(
            result,
            (None, None, None, 1.0, 5)
        )

    def test_compute_modularity_statistics_zero_standard_deviation(self):
        candidate = CandidateThresholdStub(
            value=0.2,
            modularity=0.6
        )

        result = null_model_module._compute_null_modularities_statistics(
            candidate_threshold=candidate,
            null_modularities=[0.4, 0.4],
            number_of_null_models=2
        )

        self.assertEqual(result[0], 0.4)
        self.assertEqual(result[1], 0.0)
        self.assertIsNone(result[2])
        self.assertAlmostEqual(result[3], 1 / 3)
        self.assertEqual(result[4], 1)

    def test_compute_conductance_statistics_with_invalid_results(self):
        candidate = CandidateThresholdStub(
            value=0.2,
            conductance=0.2
        )

        result = null_model_module._compute_null_conductances_statistics(
            candidate_threshold=candidate,
            null_conductances=[0.1, 0.3, 0.4],
            number_of_null_models=4
        )

        expected_mean = np.mean([0.1, 0.3, 0.4])
        expected_std = np.std([0.1, 0.3, 0.4], ddof=1)
        self.assertAlmostEqual(result[0], expected_mean)
        self.assertAlmostEqual(result[1], expected_std)
        self.assertAlmostEqual(
            result[2],
            (expected_mean - 0.2) / expected_std
        )
        self.assertAlmostEqual(result[3], 3 / 5)
        self.assertEqual(result[4], 3)

    def test_compute_conductance_statistics_without_valid_results(self):
        candidate = CandidateThresholdStub(value=0.2)

        result = null_model_module._compute_null_conductances_statistics(
            candidate_threshold=candidate,
            null_conductances=[],
            number_of_null_models=3
        )

        self.assertEqual(
            result,
            (None, None, None, 1.0, 4)
        )

    def test_null_model_evaluation_fieldnames_and_to_dict(self):
        evaluation = NullModelEvaluation(
            number_of_null_graphs=4,
            number_of_valid_results=3,
            null_modularities=[0.2, 0.4, 0.8],
            mean_null_modularity=0.466,
            std_null_modularity=0.306,
            modularity_z_score=0.438,
            modularity_empirical_p_value=0.6,
            modularity_rank=3,
            null_conductances=[0.1, 0.3, 0.4],
            mean_null_conductance=0.266,
            std_null_conductance=0.153,
            conductance_z_score=0.436,
            conductance_empirical_p_value=0.6,
            conductance_rank=3
        )

        self.assertEqual(
            NullModelEvaluation.fieldnames(),
            [
                "#Null Graphs",
                "#Valid Null Modularities and Conductances",
                "Null Modularities",
                "Mean Null Modularity",
                "Std Null Modularity",
                "Z Modularity",
                "Modularity Empirical p-value",
                "Modularity Rank",
                "Null Conductances",
                "Mean Null Conductance",
                "Std Null Conductance",
                "Z Conductance",
                "Conductance Empirical p-value",
                "Conductance Rank",
                "Acceptable Null Model?"
            ]
        )
        self.assertEqual(
            evaluation.to_dict(),
            {
                "#Null Graphs": 4,
                "#Valid Null Modularities and Conductances": 3,
                "Null Modularities": [0.2, 0.4, 0.8],
                "Mean Null Modularity": 0.466,
                "Std Null Modularity": 0.306,
                "Z Modularity": 0.438,
                "Modularity Empirical p-value": 0.6,
                "Modularity Rank": 3,
                "Null Conductances": [0.1, 0.3, 0.4],
                "Mean Null Conductance": 0.266,
                "Std Null Conductance": 0.153,
                "Z Conductance": 0.436,
                "Conductance Empirical p-value": 0.6,
                "Conductance Rank": 3,
                "Acceptable Null Model?": None
            }
        )


if __name__ == "__main__":
    unittest.main()
