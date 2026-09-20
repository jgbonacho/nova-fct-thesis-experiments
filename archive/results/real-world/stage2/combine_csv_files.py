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

def select_csv_columns(
        root_dir: str,
        input_filename: str,
        output_filename: str,
        columns: list[str]
) -> None:
    root_path = Path(root_dir)
    input_path = root_path / input_filename
    output_path = root_path / output_filename

    if not input_path.exists():
        return

    with open(input_path, mode="r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)

        available_columns = [
            column
            for column in columns
            if column in (reader.fieldnames or [])
        ]

        if not available_columns:
            return

        with open(output_path, mode="w", newline="", encoding="utf-8") as output_file:
            writer = csv.DictWriter(
                output_file,
                fieldnames=available_columns
            )
            writer.writeheader()

            for row in reader:
                writer.writerow({
                    column: row[column]
                    for column in available_columns
                })

if __name__ == "__main__":

    TRAINING_NETWORKS_DIR = "training_networks"

    VALIDATION_NETWORKS_WITH_GT_DIR = "validation_networks_with_gt"
    VALIDATION_NETWORKS_WITHOUT_GT_DIR = "validation_networks_without_gt"

    TEST_NETWORKS_WITHOUT_GT_DIR = "test_networks_without_gt"
    TEST_NETWORKS_WITH_GT_DIR = "test_networks_with_gt"


    SUMMARY_FILENAME = "_summary.csv"
    COMBINE_SUMMARY_FILENAME = "_combine_summary.csv"
    COMBINE_THRESHOLDS_FILENAME = "_combine_threshold_details.csv"

    RESULTS_FILENAME = "_combine_results.csv"
    RESULTS_COLUMNS = [
        "Network",
        "Name",
        "Value",
        "K'",
        "Singleton/Near-Singleton Fraction",
        "Largest-Community Fraction",
        "Modularity",
        "Conductance",
        "Runtime",
        "Stability",
        "Acceptable Null Model?",
        "Acceptable?",
        "K' | K",
        "|K'-K|/K",
        "AMI",
        "F-measure",
        "ARI",
        "FMI",
        "NMI",
        "VI",
        "ONMI",
        "Omega"
    ]

    for base_dir in [
        os.path.join("experience2", "ths", "results_2026-07-21_01-35-02-985213"),
        os.path.join("experience2", "ths", "results_2026-07-21_03-15-17-101707"),
        os.path.join("experience2", "ths", "results_2026-07-21_05-19-39-556936"),
        os.path.join("experience2", "ths", "results_2026-07-21_20-05-55-517321"),
        os.path.join("experience2", "ths", "results_2026-07-21_21-23-40-813696"),
        os.path.join("experience2", "ths", "results_2026-07-22_04-16-41-275586"),
        os.path.join("experience2", "ths", "results_2026-07-22_12-45-13-205463"),
        os.path.join("experience2", "ths", "results_2026-07-24_08-27-39-974371"),  
        os.path.join("experience2", "ths", "results_2026-07-24_09-52-38-785445"),
        os.path.join("experience2", "ths", "results_2026-07-24_15-32-47-785178"),
        os.path.join("experience2", "ths", "results_2026-07-25_15-40-23-273023"),
        os.path.join("experience2", "ths", "results_2026-07-25_20-55-04-450298"),
        os.path.join("experience2", "ths", "results_2026-07-26_07-21-37-879275"),
        os.path.join("experience2", "ths", "results_2026-07-26_15-04-51-954365")
    ]:

        combine_csv_files(
            root_dir=os.path.join(base_dir, VALIDATION_NETWORKS_WITHOUT_GT_DIR),
            input_filename=SUMMARY_FILENAME,
            output_filename=COMBINE_SUMMARY_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, VALIDATION_NETWORKS_WITHOUT_GT_DIR),
            input_filename="07_threshold.csv",
            output_filename=COMBINE_THRESHOLDS_FILENAME
        )

        select_csv_columns(
            root_dir=os.path.join(base_dir, VALIDATION_NETWORKS_WITHOUT_GT_DIR),
            input_filename=COMBINE_THRESHOLDS_FILENAME,
            output_filename=RESULTS_FILENAME,
            columns=RESULTS_COLUMNS
        )


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

        select_csv_columns(
            root_dir=os.path.join(base_dir, TEST_NETWORKS_WITHOUT_GT_DIR),
            input_filename=COMBINE_THRESHOLDS_FILENAME,
            output_filename=RESULTS_FILENAME,
            columns=RESULTS_COLUMNS
        )


        combine_csv_files(
            root_dir=os.path.join(base_dir, VALIDATION_NETWORKS_WITH_GT_DIR),
            input_filename="_summary.csv",
            output_filename=COMBINE_SUMMARY_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, VALIDATION_NETWORKS_WITH_GT_DIR),
            input_filename="08_extrinsic_evaluation.csv",
            output_filename=COMBINE_THRESHOLDS_FILENAME,
            concatenate_columns=True
        )

        select_csv_columns(
            root_dir=os.path.join(base_dir, VALIDATION_NETWORKS_WITH_GT_DIR),
            input_filename=COMBINE_THRESHOLDS_FILENAME,
            output_filename=RESULTS_FILENAME,
            columns=RESULTS_COLUMNS
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

        select_csv_columns(
            root_dir=os.path.join(base_dir, TEST_NETWORKS_WITH_GT_DIR),
            input_filename=COMBINE_THRESHOLDS_FILENAME,
            output_filename=RESULTS_FILENAME,
            columns=RESULTS_COLUMNS
        )


        combine_csv_files(
            root_dir=os.path.join(base_dir, TRAINING_NETWORKS_DIR),
            input_filename="_summary.csv",
            output_filename=COMBINE_SUMMARY_FILENAME
        )

        combine_csv_files(
            root_dir=os.path.join(base_dir, TRAINING_NETWORKS_DIR),
            input_filename="08_extrinsic_evaluation.csv",
            output_filename=COMBINE_THRESHOLDS_FILENAME,
            concatenate_columns=True
        )

        select_csv_columns(
            root_dir=os.path.join(base_dir, TRAINING_NETWORKS_DIR),
            input_filename=COMBINE_THRESHOLDS_FILENAME,
            output_filename=RESULTS_FILENAME,
            columns=RESULTS_COLUMNS
        )


# if __name__ == "__main__":

#     TEST_NETWORKS_WITHOUT_GT_DIR = "test_networks_without_gt"
#     TEST_NETWORKS_WITH_GT_DIR = "test_networks_with_gt"
#     TEST_WITH_TRAIN_NETWORKS_DIR = "test_with_train_networks"

#     SUMMARY_FILENAME = "_summary.csv"

#     COMBINE_SUMMARY_FILENAME = "_combine_summary.csv"
#     COMBINE_THRESHOLDS_FILENAME = "_combine_threshold_details.csv"

#     RESULTS_FILENAME = "_combine_results.csv"

#     RESULTS_COLUMNS = [
#         "Network",
#         "Name",
#         "Value",
#         "K'",
#         "Singleton/Near-Singleton Fraction",
#         "Largest-Community Fraction",
#         "Modularity",
#         "Conductance",
#         "Runtime",
#         "Stability",
#         "Acceptable Null Model?",
#         "Acceptable?",
#         "K' | K",
#         "|K'-K|/K",
#         "AMI",
#         "F-measure",
#         "ARI",
#         "FMI",
#         "NMI",
#         "VI",
#         "ONMI",
#         "Omega"
#     ]

#     for base_dir in [
#         os.path.join("experience1", "v1", "results_2026-07-12_23-54-12-394620"),
#         os.path.join("experience1", "v1", "results_2026-07-14_00-00-52-195086"),
#         os.path.join("experience1", "v1", "results_2026-07-14_10-55-24-787794"),
#         os.path.join("experience1", "v2", "results_2026-07-14_18-35-00-623858"),
#         os.path.join("experience1", "v2", "results_2026-07-14_23-45-56-297136"),
#         os.path.join("experience1", "v2", "results_2026-07-15_04-19-17-796221")
#     ]:

#         combine_csv_files(
#             root_dir=os.path.join(base_dir, TEST_NETWORKS_WITHOUT_GT_DIR),
#             input_filename=SUMMARY_FILENAME,
#             output_filename=COMBINE_SUMMARY_FILENAME
#         )

#         combine_csv_files(
#             root_dir=os.path.join(base_dir, TEST_NETWORKS_WITHOUT_GT_DIR),
#             input_filename="07_threshold.csv",
#             output_filename=COMBINE_THRESHOLDS_FILENAME
#         )

#         select_csv_columns(
#             root_dir=os.path.join(base_dir, TEST_NETWORKS_WITHOUT_GT_DIR),
#             input_filename=COMBINE_THRESHOLDS_FILENAME,
#             output_filename=RESULTS_FILENAME,
#             columns=RESULTS_COLUMNS
#         )

#         combine_csv_files(
#             root_dir=os.path.join(base_dir, TEST_NETWORKS_WITH_GT_DIR),
#             input_filename="_summary.csv",
#             output_filename=COMBINE_SUMMARY_FILENAME
#         )

#         combine_csv_files(
#             root_dir=os.path.join(base_dir, TEST_NETWORKS_WITH_GT_DIR),
#             input_filename="08_extrinsic_evaluation.csv",
#             output_filename=COMBINE_THRESHOLDS_FILENAME,
#             concatenate_columns=True
#         )

#         select_csv_columns(
#             root_dir=os.path.join(base_dir, TEST_NETWORKS_WITH_GT_DIR),
#             input_filename=COMBINE_THRESHOLDS_FILENAME,
#             output_filename=RESULTS_FILENAME,
#             columns=RESULTS_COLUMNS
#         )

#         combine_csv_files(
#             root_dir=os.path.join(base_dir, TEST_WITH_TRAIN_NETWORKS_DIR),
#             input_filename="_summary.csv",
#             output_filename=COMBINE_SUMMARY_FILENAME
#         )

#         combine_csv_files(
#             root_dir=os.path.join(base_dir, TEST_WITH_TRAIN_NETWORKS_DIR),
#             input_filename="08_extrinsic_evaluation.csv",
#             output_filename=COMBINE_THRESHOLDS_FILENAME,
#             concatenate_columns=True
#         )

#         select_csv_columns(
#             root_dir=os.path.join(base_dir, TEST_WITH_TRAIN_NETWORKS_DIR),
#             input_filename=COMBINE_THRESHOLDS_FILENAME,
#             output_filename=RESULTS_FILENAME,
#             columns=RESULTS_COLUMNS
#         )
