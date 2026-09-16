import os
import time
from pathlib import Path

from experiments.config import REAL_WORLD_RESULTS_BASE_DIR_PATH, REAL_WORLD_TEST_NETWORKS_WITH_GT_BASE_DIR_PATH, \
    REAL_WORLD_TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH, REAL_WORLD_RESULTS_TEST_NETWORKS_WITH_GT_NAME, \
    REAL_WORLD_RESULTS_TEST_NETWORKS_WITHOUT_GT_NAME
from experiments.scripts.real_world_networks.sensitivity_analysis.utils.utils import load_real_world_network_configs, \
    append_properties, save_experiment_report
from experiments.scripts.real_world_networks.sensitivity_analysis.utils.variables import \
    NETWORK_PROPERTIES_FILENAME, \
    NETWORK_PROPERTIES_FIELDNAMES, \
    GROUND_TRUTH_PROPERTIES_FILENAME, GROUND_TRUTH_PROPERTIES_FIELDNAMES, REPORT_FILENAME
from experiments.scripts.real_world_networks.utils.ground_truth_properties.ground_truth_properties import \
    compute_ground_truth_properties
from experiments.scripts.real_world_networks.utils.network_properties.network_properties import \
    compute_network_properties
from experiments.scripts.real_world_networks.utils.real_world_data_loader import load_network_from_gml
from experiments.scripts.utils.utils import create_results_dir, log_progress


def characterization_of_real_world_networks() -> str:
    """
    Characterization of real world networks.

    Returns:
        results_dir : (str)
            The path to the results' directory.
    """

    execution_start_time = time.perf_counter()
    results_dir = create_results_dir(REAL_WORLD_RESULTS_BASE_DIR_PATH)

    for network_type, networks_base_dir_path in [
        (REAL_WORLD_RESULTS_TEST_NETWORKS_WITH_GT_NAME, REAL_WORLD_TEST_NETWORKS_WITH_GT_BASE_DIR_PATH),
        (REAL_WORLD_RESULTS_TEST_NETWORKS_WITHOUT_GT_NAME, REAL_WORLD_TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH)
    ]:
        family_dirs = sorted(
            [directory for directory in Path(networks_base_dir_path).iterdir() if directory.is_dir()],
            key=lambda path: path.name
        )

        for family_idx, family_dir in enumerate(family_dirs, start=1):
            log_progress(family_idx, len(family_dirs), family_dir.name, 4, True)

            network_configs = load_real_world_network_configs(family_dir, family_dir.name)
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
                except Exception as e:
                    print(f"[ERROR] {e}")
                    continue

    # Generate report.
    execution_elapsed_time = time.perf_counter() - execution_start_time
    save_experiment_report(
        results_dir=os.path.join(results_dir),
        output_filename=REPORT_FILENAME,
        execution_elapsed_time=execution_elapsed_time
    )

    return results_dir
