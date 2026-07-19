import csv
import os
import time
from pathlib import Path

import numpy as np

from experiments.config import REAL_WORLD_TRAIN_NETWORKS_BASE_DIR_PATH, REAL_WORLD_TEST_NETWORKS_WITH_GT_BASE_DIR_PATH, \
    REAL_WORLD_TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH, REAL_WORLD_RESULTS_BASE_DIR_PATH, \
    REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME, REAL_WORLD_RESULTS_TRAIN_NETWORKS_WITH_GT_NAME, \
    REAL_WORLD_RESULTS_TEST_NETWORKS_WITH_GT_NAME, REAL_WORLD_RESULTS_TEST_NETWORKS_WITHOUT_GT_NAME
from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.scripts.real_world_networks.sensitivity_analysis.utils.utils import load_real_world_network_configs
from experiments.scripts.real_world_networks.thresholds.network_family_thresholds.network_family_candidate_thresholds.network_family_candidate_thresholds import \
    compute_thresholds_per_family
from experiments.scripts.real_world_networks.thresholds.network_thresholds.extrinsic_evaluation.extrinsic_evaluation import \
    evaluate_final_threshold_using_extrinsic_metrics
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.intrinsic_evaluation import \
    evaluate_candidate_thresholds_using_intrinsic_metrics
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.network_candidate_thresholds import \
    compute_candidate_thresholds
from experiments.scripts.real_world_networks.thresholds.network_thresholds.null_model_evaluation.null_model_evaluation import \
    evaluate_candidate_thresholds_under_null_model
from experiments.scripts.real_world_networks.thresholds.network_thresholds.outputs.outputs import generate_final_outputs
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_filtering_and_parsimony_selection import \
    select_final_threshold_by_pareto_and_parsimony
from experiments.scripts.real_world_networks.thresholds.network_thresholds.stability_evaluation.stability_evaluation import \
    evaluate_candidate_thresholds_under_perturbation_stability
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.thresholds.utils.real_world_data_loader import load_network_from_gml
from experiments.scripts.real_world_networks.thresholds.utils.utils import save_contributions_experiment_report
from experiments.scripts.real_world_networks.thresholds.utils.variables import RAW_CONTRIBUTIONS_FILENAME, \
    RAW_CONTRIBUTIONS_FILENAMES, \
    K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAME, K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAMES, \
    K_BOUNDARY_THRESHOLDS_BY_FAMILY_FILENAME, K_BOUNDARY_THRESHOLDS_BY_FAMIL_FIELDNAMES, \
    CANDIDATE_THRESHOLDS_FILENAME, \
    CANDIDATE_THRESHOLDS_FIELDNAMES, INTRINSIC_EVALUATION_FILENAME, INTRINSIC_EVALUATION_FIELDNAMES, \
    STABILITY_EVALUATION_FILENAME, STABILITY_EVALUATION_FIELDNAMES, NULL_MODEL_EVALUATION_FILENAME, \
    NULL_MODEL_EVALUATION_FIELDNAMES, FINAL_THRESHOLDS_FILENAME, FINAL_THRESHOLDS_FIELDNAMES, THRESHOLD_FILENAME, \
    EXTRINSIC_EVALUATION_FILENAME, REPORT_FILENAME
from experiments.scripts.utils.adjacency_matrix import compute_adjacency_matrix
from experiments.scripts.utils.utils import create_results_dir, log_progress, create_dir


def estimate_real_world_network_thresholds(config: RealWorldThresholdEstimationConfig) -> str:
    """
    Estimate real-world network thresholds.

    Parameters:
        config : (LFRThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        results_dir : (str)
            The path to the results' directory.
    """

    execution_start_time = time.perf_counter()
    results_dir = create_results_dir(REAL_WORLD_RESULTS_BASE_DIR_PATH)

    # Stage 1
    family_dirs = sorted(
        [directory for directory in Path(REAL_WORLD_TRAIN_NETWORKS_BASE_DIR_PATH).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )

    for network_family_idx, network_family_dir in enumerate(family_dirs, start=1):
        log_progress(network_family_idx, len(family_dirs), network_family_dir.name, 4, True)

        family_results_dir = create_dir(
            os.path.join(results_dir, REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME, network_family_dir.name))
        raw_contributions_file = os.path.join(family_results_dir, RAW_CONTRIBUTIONS_FILENAME)
        network_configs = load_real_world_network_configs(network_family_dir, network_family_dir.name)

        with open(file=raw_contributions_file, mode="w", newline="", encoding="utf-8") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(RAW_CONTRIBUTIONS_FILENAMES)

            for network_config_idx, network_config in enumerate(network_configs, start=1):
                log_progress(network_config_idx, len(network_configs), network_config.name, 2)

                try:
                    graph, ground_truth_labels, k = load_network_from_gml(str(network_family_dir), network_config)

                    A = compute_adjacency_matrix(graph)
                    W = np.asarray(A if not config.apply_lapin else lapin(A), dtype=np.float64)
                    epsilon, tau, k_max = -np.inf, config.tau, config.compute_k_max(graph.number_of_nodes())
                    _, contributions, _, _, _, stop_condition = faddis(
                        W=W, epsilon=epsilon, tau=tau, k_max=k_max
                    )

                    writer.writerow([network_config.name, k, stop_condition] + list(contributions))
                    out_file.flush()
                    os.fsync(out_file.fileno())
                except Exception as e:
                    print(f"[ERROR] {e}")
                    continue

    thresholds_per_family = compute_thresholds_per_family(
        results_dir=os.path.join(results_dir, REAL_WORLD_RESULTS_TRAIN_NETWORKS_NAME),
        input_filename=RAW_CONTRIBUTIONS_FILENAME,
        input_fieldnames=RAW_CONTRIBUTIONS_FILENAMES,
        k_boundary_thresholds_by_network_output_filename=K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAME,
        k_boundary_thresholds_by_network_output_fieldnames=K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAMES,
        k_boundary_thresholds_by_family_output_filename=K_BOUNDARY_THRESHOLDS_BY_FAMILY_FILENAME,
        k_boundary_thresholds_by_family_output_fieldnames=K_BOUNDARY_THRESHOLDS_BY_FAMIL_FIELDNAMES,
        discard_global_component=not config.apply_lapin
    )

    # Stage 2
    for network_type_name, networks_base_dir_path in [
        (REAL_WORLD_RESULTS_TRAIN_NETWORKS_WITH_GT_NAME, REAL_WORLD_TRAIN_NETWORKS_BASE_DIR_PATH),
        (REAL_WORLD_RESULTS_TEST_NETWORKS_WITHOUT_GT_NAME, REAL_WORLD_TEST_NETWORKS_WITHOUT_GT_BASE_DIR_PATH),
        (REAL_WORLD_RESULTS_TEST_NETWORKS_WITH_GT_NAME, REAL_WORLD_TEST_NETWORKS_WITH_GT_BASE_DIR_PATH),
    ]:
        family_dirs = sorted(
            [directory for directory in Path(networks_base_dir_path).iterdir() if directory.is_dir()],
            key=lambda path: path.name
        )

        for network_family_idx, network_family_dir in enumerate(family_dirs, start=1):
            log_progress(network_family_idx, len(family_dirs), network_family_dir.name, 4, True)

            network_configs = load_real_world_network_configs(network_family_dir, network_family_dir.name)
            for network_config_idx, network_config in enumerate(network_configs, start=1):
                log_progress(network_config_idx, len(network_configs), network_config.name, 2)

                network_results_dir = create_dir(os.path.join(results_dir, network_type_name, network_config.name))
                raw_contributions_file_2 = os.path.join(network_results_dir, RAW_CONTRIBUTIONS_FILENAME)

                with open(file=raw_contributions_file_2, mode="w", newline="", encoding="utf-8") as out_file:
                    writer = csv.writer(out_file)
                    writer.writerow(RAW_CONTRIBUTIONS_FILENAMES)

                    try:
                        graph, ground_truth_labels, k = load_network_from_gml(str(network_family_dir), network_config)

                        A = compute_adjacency_matrix(graph)
                        W = np.asarray(A if not config.apply_lapin else lapin(A), dtype=np.float64)
                        epsilon, tau, k_max = -np.inf, config.tau, config.compute_k_max(graph.number_of_nodes())
                        _, contributions, _, _, _, stop_condition = faddis(
                            W=W, epsilon=epsilon, tau=tau, k_max=k_max
                        )

                        writer.writerow([network_config.name, k, stop_condition] + list(contributions))
                        out_file.flush()
                        os.fsync(out_file.fileno())
                    except Exception as e:
                        print(f"[ERROR] {e}")
                        continue

                # Stage 2.1
                candidate_thresholds = compute_candidate_thresholds(
                    results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                    network_family=network_family_dir.name,
                    k_boundary_thresholds_per_family=thresholds_per_family,
                    input_filename=RAW_CONTRIBUTIONS_FILENAME,
                    input_fieldnames=RAW_CONTRIBUTIONS_FILENAMES,
                    output_filename=CANDIDATE_THRESHOLDS_FILENAME,
                    output_fieldnames=CANDIDATE_THRESHOLDS_FIELDNAMES
                )

                # Stage 2.2
                candidate_thresholds_after_intrinsic_evaluation = evaluate_candidate_thresholds_using_intrinsic_metrics(
                    results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                    graph_and_matrices=(graph, A, W),
                    candidate_thresholds=candidate_thresholds,
                    output_filename=INTRINSIC_EVALUATION_FILENAME,
                    output_fieldnames=INTRINSIC_EVALUATION_FIELDNAMES,
                    config=config
                )

                # Stage 2.3
                candidate_thresholds_after_perturbation_stability = evaluate_candidate_thresholds_under_perturbation_stability(
                    results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                    graph_and_matrices=(graph, A, W),
                    candidate_thresholds=candidate_thresholds_after_intrinsic_evaluation,
                    output_filename=STABILITY_EVALUATION_FILENAME,
                    output_fieldnames=STABILITY_EVALUATION_FIELDNAMES,
                    config=config
                )

                # Stage 2.4
                candidate_thresholds_after_null_model = evaluate_candidate_thresholds_under_null_model(
                    results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                    graph_and_matrices=(graph, A, W),
                    candidate_thresholds=candidate_thresholds_after_perturbation_stability,
                    output_filename=NULL_MODEL_EVALUATION_FILENAME,
                    output_fieldnames=NULL_MODEL_EVALUATION_FIELDNAMES,
                    config=config
                )

                # Stage 2.5
                final_threshold = select_final_threshold_by_pareto_and_parsimony(
                    results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                    candidate_thresholds=candidate_thresholds_after_null_model,
                    final_thresholds_output_filename=FINAL_THRESHOLDS_FILENAME,
                    final_thresholds_output_fieldnames=FINAL_THRESHOLDS_FIELDNAMES,
                    threshold_output_filename=THRESHOLD_FILENAME
                )

                generate_final_outputs(
                    results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                    raw_contributions_filename=RAW_CONTRIBUTIONS_FILENAME,
                    raw_contributions_fieldnames=RAW_CONTRIBUTIONS_FILENAMES,
                    candidate_thresholds_filename=CANDIDATE_THRESHOLDS_FILENAME,
                    intrinsic_evaluation_filename=INTRINSIC_EVALUATION_FILENAME,
                    stability_evaluation_filename=STABILITY_EVALUATION_FILENAME,
                    null_model_evaluation_filename=NULL_MODEL_EVALUATION_FILENAME,
                    final_threshold=final_threshold,
                    config=config
                )

                # Stage 2.6
                if network_type_name in {REAL_WORLD_RESULTS_TRAIN_NETWORKS_WITH_GT_NAME,
                                         REAL_WORLD_RESULTS_TEST_NETWORKS_WITH_GT_NAME}:
                    evaluate_final_threshold_using_extrinsic_metrics(
                        results_dir=os.path.join(results_dir, network_type_name, network_config.name),
                        graph_and_matrices=(graph, A, W),
                        overlapping_ground_truth=network_config.overlapping_ground_truth,
                        ground_truth=(ground_truth_labels, k),
                        final_threshold=final_threshold,
                        output_filename=EXTRINSIC_EVALUATION_FILENAME,
                        output_base_fieldnames=FINAL_THRESHOLDS_FIELDNAMES,
                        config=config
                    )

    # Generate report
    execution_elapsed_time = time.perf_counter() - execution_start_time
    save_contributions_experiment_report(
        results_dir=results_dir,
        output_filename=REPORT_FILENAME,
        execution_elapsed_time=execution_elapsed_time,
        config=config
    )

    return results_dir
