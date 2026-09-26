import copy
import unittest
from dataclasses import fields

from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.community_properties.community_properties import \
    compute_community_properties
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.community_properties.community_properties_dataclass import \
    CommunityProperties


class TestCommunityProperties(unittest.TestCase):

    def test_compute_non_overlapping_community_properties(self):
        properties = compute_community_properties(
            number_of_nodes=6,
            predicted_labels=[0, 0, 1, 2, 2, 2],
            overlapping_communities=False,
            near_singleton_boundary=2
        )

        self.assertEqual(properties.number_of_communities, 3)
        self.assertCountEqual(
            properties.community_size_distribution,
            [2, 1, 3]
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_count,
            2
        )
        self.assertAlmostEqual(
            properties.singleton_or_near_singleton_fraction,
            2 / 3
        )
        self.assertAlmostEqual(
            properties.largest_community_fraction,
            3 / 6
        )

    def test_compute_overlapping_community_properties(self):
        properties = compute_community_properties(
            number_of_nodes=5,
            predicted_labels=[
                [0, 1],
                [1],
                [2],
                [0, 2],
                [2]
            ],
            overlapping_communities=True,
            near_singleton_boundary=2
        )

        self.assertEqual(properties.number_of_communities, 3)
        self.assertCountEqual(
            properties.community_size_distribution,
            [2, 2, 3]
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_count,
            2
        )
        self.assertAlmostEqual(
            properties.singleton_or_near_singleton_fraction,
            2 / 3
        )
        self.assertAlmostEqual(
            properties.largest_community_fraction,
            3 / 5
        )

    def test_near_singleton_boundary_is_inclusive(self):
        properties = compute_community_properties(
            number_of_nodes=5,
            predicted_labels=[0, 0, 1, 1, 1],
            overlapping_communities=False,
            near_singleton_boundary=2
        )

        self.assertEqual(
            properties.singleton_or_near_singleton_count,
            1
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_fraction,
            0.5
        )

    def test_single_community(self):
        properties = compute_community_properties(
            number_of_nodes=4,
            predicted_labels=[7, 7, 7, 7],
            overlapping_communities=False,
            near_singleton_boundary=2
        )

        self.assertEqual(properties.number_of_communities, 1)
        self.assertEqual(
            properties.community_size_distribution,
            [4]
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_count,
            0
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_fraction,
            0.0
        )
        self.assertEqual(
            properties.largest_community_fraction,
            1.0
        )

    def test_empty_membership_lists_are_ignored_for_overlapping_communities(self):
        properties = compute_community_properties(
            number_of_nodes=4,
            predicted_labels=[
                [0],
                [],
                [0, 1],
                [1]
            ],
            overlapping_communities=True,
            near_singleton_boundary=2
        )

        self.assertEqual(properties.number_of_communities, 2)
        self.assertCountEqual(
            properties.community_size_distribution,
            [2, 2]
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_count,
            2
        )
        self.assertEqual(
            properties.singleton_or_near_singleton_fraction,
            1.0
        )
        self.assertEqual(
            properties.largest_community_fraction,
            0.5
        )

    def test_compute_community_properties_does_not_modify_labels(self):
        predicted_labels = [
            [0, 1],
            [1],
            [2]
        ]
        original_labels = copy.deepcopy(predicted_labels)

        compute_community_properties(
            number_of_nodes=3,
            predicted_labels=predicted_labels,
            overlapping_communities=True,
            near_singleton_boundary=1
        )

        self.assertEqual(predicted_labels, original_labels)

    def test_community_properties_field_metadata(self):
        self.assertEqual(
            [
                dataclass_field.metadata["label"]
                for dataclass_field in fields(CommunityProperties)
            ],
            [
                "K'",
                "Community Size Distribution",
                "#Singleton/Near-Singleton Communities",
                "Singleton/Near-Singleton Fraction",
                "Largest-Community Fraction"
            ]
        )


if __name__ == "__main__":
    unittest.main()
