import csv
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from experiments.scripts.lfr_networks.thresholds.bootstrap_and_mse_selection.bootstrap_and_mse import \
    _bootstrapping, _compute_candidate_thresholds, _get_contributions, \
    _load_candidate_thresholds, _load_network_contributions, _normalize_contributions


class TestBootstrapAndMSE(unittest.TestCase):

    @staticmethod
    def _write_csv(path: str, rows: list[list]) -> None:
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerows(rows)

    def test_load_candidate_thresholds(self):
        with TemporaryDirectory() as temporary_dir:
            self._write_csv(
                os.path.join(temporary_dir, "candidate_thresholds.csv"),
                [
                    ["Network Family", "Mean", "Median"],
                    ["family_a", 0.1, 0.2],
                    ["family_b", 0.3, 0.4]
                ]
            )

            thresholds = _load_candidate_thresholds(
                results_dir=temporary_dir,
                input_filename="candidate_thresholds.csv",
                threshold_metrics=("Mean", "Median")
            )

        self.assertEqual(
            thresholds,
            {
                "family_a": {"Mean": 0.1, "Median": 0.2},
                "family_b": {"Mean": 0.3, "Median": 0.4}
            }
        )

    def test_load_network_contributions(self):
        with TemporaryDirectory() as temporary_dir:
            self._write_csv(
                os.path.join(temporary_dir, "raw.csv"),
                [
                    ["Network", "K", "c1", "c2", "c3"],
                    ["network_a", 2, 0.1, 0.2, 0.3],
                    ["network_b", 3, 0.4, 0.5]
                ]
            )

            contributions = _load_network_contributions(
                results_dir=Path(temporary_dir),
                input_filename="raw.csv"
            )

        self.assertEqual(
            contributions,
            [
                [0.1, 0.2, 0.3],
                [0.4, 0.5]
            ]
        )

    def test_bootstrapping_is_reproducible(self):
        first_sample = _bootstrapping(
            number_of_networks=5,
            with_replacement=True,
            sample_size=8,
            random_seed=7
        )
        second_sample = _bootstrapping(
            number_of_networks=5,
            with_replacement=True,
            sample_size=8,
            random_seed=7
        )

        self.assertEqual(first_sample, second_sample)
        self.assertEqual(len(first_sample), 8)
        self.assertTrue(all(0 <= index < 5 for index in first_sample))

    def test_bootstrapping_without_replacement(self):
        sampled_indices = _bootstrapping(
            number_of_networks=5,
            with_replacement=False,
            sample_size=3,
            random_seed=3
        )

        self.assertEqual(len(sampled_indices), 3)
        self.assertEqual(len(set(sampled_indices)), 3)

    def test_get_contributions(self):
        contributions = _get_contributions(
            network_contributions=[
                [0.1, 0.2],
                [0.3],
                [0.4, 0.5]
            ],
            selected_indices=[2, 0, 2]
        )

        self.assertEqual(
            contributions,
            [0.4, 0.5, 0.1, 0.2, 0.4, 0.5]
        )

    def test_normalize_contributions(self):
        contributions = [1.0, 2.0, 3.0]
        original_contributions = contributions.copy()

        normalized_contributions = _normalize_contributions(contributions)

        self.assertEqual(contributions, original_contributions)
        self.assertAlmostEqual(sum(normalized_contributions), 1.0)
        self.assertEqual(normalized_contributions, [1 / 6, 2 / 6, 3 / 6])

    def test_compute_candidate_thresholds(self):
        thresholds = _compute_candidate_thresholds(
            normalized_values=[0.1, 0.2, 0.3, 0.4],
            threshold_metrics=("Mean", "Median", "75%", "90%", "95%")
        )

        self.assertAlmostEqual(thresholds["Mean"], 0.25)
        self.assertAlmostEqual(thresholds["Median"], 0.25)
        self.assertAlmostEqual(thresholds["75%"], 0.325)
        self.assertAlmostEqual(thresholds["90%"], 0.37)
        self.assertAlmostEqual(thresholds["95%"], 0.385)


if __name__ == "__main__":
    unittest.main()
