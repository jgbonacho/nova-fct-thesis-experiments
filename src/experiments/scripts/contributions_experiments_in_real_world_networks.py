import csv
import os
from pathlib import Path

import numpy as np

from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.loaders.adjacency_matrix import compute_adjacency_matrix
from experiments.loaders.real_world_data_loader import load_network_from_gml
from experiments.utils.utils import log_progress, create_results_dir, \
    save_normalized_contributions_and_draw_line_plots, save_statistics_and_draw_histograms, draw_boxplot, \
    draw_line_plot, save_candidate_thresholds, save_experiment_report, load_real_world_network_configs, \
    compute_real_world_network_properties, draw_sorted_k_contributions_bar_plot, \
    selected_thresholds_using_a_statistic_metric, save_k_boundary_geometric_mean_thresholds, \
    save_faddis_sensitivity_correlations

ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..')
NETWORKS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'real-world')
RESULTS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'results', 'real-world')

RAW_CONTRIBUTIONS_FILENAME = "raw_contributions.csv"
NORMALIZED_CONTRIBUTIONS_FILENAME = "normalized_contributions.csv"
STATISTICS_FILENAME = "statistics.csv"
HISTOGRAM_FILENAME = "histogram.pdf"
BOXPLOT_FILENAME = "boxplot.pdf"
LINE_PLOT_FILENAME = "line_plot.pdf"
CANDIDATE_THRESHOLDS_FILENAME = "candidate_thresholds.csv"
BOOTSTRAP_STATISTICS_FILENAME = "bootstrap_statistics.csv"
SELECTED_THRESHOLDS_FILENAME = "thresholds.csv"
REPORT_FILENAME = "report.json"
BARPLOT_FILENAME = "sorted_k_contributions_barplot.pdf"
NETWORK_PROPERTIES_FILENAME = "network_properties.csv"
K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAME = "k_boundary_thresholds_by_network.csv"
K_BOUNDARY_THRESHOLDS_BY_FAMILY_FILENAME = "thresholds.csv"
FADDIS_SENSITIVITY_CORRELATIONS = "faddis_sensitivity_correlations.csv"

THRESHOLDS_METRICS = ("Mean", "Median", "75%", "90%", "95%")
NETWORK_PROPERTIES_FIELDNAMES = [
    "Network", "Ground-Truth?",
    "Nodes LCC", "Edges LCC",
    "Min Degree", "Max Degree", "Average Degree", "Degree Std", "Degree CV", "Degree Hub Ratio",
    "Density", "Sparsity",
    "Global Clustering Coefficient", "Degree Assortativity", "Average Clustering",
    "Overlapping Ground-Truth?", "Overlap Fraction",
    "K", "Community Proportion",
    "Min Community Size", "Max Community Size", "Average Community Size", "Community Size Std", "Community Size CV",
    "Nodes Without Community", "Nodes Fraction Without Community"
]


def run_contributions_experiments_in_real_world_networks(apply_lapin: bool = False, use_desired_k: bool = True) -> str:
    """
    Run contributions experiments in real-world networks.
    Exceptionally, when the configuration is LAPIN-off and extraction of K desired clusters,
    the script extracts K + 1 clusters due to the conditional removal of the first extracted cluster, which behave as a global/background component.

    Parameters:
        apply_lapin : (bool)
            Whether to apply the Lapin transformation.
        use_desired_k : (bool)
            Whether to use the desired number of communities.

    Returns:
        results_dir : (str)
            The path to the results' directory.

    Saves:
        TODO
    """

    results_dir = create_results_dir(RESULTS_BASE_DIR_PATH)

    # Stage 1
    network_family_dirs = sorted(
        [directory for directory in Path(NETWORKS_BASE_DIR_PATH).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )

    with open(os.path.join(results_dir, NETWORK_PROPERTIES_FILENAME), "w", newline="",
              encoding="utf-8") as properties_file:
        properties_writer = csv.DictWriter(properties_file, fieldnames=NETWORK_PROPERTIES_FIELDNAMES)
        properties_writer.writeheader()

        for network_family_idx, network_family_dir in enumerate(network_family_dirs, start=1):
            log_progress(network_family_idx, len(network_family_dirs), network_family_dir.name, 4, True)

            network_family_results_dir = os.path.join(results_dir, network_family_dir.name)
            os.makedirs(network_family_results_dir)

            network_configs = load_real_world_network_configs(network_family_dir, network_family_dir.name)
            with (open(os.path.join(network_family_results_dir, RAW_CONTRIBUTIONS_FILENAME), "w", newline="",
                       encoding="utf-8") as out_file):
                writer = csv.writer(out_file)
                writer.writerow(["Network", "K", "Stop Condition"])

                for network_config_idx, network_config in enumerate(network_configs, start=1):
                    log_progress(network_config_idx, len(network_configs), network_config.name, 2)

                    try:
                        graph, ground_truth_labels, k = load_network_from_gml(network_family_dir, network_config)

                        properties_writer.writerow(
                            compute_real_world_network_properties(
                                network_name=network_config.name,
                                graph=graph,
                                ground_truth_labels=ground_truth_labels,
                                k=k,
                                ground_truth=network_config.ground_truth,
                                overlapping_ground_truth=network_config.overlapping_ground_truth
                            )
                        )
                        properties_file.flush()
                        os.fsync(properties_file.fileno())

                        A = compute_adjacency_matrix(graph)
                        W = A if not apply_lapin else lapin(A)
                        W = np.asarray(W, dtype=np.float64)

                        if use_desired_k:
                            _, contributions, _, _, _, stop_condition = faddis(
                                W=W, desired_k=k + 1 if not apply_lapin else k
                            )
                        else:
                            _, contributions, _, _, _, stop_condition = faddis(
                                W=W, epsilon=-np.inf, tau=-np.inf, k_max=1000
                            )

                        writer.writerow([network_config.name, k, stop_condition] + list(contributions))

                        out_file.flush()
                        os.fsync(out_file.fileno())
                    except Exception as e:
                        print(f"[ERROR] {e}")
                        continue

    global_sum = save_normalized_contributions_and_draw_line_plots(
        results_dir, RAW_CONTRIBUTIONS_FILENAME, NORMALIZED_CONTRIBUTIONS_FILENAME,
        number_of_columns_to_skip=3
    )

    if use_desired_k:
        save_statistics_and_draw_histograms(
            results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, STATISTICS_FILENAME, HISTOGRAM_FILENAME,
            number_of_columns_to_skip=3
        )
        draw_boxplot(results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, BOXPLOT_FILENAME, number_of_columns_to_skip=3)
        draw_line_plot(results_dir, STATISTICS_FILENAME, LINE_PLOT_FILENAME)
        save_candidate_thresholds(results_dir, STATISTICS_FILENAME, CANDIDATE_THRESHOLDS_FILENAME, THRESHOLDS_METRICS)

        # Stage 2
        selected_thresholds_using_a_statistic_metric(
            results_dir=results_dir,
            candidate_thresholds_input_filename=CANDIDATE_THRESHOLDS_FILENAME,
            thresholds_output_filename=SELECTED_THRESHOLDS_FILENAME,
            statistics_metric="Median"
        )

        # Stage 3
        save_faddis_sensitivity_correlations(
            results_dir=results_dir,
            network_properties_filename=NETWORK_PROPERTIES_FILENAME,
            threshold_source_filename=NORMALIZED_CONTRIBUTIONS_FILENAME,
            output_filename=FADDIS_SENSITIVITY_CORRELATIONS,
            threshold_mode="network_statistic",
            statistic_metric="Median",
            number_of_columns_to_skip=3
        )

    else:
        draw_sorted_k_contributions_bar_plot(
            results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, BARPLOT_FILENAME,
            remove_first_contribution=not apply_lapin,
            number_of_columns_to_skip=3
        )

        # Stage 2
        save_k_boundary_geometric_mean_thresholds(
            results_dir=results_dir,
            input_filename=NORMALIZED_CONTRIBUTIONS_FILENAME,
            output_by_network_filename=K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAME,
            output_by_family_filename=K_BOUNDARY_THRESHOLDS_BY_FAMILY_FILENAME,
            remove_first_contribution=not apply_lapin,
            global_sum=global_sum,
            number_of_columns_to_skip=3
        )

        # Stage 3
        save_faddis_sensitivity_correlations(
            results_dir=results_dir,
            network_properties_filename=NETWORK_PROPERTIES_FILENAME,
            threshold_source_filename=K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAME,
            output_filename=FADDIS_SENSITIVITY_CORRELATIONS,
            threshold_mode="k_boundary",
            threshold_column="Normalized Threshold",
            valid_thresholds_only=True,
            number_of_columns_to_skip=3
        )

    # Report
    save_experiment_report(results_dir, REPORT_FILENAME, apply_lapin, use_desired_k, network_family_dirs)

    return results_dir
