import os
import unittest
from datetime import datetime
from tempfile import TemporaryDirectory
from unittest.mock import patch

from experiments.scripts.utils.utils import create_dir, create_results_dir, log_progress


class TestUtils(unittest.TestCase):

    @patch("experiments.scripts.utils.utils.datetime")
    def test_create_results_dir(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime(2026, 7, 21, 12, 30, 45, 123456)

        with TemporaryDirectory() as temporary_dir:
            base_dir = os.path.join(temporary_dir, "results")

            results_dir = create_results_dir(base_dir)

            expected_results_dir = os.path.join(
                base_dir,
                "results_2026-07-21_12-30-45-123456"
            )

            self.assertEqual(results_dir, expected_results_dir)
            self.assertTrue(os.path.isdir(base_dir))
            self.assertTrue(os.path.isdir(results_dir))

    @patch("experiments.scripts.utils.utils.datetime")
    def test_create_results_dir_with_existing_base_directory(self, mocked_datetime):
        mocked_datetime.now.return_value = datetime(2026, 7, 21, 12, 30, 45, 123456)

        with TemporaryDirectory() as temporary_dir:
            base_dir = os.path.join(temporary_dir, "results")
            os.makedirs(base_dir)

            results_dir = create_results_dir(base_dir)

            self.assertTrue(os.path.isdir(results_dir))

    def test_create_dir(self):
        with TemporaryDirectory() as temporary_dir:
            path = os.path.join(temporary_dir, "level_1", "level_2")

            returned_path = create_dir(path)

            self.assertEqual(returned_path, path)
            self.assertTrue(os.path.isdir(path))

    def test_create_dir_when_directory_already_exists(self):
        with TemporaryDirectory() as temporary_dir:
            path = os.path.join(temporary_dir, "results")
            os.makedirs(path)

            returned_path = create_dir(path)

            self.assertEqual(returned_path, path)
            self.assertTrue(os.path.isdir(path))

    @patch("builtins.print")
    def test_log_progress(self, mocked_print):
        result = log_progress(
            current_step=2,
            total_steps=5,
            item_label="network",
            indent_level=3
        )

        self.assertIsNone(result)
        mocked_print.assert_called_once_with("### [2/5] 'network'")

    @patch("builtins.print")
    def test_log_progress_with_empty_line(self, mocked_print):
        log_progress(
            current_step=1,
            total_steps=3,
            item_label="family",
            indent_level=2,
            empty_line=True
        )

        mocked_print.assert_called_once_with("\n## [1/3] 'family'")


if __name__ == "__main__":
    unittest.main()
