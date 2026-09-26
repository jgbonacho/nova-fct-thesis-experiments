import unittest

from experiments.scripts.real_world_networks.utils.network_config_dataclass import NetworkConfig


class TestNetworkConfig(unittest.TestCase):

    def test_from_dict_with_all_fields(self):
        data = {
            "name": "dolphins",
            "gml_filename": "dolphins.gml",
            "ground_truth": True,
            "overlapping_ground_truth": False,
            "ground_truth_attr": "community"
        }

        config = NetworkConfig.from_dict(data)

        self.assertEqual(
            config,
            NetworkConfig(
                name="dolphins",
                gml_filename="dolphins.gml",
                ground_truth=True,
                overlapping_ground_truth=False,
                ground_truth_attr="community"
            )
        )

    def test_from_dict_without_optional_ground_truth_fields(self):
        config = NetworkConfig.from_dict(
            {
                "name": "jazz",
                "gml_filename": "jazz.gml",
                "ground_truth": False
            }
        )

        self.assertEqual(config.name, "jazz")
        self.assertEqual(config.gml_filename, "jazz.gml")
        self.assertFalse(config.ground_truth)
        self.assertIsNone(config.overlapping_ground_truth)
        self.assertIsNone(config.ground_truth_attr)

    def test_from_dict_preserves_explicit_none_values(self):
        config = NetworkConfig.from_dict(
            {
                "name": "network",
                "gml_filename": "network.gml",
                "ground_truth": False,
                "overlapping_ground_truth": None,
                "ground_truth_attr": None
            }
        )

        self.assertIsNone(config.overlapping_ground_truth)
        self.assertIsNone(config.ground_truth_attr)

    def test_from_dict_ignores_additional_fields(self):
        config = NetworkConfig.from_dict(
            {
                "name": "network",
                "gml_filename": "network.gml",
                "ground_truth": True,
                "overlapping_ground_truth": True,
                "ground_truth_attr": "communities",
                "description": "ignored"
            }
        )

        self.assertFalse(hasattr(config, "description"))

    def test_from_dict_requires_name(self):
        with self.assertRaises(KeyError):
            NetworkConfig.from_dict(
                {
                    "gml_filename": "network.gml",
                    "ground_truth": False
                }
            )

    def test_from_dict_requires_gml_filename(self):
        with self.assertRaises(KeyError):
            NetworkConfig.from_dict(
                {
                    "name": "network",
                    "ground_truth": False
                }
            )

    def test_from_dict_requires_ground_truth(self):
        with self.assertRaises(KeyError):
            NetworkConfig.from_dict(
                {
                    "name": "network",
                    "gml_filename": "network.gml"
                }
            )


if __name__ == "__main__":
    unittest.main()
