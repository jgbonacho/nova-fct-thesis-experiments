import csv
import os
import time
from pathlib import Path

import numpy as np
from experiments.config import REAL_WORLD_RESULTS_BASE_DIR_PATH, REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME, \
    REAL_WORLD_TRAIN_NETWORKS_BASE_DIR_PATH
from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.scripts.real_world_networks.sensitivity_analysis.correlations.correlations import \
    perform_faddis_sensitivity_analysis
from experiments.scripts.real_world_networks.sensitivity_analysis.utils.utils import load_real_world_network_configs, \
    append_properties, save_experiment_report
from experiments.scripts.real_world_networks.sensitivity_analysis.utils.variables import \
    RAW_CONTRIBUTIONS_FILENAME, RAW_CONTRIBUTIONS_FIELDNAMES, NETWORK_PROPERTIES_FILENAME, \
    NETWORK_PROPERTIES_FIELDNAMES, \
    FADDIS_SENSITIVITY_ANALYSIS_FILENAME, \
    FADDIS_SENSITIVITY_ANALYSIS_FIELDNAMES, REPORT_FILENAME
from experiments.scripts.real_world_networks.utils.network_properties.network_properties import \
    compute_network_properties
from experiments.scripts.real_world_networks.utils.real_world_data_loader import load_network_from_gml
from experiments.scripts.utils.adjacency_matrix import compute_adjacency_matrix
from experiments.scripts.utils.utils import create_results_dir, log_progress, create_dir


def sensitivity_analysis_in_real_world_networks(apply_lapin: bool = True) -> str:
    """
    Perform a FADDIS sensitivity analysis in real-world networks.

    Parameters:
        apply_lapin : (bool, optional)
            Whether to apply the Lapin transformation.
            Default is True.

    Returns:
        results_dir : (str)
            The path to the results' directory.
    """

    execution_start_time = time.perf_counter()
    results_dir = create_results_dir(REAL_WORLD_RESULTS_BASE_DIR_PATH)

    network_type = REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME
    networks_base_dir_path = REAL_WORLD_TRAIN_NETWORKS_BASE_DIR_PATH

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
            writer.writerow(RAW_CONTRIBUTIONS_FIELDNAMES)

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
        results_dir=os.path.join(results_dir, REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME),
        network_properties_input_filename=NETWORK_PROPERTIES_FILENAME,
        network_properties_input_fieldnames=NETWORK_PROPERTIES_FIELDNAMES,
        raw_contributions_input_filename=RAW_CONTRIBUTIONS_FILENAME,
        raw_contributions_input_fieldnames=RAW_CONTRIBUTIONS_FIELDNAMES,
        output_filename=FADDIS_SENSITIVITY_ANALYSIS_FILENAME,
        output_fieldnames=FADDIS_SENSITIVITY_ANALYSIS_FIELDNAMES,
        apply_lapin=apply_lapin
    )

    # Generate report.
    execution_elapsed_time = time.perf_counter() - execution_start_time
    save_experiment_report(
        results_dir=os.path.join(results_dir),
        output_filename=REPORT_FILENAME,
        execution_elapsed_time=execution_elapsed_time,
        apply_lapin=apply_lapin
    )

    return results_dir
