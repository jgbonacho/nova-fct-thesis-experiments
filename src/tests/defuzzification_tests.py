import unittest

import numpy as np

from experiments.defuzzification.defuzzification import apply_defuzzification_rule


class Test(unittest.TestCase):

    def test_maximum_membership_assignment_1(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.0, 0.5, 0.5]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=None, conditionally_discard_first_cluster=True, overlapping=False
        )

        self.assertFalse(first_cluster_discarded, "First cluster should not be discarded.")
        self.assertEqual(predicted_labels, [2, 0, 1, 1], "Predicted labels should be [2, 0, 1, 1].")

    def test_maximum_membership_assignment_2(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.5, 0.4]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=None, conditionally_discard_first_cluster=True, overlapping=False,
        )

        self.assertTrue(first_cluster_discarded, "First cluster should be discarded.")
        self.assertEqual(predicted_labels, [2, 1, 1, 1], "Predicted labels should be [2, 1, 1, 1].")

    def test_node_wise_alpha_cut_thresholding_1(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.0, 0.5, 0.5]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=0.5, conditionally_discard_first_cluster=True, overlapping=True
        )

        self.assertFalse(first_cluster_discarded, "First cluster should not be discarded.")
        print(predicted_labels)

    def test_node_wise_alpha_cut_thresholding_2(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.5, 0.4]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=0.5, conditionally_discard_first_cluster=True, overlapping=True
        )

        self.assertTrue(first_cluster_discarded, "First cluster should be discarded.")
        print(predicted_labels)

    def test_node_wise_alpha_cut_thresholding_3(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.0, 0.5, 0.5]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=0.3, conditionally_discard_first_cluster=True, overlapping=True
        )

        self.assertFalse(first_cluster_discarded, "First cluster should not be discarded.")
        print(predicted_labels)

    def test_node_wise_alpha_cut_thresholding_4(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.5, 0.4]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=0.3, conditionally_discard_first_cluster=True, overlapping=True
        )

        self.assertTrue(first_cluster_discarded, "First cluster should be discarded.")
        print(predicted_labels)

    def test_node_wise_alpha_cut_thresholding_5(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.0, 0.5, 0.5]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=0.7, conditionally_discard_first_cluster=True, overlapping=True
        )

        self.assertFalse(first_cluster_discarded, "First cluster should not be discarded.")
        print(predicted_labels)

    def test_node_wise_alpha_cut_thresholding_6(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.5, 0.4]])

        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
            U, gamma=0.7, conditionally_discard_first_cluster=True, overlapping=True
        )

        self.assertTrue(first_cluster_discarded, "First cluster should be discarded.")
        print(predicted_labels)

    def test_invalid_gamma(self):
        U = np.array([[0.1, 0.1, 0.8], [0.8, 0.1, 0.1], [0.2, 0.6, 0.2], [0.1, 0.5, 0.4]])

        self.assertRaises(
            ValueError,
            apply_defuzzification_rule, U, gamma=-0.5, conditionally_discard_first_cluster=True, overlapping=True
        )
        self.assertRaises(
            ValueError,
            apply_defuzzification_rule, U, gamma=1.5, conditionally_discard_first_cluster=True, overlapping=True
        )


if __name__ == "__main__":
    unittest.main()
