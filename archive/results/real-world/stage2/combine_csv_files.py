import csv
import os
from pathlib import Path

def combine_csv_files(
        root_dir: str,
        input_filename: str,
        output_filename: str,
        concatenate_columns: bool = False
) -> None:
    root_path = Path(root_dir)
    output_path = os.path.join(root_path,output_filename)

    csv_paths = sorted(path for path in root_path.rglob(input_filename) if path != output_path)

    if not csv_paths:
        return

    if concatenate_columns:
        fieldnames = []

        for csv_path in csv_paths:
            with open(csv_path, mode="r", newline="", encoding="utf-8") as input_file:
                reader = csv.DictReader(input_file)

                for fieldname in reader.fieldnames or []:
                    if fieldname not in fieldnames:
                        fieldnames.append(fieldname)

        if not fieldnames:
            return

        # Second pass: combine all rows.
        with open(output_path, mode="w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(output_file, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()

            for csv_path in csv_paths:
                with open(csv_path, mode="r", newline="", encoding="utf-8") as input_file:
                    reader = csv.DictReader(input_file)
                    writer.writerows(reader)

    else:
        expected_fieldnames = None

        with open(output_path, mode="w", newline="", encoding="utf-8") as output_file:
            writer = None

            for csv_path in csv_paths:
                with open(csv_path, mode="r", newline="", encoding="utf-8") as input_file:
                    reader = csv.DictReader(input_file)

                    if expected_fieldnames is None:
                        expected_fieldnames = reader.fieldnames

                        if not expected_fieldnames:
                            continue

                        writer = csv.DictWriter(output_file, fieldnames=expected_fieldnames)
                        writer.writeheader()

                    elif reader.fieldnames != expected_fieldnames:
                        raise ValueError(f"[ERROR] Columns in {csv_path} do not match the expected columns: {expected_fieldnames}.")

                    if writer is not None:
                        writer.writerows(reader)

if __name__ == "__main__":

    TEST_NETWORKS_WITHOUT_GT_DIR = "test_networks_without_gt"
    TEST_NETWORKS_WITH_GT_DIR = "test_networks_with_gt"
    TRAIN_NETWORKS_WITH_GT_DIR = "train_networks_with_gt"

    SUMMARY_FILENAME = "_summary.csv"

    COMBINE_SUMMARY_FILENAME = "_combine_summary.csv"
    COMBINE_THRESHOLDS_FILENAME = "_combine_threshold_details.csv"

    for base_dir in [
        os.path.join("experience1", "v1", "results_2026-07-12_23-54-12-394620"),
        os.path.join("experience1", "v1", "results_2026-07-14_00-00-52-195086"),
        os.path.join("experience1", "v1", "results_2026-07-14_10-55-24-787794"),
        os.path.join("experience1", "v2", "results_2026-07-14_18-35-00-623858"),
        os.path.join("experience1", "v2", "results_2026-07-14_23-45-56-297136"),
        os.path.join("experience1", "v2", "results_2026-07-15_04-19-17-796221"),

        os.path.join("experience2", "ths", "results_2026-07-19_12-57-27-555522-old"),
        os.path.join("experience2", "ths", "results_2026-07-19_19-20-08-944343-old"),
        os.path.join("experience2", "ths", "results_2026-07-20_07-28-20-060385-old"),
        os.path.join("experience2", "ths", "results_2026-07-21_01-35-02-985213"),
        os.path.join("experience2", "ths", "results_2026-07-21_05-19-39-556936"),
        os.path.join("experience2", "ths", "results_2026-07-21_20-05-55-517321"),
        os.path.join("experience2", "ths", "results_2026-07-21_21-23-40-813696"),
        os.path.join("experience2", "ths", "results_2026-07-22_04-16-41-275586"),
        os.path.join("experience2", "ths", "results_2026-07-22_07-21-37-879275")
    ]:

        combine_csv_files(
            root_dir=os.path.join(base_dir, TEST_NETWORKS_WITHOUT_GT_DIR),
            input_filename=SUMMARY_FILENAME,
            output_filename=COMBINE_SUMMARY_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, TEST_NETWORKS_WITHOUT_GT_DIR),
            input_filename="07_threshold.csv",
            output_filename=COMBINE_THRESHOLDS_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, TEST_NETWORKS_WITH_GT_DIR),
            input_filename="_summary.csv",
            output_filename=COMBINE_SUMMARY_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, TEST_NETWORKS_WITH_GT_DIR),
            input_filename="08_extrinsic_evaluation.csv",
            output_filename=COMBINE_THRESHOLDS_FILENAME,
            concatenate_columns=True
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, TRAIN_NETWORKS_WITH_GT_DIR),
            input_filename="_summary.csv",
            output_filename=COMBINE_SUMMARY_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, TRAIN_NETWORKS_WITH_GT_DIR),
            input_filename="08_extrinsic_evaluation.csv",
            output_filename=COMBINE_THRESHOLDS_FILENAME,
            concatenate_columns=True
        )
