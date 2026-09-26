import unittest
from unittest.mock import patch

import numpy as np

from experiments.scripts.real_world_networks.utils.affinity_designs import \
    affinity_design_dataclass as affinity_design_module
from experiments.scripts.real_world_networks.utils.affinity_designs.affinity_design_dataclass import \
    AffinityDesign


class TestAffinityDesign(unittest.TestCase):

    def setUp(self):
        self.A = np.array(
            [[0.0, 1.0],
             [1.0, 0.0]]
        )

    def test_default_returns_copy_of_adjacency_matrix(self):
        W = AffinityDesign.DEFAULT.apply_affinity_design(self.A)

        np.testing.assert_array_equal(W, self.A)
        self.assertIsNot(W, self.A)

        W[0, 1] = 0.0
        self.assertEqual(self.A[0, 1], 1.0)

    def test_binary_set_affinity_design_dispatch(self):
        cases = [
            (AffinityDesign.KUL, "compute_kul"),
            (AffinityDesign.DICE, "compute_dice"),
            (AffinityDesign.OCHIAI, "compute_ochiai")
        ]

        for affinity_design, function_name in cases:
            with self.subTest(affinity_design=affinity_design):
                expected_W = np.full((2, 2), 0.5)

                with patch.object(
                        affinity_design_module,
                        function_name,
                        return_value=expected_W
                ) as mocked_function:
                    W = affinity_design.apply_affinity_design(self.A)

                mocked_function.assert_called_once_with(self.A)
                self.assertIs(W, expected_W)

    def test_weighted_inner_product_affinity_design_dispatch(self):
        cases = [
            (AffinityDesign.IP_B0, 0),
            (AffinityDesign.IP_B0_5, 0.5),
            (AffinityDesign.IP_B1, 1)
        ]

        for affinity_design, expected_beta in cases:
            with self.subTest(affinity_design=affinity_design):
                expected_W = np.full((2, 2), expected_beta)

                with patch.object(
                        affinity_design_module,
                        "compute_ip",
                        return_value=expected_W
                ) as mocked_compute_ip:
                    W = affinity_design.apply_affinity_design(self.A)

                mocked_compute_ip.assert_called_once_with(
                    self.A,
                    beta=expected_beta
                )
                self.assertIs(W, expected_W)

    def test_cosine_weighted_inner_product_affinity_design_dispatch(self):
        cases = [
            (AffinityDesign.COSIP_B0, 0),
            (AffinityDesign.COSIP_B0_5, 0.5),
            (AffinityDesign.COSIP_B1, 1)
        ]

        for affinity_design, expected_beta in cases:
            with self.subTest(affinity_design=affinity_design):
                expected_W = np.full((2, 2), expected_beta)

                with patch.object(
                        affinity_design_module,
                        "compute_cosip",
                        return_value=expected_W
                ) as mocked_compute_cosip:
                    W = affinity_design.apply_affinity_design(self.A)

                mocked_compute_cosip.assert_called_once_with(
                    self.A,
                    beta=expected_beta
                )
                self.assertIs(W, expected_W)

    def test_enum_values(self):
        self.assertEqual(AffinityDesign.DEFAULT.value, "Default")
        self.assertEqual(AffinityDesign.KUL.value, "Kul")
        self.assertEqual(AffinityDesign.IP_B0_5.value, "Ip_b0.5")
        self.assertEqual(AffinityDesign.COSIP_B1.value, "CosIp_b1")

    def test_invalid_affinity_design_value(self):
        with self.assertRaises(ValueError):
            AffinityDesign("Unknown")


if __name__ == "__main__":
    unittest.main()
