import unittest

import numpy as np

from experiments.scripts.real_world_networks.thresholds.network_thresholds.stability_evaluation import \
    stability_evaluation as stability_module
from experiments.scripts.real_world_networks.thresholds.network_thresholds.stability_evaluation.stability_evaluation_dataclass import \
    StabilityEvaluation


class CandidateThresholdStub:

    def __init__(self, value):
        self.value = value
        self.stability_evaluation = None


class TestStabilityEvaluation(unittest.TestCase):

    def test_compute_stability_counts_missing_similarities_as_zero(self):
        self.assertEqual(
            stability_module._compute_stability(
                sims=[1.0, 0.5],
                number_of_perturbed_graphs=4
            ),
            0.375
        )
        self.assertEqual(
            stability_module._compute_stability(
                sims=[],
                number_of_perturbed_graphs=4
            ),
            0.0
        )

    def test_fuzzy_co_membership_similarity_for_identical_structures(self):
        U = np.array(
            [
                [1.0, 0.0],
                [0.5, 0.5],
                [0.0, 1.0]
            ]
        )

        similarity = (
            stability_module._compute_fuzzy_co_membership_similarity(
                U=U,
                first_cluster_discarded=False,
                perturbed_U=U.copy(),
                perturbed_first_cluster_discarded=False
            )
        )

        self.assertAlmostEqual(similarity, 1.0)

    def test_fuzzy_similarity_is_invariant_to_community_column_order(self):
        U = np.array(
            [
                [1.0, 0.0],
                [0.7, 0.3],
                [0.0, 1.0]
            ]
        )
        permuted_U = U[:, [1, 0]]

        similarity = (
            stability_module._compute_fuzzy_co_membership_similarity(
                U=U,
                first_cluster_discarded=False,
                perturbed_U=permuted_U,
                perturbed_first_cluster_discarded=False
            )
        )

        self.assertAlmostEqual(similarity, 1.0)

    def test_fuzzy_similarity_discards_first_cluster_independently(self):
        actual_memberships = np.array(
            [
                [1.0, 0.0],
                [0.5, 0.5],
                [0.0, 1.0]
            ]
        )
        U_with_background = np.column_stack(
            [
                np.full(3, 0.2),
                actual_memberships
            ]
        )

        similarity = (
            stability_module._compute_fuzzy_co_membership_similarity(
                U=U_with_background,
                first_cluster_discarded=True,
                perturbed_U=actual_memberships,
                perturbed_first_cluster_discarded=False
            )
        )

        self.assertAlmostEqual(similarity, 1.0)

    def test_fuzzy_similarity_returns_none_without_usable_clusters(self):
        U = np.ones((3, 1))

        self.assertIsNone(
            stability_module._compute_fuzzy_co_membership_similarity(
                U=U,
                first_cluster_discarded=True,
                perturbed_U=np.ones((3, 2)),
                perturbed_first_cluster_discarded=False
            )
        )

    def test_fuzzy_similarity_returns_none_for_zero_norm(self):
        zero_U = np.zeros((3, 2))

        self.assertIsNone(
            stability_module._compute_fuzzy_co_membership_similarity(
                U=zero_U,
                first_cluster_discarded=False,
                perturbed_U=zero_U.copy(),
                perturbed_first_cluster_discarded=False
            )
        )

    def test_stability_evaluation_fieldnames_and_to_dict(self):
        evaluation = StabilityEvaluation(
            number_of_perturbed_graphs=4,
            number_of_valid_similarities=2,
            similarities=[1.0, 0.5],
            stability=0.375
        )

        self.assertEqual(
            StabilityEvaluation.fieldnames(),
            [
                "#Perturbed Graphs",
                "#Valid Similarities",
                "Similarities",
                "Stability",
                "Acceptable Stability?"
            ]
        )
        self.assertEqual(
            evaluation.to_dict(),
            {
                "#Perturbed Graphs": 4,
                "#Valid Similarities": 2,
                "Similarities": [1.0, 0.5],
                "Stability": 0.375,
                "Acceptable Stability?": None
            }
        )


if __name__ == "__main__":
    unittest.main()
