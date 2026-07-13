import csv
import os
import time
from pathlib import Path

import numpy as np

from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.loaders.adjacency_matrix import compute_adjacency_matrix
from experiments.loaders.real_world_data_loader import load_network_from_gml
from experiments.utils.dataclasses.ground_truth_properties_dataclass import GroundTruthProperties
from experiments.utils.dataclasses.network_properties_dataclass import NetworkProperties
from experiments.utils.utils import create_results_dir, log_progress, create_dir
from experiments.utils.utils_real_world_networks import load_real_world_network_configs, compute_network_properties, \
    compute_ground_truth_properties, append_properties, perform_faddis_sensitivity_analysis, \
    save_sensitivity_experiment_report

ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..')

TRAIN_NETWORKS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'train-with-gt')
TEST_NETWORKS_WITH_GT_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'test-with-gt')
TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world', 'test-without-gt')

RESULTS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'results', 'real-world')
RESULTS_TRAIN_NETWORKS_NAME = "train_networks"
RESULTS_NETWORKS_WITH_GT_NAME = "test_networks_with_gt"
RESULTS_NETWORKS_WITHOUT_GT_NAME = "test_networks_without_gt"

RAW_CONTRIBUTIONS_FILENAME = "raw_contributions.csv"
RAW_CONTRIBUTIONS_FILENAMES = [
    "Network", "K", "Stop Condition"
]

NETWORK_PROPERTIES_FILENAME = "network_properties.csv"
NETWORK_PROPERTIES_FIELDNAMES = NetworkProperties.headers()

GROUND_TRUTH_PROPERTIES_FILENAME = "ground_truth_properties.csv"
GROUND_TRUTH_PROPERTIES_FIELDNAMES = GroundTruthProperties.headers()

FADDIS_SENSITIVITY_ANALYSIS_FILENAME = "faddis_sensitivity_analysis.csv"
FADDIS_SENSITIVITY_ANALYSIS_FIELDNAMES = [
    "Ground-Truth Type", "Network Property", "FADDIS Property", "#Networks",
    "Spearman Correlation", "Pearson Correlation"
]

REPORT_FILENAME = "report.json"


def run_sensitivity_experiments_in_real_world_networks(apply_lapin: bool = False) -> str:
    execution_start_time = time.perf_counter()
    results_dir = create_results_dir(RESULTS_BASE_DIR_PATH)

    for network_type, networks_base_dir_path in [
        (RESULTS_TRAIN_NETWORKS_NAME, TRAIN_NETWORKS_BASE_DIR_PATH),
        (RESULTS_NETWORKS_WITH_GT_NAME, TEST_NETWORKS_WITH_GT_BASE_DIR_PATH),
        (RESULTS_NETWORKS_WITHOUT_GT_NAME, TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH)
    ]:
        family_dirs = sorted(
            [directory for directory in Path(networks_base_dir_path).iterdir() if directory.is_dir()],
            key=lambda path: path.name
        )

        for family_idx, family_dir in enumerate(family_dirs, start=1):
            log_progress(family_idx, len(family_dirs), family_dir.name, 4, True)

            family_results_dir = create_dir(os.path.join(results_dir, network_type, family_dir.name))
            raw_contributions_file = os.path.join(family_results_dir, RAW_CONTRIBUTIONS_FILENAME)
            network_configs = load_real_world_network_configs(family_dir, family_dir.name)

            with open(file=raw_contributions_file, mode="w", newline="", encoding="utf-8") as out_file:
                writer = csv.writer(out_file)
                writer.writerow(RAW_CONTRIBUTIONS_FILENAMES)

                for network_config_idx, network_config in enumerate(network_configs, start=1):
                    log_progress(network_config_idx, len(network_configs), network_config.name, 2)

                    try:
                        graph, ground_truth_labels, k = load_network_from_gml(str(family_dir), network_config)

                        append_properties(
                            results_dir=os.path.join(results_dir, network_type),
                            output_filename=NETWORK_PROPERTIES_FILENAME,
                            output_fieldnames=NETWORK_PROPERTIES_FIELDNAMES,
                            properties=compute_network_properties(
                                network_name=network_config.name,
                                graph=graph,
                                ground_truth=network_config.ground_truth,
                                overlapping_ground_truth=network_config.overlapping_ground_truth
                            )
                        )

                        if network_config.ground_truth:
                            append_properties(
                                results_dir=os.path.join(results_dir, network_type),
                                output_filename=GROUND_TRUTH_PROPERTIES_FILENAME,
                                output_fieldnames=GROUND_TRUTH_PROPERTIES_FIELDNAMES,
                                properties=compute_ground_truth_properties(
                                    network_name=network_config.name,
                                    ground_truth_labels=ground_truth_labels,
                                    k=k,
                                    overlapping_ground_truth=network_config.overlapping_ground_truth,
                                    number_of_nodes=graph.number_of_nodes()
                                )
                            )

                        A = compute_adjacency_matrix(graph)
                        W = np.asarray(A if not apply_lapin else lapin(A), dtype=np.float64)
                        epsilon, tau, k_max = -np.inf, -np.inf, 1000
                        _, contributions, _, _, _, stop_condition = faddis(
                            W=W, epsilon=epsilon, tau=-np.inf, k_max=k_max
                        )

                        writer.writerow([network_config.name, k, stop_condition] + list(contributions))
                        out_file.flush()
                        os.fsync(out_file.fileno())
                    except Exception as e:
                        print(f"[ERROR] {e}")
                        continue

    perform_faddis_sensitivity_analysis(
        results_dir=os.path.join(results_dir, RESULTS_TRAIN_NETWORKS_NAME),
        network_properties_input_filename=NETWORK_PROPERTIES_FILENAME,
        network_properties_input_fieldnames=NETWORK_PROPERTIES_FIELDNAMES,
        raw_contributions_input_filename=RAW_CONTRIBUTIONS_FILENAME,
        raw_contributions_input_fieldnames=RAW_CONTRIBUTIONS_FILENAMES,
        output_filename=FADDIS_SENSITIVITY_ANALYSIS_FILENAME,
        output_fieldnames=FADDIS_SENSITIVITY_ANALYSIS_FIELDNAMES,
        apply_lapin=apply_lapin
    )

    # Generate report
    execution_elapsed_time = time.perf_counter() - execution_start_time
    save_sensitivity_experiment_report(
        results_dir=os.path.join(results_dir),
        output_filename=REPORT_FILENAME,
        execution_elapsed_time=execution_elapsed_time,
        apply_lapin=apply_lapin
    )

    return results_dir
