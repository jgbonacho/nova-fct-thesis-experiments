import csv
import json
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from experiments.scripts.real_world_networks.sensitivity_analysis.utils.utils import \
    append_properties, load_real_world_network_configs, save_experiment_report


class PropertiesStub:

    def __init__(self, values: dict):
        self.values = values

    def to_dict(self) -> dict:
        return self.values.copy()


class TestSensitivityAnalysisUtils(unittest.TestCase):

    def test_load_real_world_network_configs(self):
        network_configs_data = [
            {
                "name": "dolphins",
                "gml_filename": "dolphins",
                "ground_truth": True,
                "overlapping_ground_truth": False,
                "ground_truth_attr": "community"
            },
            {
                "name": "jazz",
                "gml_filename": "jazz",
                "ground_truth": False
            }
        ]

        with TemporaryDirectory() as temporary_dir:
            input_file = Path(temporary_dir, "family.json")
            input_file.write_text(
                json.dumps(network_configs_data),
                encoding="utf-8"
            )

            network_configs = load_real_world_network_configs(
                network_directory=Path(temporary_dir),
                input_filename="family"
            )

        self.assertEqual(len(network_configs), 2)

        self.assertEqual(network_configs[0].name, "dolphins")
        self.assertEqual(network_configs[0].gml_filename, "dolphins")
        self.assertTrue(network_configs[0].ground_truth)
        self.assertFalse(network_configs[0].overlapping_ground_truth)
        self.assertEqual(network_configs[0].ground_truth_attr, "community")

        self.assertEqual(network_configs[1].name, "jazz")
        self.assertEqual(network_configs[1].gml_filename, "jazz")
        self.assertFalse(network_configs[1].ground_truth)
        self.assertIsNone(network_configs[1].overlapping_ground_truth)
        self.assertIsNone(network_configs[1].ground_truth_attr)

    def test_load_real_world_network_configs_from_empty_list(self):
        with TemporaryDirectory() as temporary_dir:
            Path(temporary_dir, "family.json").write_text(
                "[]",
                encoding="utf-8"
            )

            network_configs = load_real_world_network_configs(
                network_directory=Path(temporary_dir),
                input_filename="family"
            )

        self.assertEqual(network_configs, [])

    def test_append_properties_creates_directory_file_header_and_row(self):
        with TemporaryDirectory() as temporary_dir:
            results_dir = os.path.join(
                temporary_dir,
                "nested",
                "results"
            )
            properties = PropertiesStub(
                {
                    "Network": "dolphins",
                    "Nodes": 62
                }
            )

            result = append_properties(
                results_dir=results_dir,
                output_filename="properties.csv",
                output_fieldnames=["Network", "Nodes"],
                properties=properties
            )

            output_file = os.path.join(
                results_dir,
                "properties.csv"
            )
            self.assertTrue(os.path.isfile(output_file))

            with open(
                    output_file,
                    mode="r",
                    newline="",
                    encoding="utf-8"
            ) as file:
                rows = list(csv.reader(file))

        self.assertIsNone(result)
        self.assertEqual(
            rows,
            [
                ["Network", "Nodes"],
                ["dolphins", "62"]
            ]
        )

    def test_append_properties_appends_without_repeating_header(self):
        with TemporaryDirectory() as temporary_dir:
            for network, nodes in [
                ("dolphins", 62),
                ("jazz", 198)
            ]:
                append_properties(
                    results_dir=temporary_dir,
                    output_filename="properties.csv",
                    output_fieldnames=["Network", "Nodes"],
                    properties=PropertiesStub(
                        {
                            "Network": network,
                            "Nodes": nodes
                        }
                    )
                )

            with open(
                    os.path.join(temporary_dir, "properties.csv"),
                    mode="r",
                    newline="",
                    encoding="utf-8"
            ) as file:
                rows = list(csv.reader(file))

        self.assertEqual(
            rows,
            [
                ["Network", "Nodes"],
                ["dolphins", "62"],
                ["jazz", "198"]
            ]
        )

    def test_append_properties_writes_header_to_existing_empty_file(self):
        with TemporaryDirectory() as temporary_dir:
            output_file = Path(temporary_dir, "properties.csv")
            output_file.touch()

            append_properties(
                results_dir=temporary_dir,
                output_filename="properties.csv",
                output_fieldnames=["Network", "Nodes"],
                properties=PropertiesStub(
                    {
                        "Network": "dolphins",
                        "Nodes": 62
                    }
                )
            )

            with open(
                    output_file,
                    mode="r",
                    newline="",
                    encoding="utf-8"
            ) as file:
                rows = list(csv.reader(file))

        self.assertEqual(
            rows,
            [
                ["Network", "Nodes"],
                ["dolphins", "62"]
            ]
        )

    def test_append_properties_rejects_unexpected_dictionary_fields(self):
        with TemporaryDirectory() as temporary_dir:
            with self.assertRaises(ValueError):
                append_properties(
                    results_dir=temporary_dir,
                    output_filename="properties.csv",
                    output_fieldnames=["Network"],
                    properties=PropertiesStub(
                        {
                            "Network": "dolphins",
                            "Unexpected": 10
                        }
                    )
                )

    def test_save_sensitivity_experiment_report(self):
        with TemporaryDirectory() as temporary_dir:
            result = save_experiment_report(
                results_dir=temporary_dir,
                output_filename="report.json",
                execution_elapsed_time=12.5,
                apply_lapin=True
            )

            with open(
                    os.path.join(temporary_dir, "report.json"),
                    mode="r",
                    encoding="utf-8"
            ) as file:
                report = json.load(file)

        self.assertIsNone(result)
        self.assertEqual(
            report,
            {
                "apply_lapin": True,
                "execution_elapsed_time_secs": 12.5
            }
        )

    def test_save_sensitivity_experiment_report_overwrites_existing_file(self):
        with TemporaryDirectory() as temporary_dir:
            output_file = Path(temporary_dir, "report.json")
            output_file.write_text(
                json.dumps({"old": "content"}),
                encoding="utf-8"
            )

            save_experiment_report(
                results_dir=temporary_dir,
                output_filename="report.json",
                execution_elapsed_time=3.0,
                apply_lapin=False
            )

            with open(
                    output_file,
                    mode="r",
                    encoding="utf-8"
            ) as file:
                report = json.load(file)

        self.assertEqual(
            report,
            {
                "apply_lapin": False,
                "execution_elapsed_time_secs": 3.0
            }
        )


if __name__ == "__main__":
    unittest.main()
