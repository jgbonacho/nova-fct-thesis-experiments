import math
import unittest

from experiments.scripts.real_world_networks.utils.ground_truth_properties.ground_truth_properties import \
    compute_ground_truth_properties
from experiments.scripts.real_world_networks.utils.ground_truth_properties.ground_truth_properties_dataclass import \
    GroundTruthProperties


class TestGroundTruthProperties(unittest.TestCase):

    def test_returns_none_without_ground_truth_labels(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=None,
            k=None,
            overlapping_ground_truth=False,
            number_of_nodes=4
        )

        self.assertIsNone(properties)

    def test_compute_non_overlapping_ground_truth_properties(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=[0, 0, 1, 1, 1, -1],
            k=2,
            overlapping_ground_truth=False,
            number_of_nodes=6
        )

        self.assertEqual(properties.network, "network")
        self.assertFalse(properties.overlapping_ground_truth)
        self.assertEqual(properties.overlap_fraction, 0.0)
        self.assertEqual(properties.k, 2)
        self.assertAlmostEqual(properties.community_proportion, 2 / 6)
        self.assertEqual(properties.min_community_size, 2.0)
        self.assertEqual(properties.max_community_size, 3.0)
        self.assertEqual(properties.average_community_size, 2.5)
        self.assertAlmostEqual(properties.community_size_std, math.sqrt(0.5))
        self.assertAlmostEqual(
            properties.community_size_cv,
            math.sqrt(0.5) / 2.5
        )
        self.assertEqual(properties.nodes_without_community, 1)
        self.assertAlmostEqual(
            properties.nodes_fraction_without_community,
            1 / 6
        )

    def test_compute_overlapping_ground_truth_properties(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=[
                [0, 1],
                [1],
                [2, 1],
                [-1],
                [],
                [2, -1]
            ],
            k=3,
            overlapping_ground_truth=True,
            number_of_nodes=6
        )

        self.assertTrue(properties.overlapping_ground_truth)
        self.assertAlmostEqual(properties.overlap_fraction, 0.5)
        self.assertEqual(properties.k, 3)
        self.assertAlmostEqual(properties.community_proportion, 0.5)
        self.assertEqual(properties.min_community_size, 1.0)
        self.assertEqual(properties.max_community_size, 3.0)
        self.assertEqual(properties.average_community_size, 2.0)
        self.assertEqual(properties.community_size_std, 1.0)
        self.assertEqual(properties.community_size_cv, 0.5)
        self.assertEqual(properties.nodes_without_community, 2)
        self.assertAlmostEqual(
            properties.nodes_fraction_without_community,
            2 / 6
        )

    def test_non_overlapping_structure_with_no_labeled_nodes(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=[-1, -1, -1],
            k=0,
            overlapping_ground_truth=False,
            number_of_nodes=3
        )

        self.assertEqual(properties.overlap_fraction, 0.0)
        self.assertEqual(properties.community_proportion, 0.0)
        self.assertIsNone(properties.min_community_size)
        self.assertIsNone(properties.max_community_size)
        self.assertIsNone(properties.average_community_size)
        self.assertIsNone(properties.community_size_std)
        self.assertIsNone(properties.community_size_cv)
        self.assertEqual(properties.nodes_without_community, 3)
        self.assertEqual(properties.nodes_fraction_without_community, 1.0)

    def test_overlapping_structure_with_no_labeled_nodes(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=[[], [-1], [-1, -1]],
            k=0,
            overlapping_ground_truth=True,
            number_of_nodes=3
        )

        self.assertIsNone(properties.overlap_fraction)
        self.assertIsNone(properties.min_community_size)
        self.assertIsNone(properties.max_community_size)
        self.assertIsNone(properties.average_community_size)
        self.assertIsNone(properties.community_size_std)
        self.assertIsNone(properties.community_size_cv)
        self.assertEqual(properties.nodes_without_community, 3)
        self.assertEqual(properties.nodes_fraction_without_community, 1.0)

    def test_single_community_has_zero_size_variation(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=[0, 0, 0],
            k=1,
            overlapping_ground_truth=False,
            number_of_nodes=3
        )

        self.assertEqual(properties.min_community_size, 3.0)
        self.assertEqual(properties.max_community_size, 3.0)
        self.assertEqual(properties.average_community_size, 3.0)
        self.assertEqual(properties.community_size_std, 0.0)
        self.assertEqual(properties.community_size_cv, 0.0)

    def test_headers(self):
        self.assertEqual(
            GroundTruthProperties.headers(),
            [
                "Network",
                "Overlapping Ground-Truth?",
                "Overlap Fraction",
                "K",
                "Community Proportion",
                "Min Community Size",
                "Max Community Size",
                "Average Community Size",
                "Community Size Std",
                "Community Size CV",
                "Nodes Without Community",
                "Nodes Fraction Without Community"
            ]
        )

    def test_to_dict(self):
        properties = GroundTruthProperties(
            network="network",
            overlapping_ground_truth=True,
            overlap_fraction=0.25,
            k=3,
            community_proportion=0.3,
            min_community_size=2.0,
            max_community_size=5.0,
            average_community_size=3.0,
            community_size_std=1.0,
            community_size_cv=1 / 3,
            nodes_without_community=1,
            nodes_fraction_without_community=0.1
        )

        self.assertEqual(
            properties.to_dict(),
            {
                "Network": "network",
                "Overlapping Ground-Truth?": True,
                "Overlap Fraction": 0.25,
                "K": 3,
                "Community Proportion": 0.3,
                "Min Community Size": 2.0,
                "Max Community Size": 5.0,
                "Average Community Size": 3.0,
                "Community Size Std": 1.0,
                "Community Size CV": 1 / 3,
                "Nodes Without Community": 1,
                "Nodes Fraction Without Community": 0.1
            }
        )

    def test_headers_match_to_dict_keys(self):
        properties = compute_ground_truth_properties(
            network_name="network",
            ground_truth_labels=[0, 0, 1],
            k=2,
            overlapping_ground_truth=False,
            number_of_nodes=3
        )

        self.assertEqual(
            list(properties.to_dict().keys()),
            GroundTruthProperties.headers()
        )


if __name__ == "__main__":
    unittest.main()
