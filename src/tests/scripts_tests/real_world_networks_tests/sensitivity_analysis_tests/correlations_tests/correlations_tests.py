import csv
import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from experiments.scripts.real_world_networks.sensitivity_analysis.correlations.correlations import \
    _load_network_properties, _load_valid_contributions_at_k, _parse_optional_float, \
    _pearson_correlation, _rank_values, _spearman_correlation, \
    perform_faddis_sensitivity_analysis


class TestCorrelations(unittest.TestCase):

    @staticmethod
    def _write_csv(path: str, rows: list[list]) -> None:
        with open(path, mode="w", newline="", encoding="utf-8") as file:
            csv.writer(file).writerows(rows)

    def test_load_network_properties(self):
        with TemporaryDirectory() as temporary_dir:
            input_path = os.path.join(temporary_dir, "network_properties.csv")
            self._write_csv(
                input_path,
                [
                    ["Network", "Density", "Ground-Truth?"],
                    ["network_b", "0.2", "True"],
                    ["network_a", "0.1", "False"]
                ]
            )

            properties = _load_network_properties(input_path)

        self.assertEqual(
            properties,
            {
                "network_b": {
                    "Network": "network_b",
                    "Density": "0.2",
                    "Ground-Truth?": "True"
                },
                "network_a": {
                    "Network": "network_a",
                    "Density": "0.1",
                    "Ground-Truth?": "False"
                }
            }
        )

    def test_load_valid_contributions_at_k_with_lapin(self):
        with TemporaryDirectory() as temporary_dir:
            family_dir = Path(temporary_dir, "family_01")
            family_dir.mkdir()

            self._write_csv(
                str(family_dir / "raw_contributions.csv"),
                [
                    ["Network", "K", "Stop Condition", "c1", "c2", "c3"],
                    ["network_a", 2, "desiredK", 0.6, 0.3, 0.1],
                    ["network_b", 1, "desiredK", 0.7, 0.2, 0.1]
                ]
            )

            contributions = _load_valid_contributions_at_k(
                results_dir=temporary_dir,
                raw_contributions_input_filename="raw_contributions.csv",
                raw_contributions_input_fieldnames=[
                    "Network",
                    "K",
                    "Stop Condition"
                ],
                apply_lapin=True
            )

        self.assertEqual(
            contributions,
            {
                "network_a": 0.3,
                "network_b": 0.7
            }
        )

    def test_load_valid_contributions_at_k_without_lapin(self):
        with TemporaryDirectory() as temporary_dir:
            family_dir = Path(temporary_dir, "family_01")
            family_dir.mkdir()

            self._write_csv(
                str(family_dir / "raw_contributions.csv"),
                [
                    ["Network", "K", "Stop Condition", "c1", "c2", "c3", "c4"],
                    ["network_a", 2, "desiredK", 0.5, 0.25, 0.15, 0.10],
                    ["network_b", 1, "desiredK", 0.6, 0.3, 0.1, ""]
                ]
            )

            contributions = _load_valid_contributions_at_k(
                results_dir=temporary_dir,
                raw_contributions_input_filename="raw_contributions.csv",
                raw_contributions_input_fieldnames=[
                    "Network",
                    "K",
                    "Stop Condition"
                ],
                apply_lapin=False
            )

        self.assertEqual(
            contributions,
            {
                "network_a": 0.15,
                "network_b": 0.3
            }
        )

    def test_load_valid_contributions_skips_missing_files_and_short_rows(self):
        with TemporaryDirectory() as temporary_dir:
            missing_file_family = Path(temporary_dir, "family_01")
            missing_file_family.mkdir()

            valid_family = Path(temporary_dir, "family_02")
            valid_family.mkdir()
            self._write_csv(
                str(valid_family / "raw_contributions.csv"),
                [
                    ["Network", "K", "Stop Condition", "c1"],
                    ["network_a", 3, "kMax", 0.5]
                ]
            )

            contributions = _load_valid_contributions_at_k(
                results_dir=temporary_dir,
                raw_contributions_input_filename="raw_contributions.csv",
                raw_contributions_input_fieldnames=[
                    "Network",
                    "K",
                    "Stop Condition"
                ],
                apply_lapin=True
            )

        self.assertEqual(contributions, {})

    def test_parse_optional_float(self):
        self.assertEqual(_parse_optional_float("1.25"), 1.25)
        self.assertEqual(_parse_optional_float(2), 2.0)

        for value in (None, "", "invalid", "nan", "inf", "-inf"):
            with self.subTest(value=value):
                self.assertIsNone(_parse_optional_float(value))

    def test_pearson_correlation(self):
        self.assertAlmostEqual(
            _pearson_correlation([1, 2, 3], [2, 4, 6]),
            1.0
        )
        self.assertAlmostEqual(
            _pearson_correlation([1, 2, 3], [6, 4, 2]),
            -1.0
        )
        self.assertIsNone(
            _pearson_correlation([1, 1, 1], [1, 2, 3])
        )
        self.assertIsNone(
            _pearson_correlation([1, 2, 3], [5, 5, 5])
        )

    def test_rank_values_with_ties(self):
        self.assertEqual(
            _rank_values([30, 10, 20, 20]),
            [4.0, 1.0, 2.5, 2.5]
        )

    def test_spearman_correlation_with_ties(self):
        correlation = _spearman_correlation(
            [1, 2, 2, 4],
            [10, 20, 20, 40]
        )

        self.assertAlmostEqual(correlation, 1.0)

    def test_analysis_skips_invalid_or_insufficient_properties(self):
        with TemporaryDirectory() as temporary_dir:
            self._write_csv(
                os.path.join(temporary_dir, "network_properties.csv"),
                [
                    [
                        "Network",
                        "Density",
                        "Average Degree",
                        "Ground-Truth?",
                        "Overlapping Ground-Truth?"
                    ],
                    ["n1", 1, "", True, False],
                    ["n2", 2, "invalid", True, False],
                    ["n3", 3, "nan", True, False]
                ]
            )

            family_dir = Path(temporary_dir, "family_01")
            family_dir.mkdir()
            self._write_csv(
                str(family_dir / "raw_contributions.csv"),
                [
                    ["Network", "K", "Stop Condition", "c1"],
                    ["n1", 1, "desiredK", 1],
                    ["n2", 1, "desiredK", 2]
                ]
            )

            perform_faddis_sensitivity_analysis(
                results_dir=temporary_dir,
                network_properties_input_filename="network_properties.csv",
                network_properties_input_fieldnames=[
                    "Network",
                    "Density",
                    "Average Degree",
                    "Ground-Truth?",
                    "Overlapping Ground-Truth?"
                ],
                raw_contributions_input_filename="raw_contributions.csv",
                raw_contributions_input_fieldnames=[
                    "Network",
                    "K",
                    "Stop Condition"
                ],
                output_filename="correlations.csv",
                output_fieldnames=[
                    "Ground-Truth Type",
                    "Network Property",
                    "FADDIS Property",
                    "#Networks",
                    "Spearman Correlation",
                    "Pearson Correlation"
                ],
                apply_lapin=True
            )

            with open(
                    os.path.join(temporary_dir, "correlations.csv"),
                    mode="r",
                    newline="",
                    encoding="utf-8"
            ) as file:
                rows = list(csv.DictReader(file))

        self.assertEqual(rows, [])


if __name__ == "__main__":
    unittest.main()
