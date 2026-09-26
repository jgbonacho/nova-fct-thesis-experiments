import json
import math
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace

from experiments.scripts.lfr_networks.thresholds.utils.utils import \
    _percentile, compute_statistics, get_family_dirs, save_experiment_report


class TestLFRUtils(unittest.TestCase):

    def test_get_family_dirs(self):
        with TemporaryDirectory() as temporary_dir:
            os.makedirs(os.path.join(temporary_dir, "family_b"))
            os.makedirs(os.path.join(temporary_dir, "family_a"))
            Path(temporary_dir, "file.txt").write_text("content", encoding="utf-8")

            family_dirs = get_family_dirs(temporary_dir)

        self.assertEqual(
            [directory.name for directory in family_dirs],
            ["family_a", "family_b"]
        )
        self.assertTrue(all(isinstance(directory, Path) for directory in family_dirs))

    def test_get_family_dirs_when_no_directories_exist(self):
        with TemporaryDirectory() as temporary_dir:
            Path(temporary_dir, "file.txt").write_text("content", encoding="utf-8")

            family_dirs = get_family_dirs(temporary_dir)

        self.assertEqual(family_dirs, [])

    def test_compute_statistics(self):
        normalized_values = [4.0, 1.0, 3.0, 2.0]
        original_values = normalized_values.copy()

        statistics = compute_statistics(normalized_values)

        expected_statistics = (
            2.5,
            math.sqrt(5 / 3),
            2.5,
            3.25,
            3.7,
            3.85,
            1.0,
            4.0
        )

        for actual, expected in zip(statistics, expected_statistics):
            self.assertAlmostEqual(actual, expected)

        self.assertEqual(normalized_values, original_values)

    def test_compute_statistics_with_odd_number_of_values(self):
        statistics = compute_statistics([3.0, 1.0, 2.0])

        self.assertAlmostEqual(statistics[0], 2.0)
        self.assertAlmostEqual(statistics[1], 1.0)
        self.assertAlmostEqual(statistics[2], 2.0)
        self.assertAlmostEqual(statistics[6], 1.0)
        self.assertAlmostEqual(statistics[7], 3.0)

    def test_percentile_without_interpolation(self):
        sorted_values = [1.0, 2.0, 3.0, 4.0, 5.0]

        self.assertEqual(_percentile(sorted_values, 0.0), 1.0)
        self.assertEqual(_percentile(sorted_values, 0.5), 3.0)
        self.assertEqual(_percentile(sorted_values, 1.0), 5.0)

    def test_percentile_with_linear_interpolation(self):
        sorted_values = [1.0, 2.0, 3.0, 4.0]

        self.assertAlmostEqual(_percentile(sorted_values, 0.25), 1.75)
        self.assertAlmostEqual(_percentile(sorted_values, 0.75), 3.25)

    def test_save_experiment_report(self):
        config = SimpleNamespace(
            apply_lapin=True,
            use_desired_k=False,
            bootstrapping_maximum_number_of_repetitions=1000,
            bootstrapping_subsample_fraction=0.8
        )
        network_family_dirs = [
            Path("/networks/family_01"),
            Path("/networks/family_02")
        ]

        with TemporaryDirectory() as temporary_dir:
            save_experiment_report(
                results_dir=temporary_dir,
                output_filename="report.json",
                config=config,
                network_family_dirs=network_family_dirs,
                execution_elapsed_time=12.5
            )

            output_file = os.path.join(temporary_dir, "report.json")
            self.assertTrue(os.path.isfile(output_file))

            with open(output_file, "r", encoding="utf-8") as file:
                report = json.load(file)

        self.assertEqual(
            report,
            {
                "apply_lapin": True,
                "use_desired_k": False,
                "bootstrapping_maximum_number_of_repetitions": 1000,
                "bootstrapping_subsample_fraction": 0.8,
                "number_of_families": 2,
                "families": ["family_01", "family_02"],
                "execution_elapsed_time_secs": 12.5
            }
        )


if __name__ == "__main__":
    unittest.main()
