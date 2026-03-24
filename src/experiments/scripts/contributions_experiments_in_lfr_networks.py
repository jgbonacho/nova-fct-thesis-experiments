import csv
import os
from pathlib import Path

import numpy as np

from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.loaders.adjacency_matrix import compute_adjacency_matrix
from experiments.loaders.synthetic_data_loader import load_lfr_benchmark_network
from experiments.utils.utils import selected_thresholds_using_bootstrap_and_mse, create_results_dir, \
    save_normalized_contributions_and_draw_line_plots, save_statistics_and_draw_histograms, draw_boxplot, \
    draw_line_plot, save_candidate_thresholds, save_experiment_report

ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', '..', '..')
NETWORKS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'synthetic')
RESULTS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'results')

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

THRESHOLDS_METRICS = ("Mean-Std", "Mean", "Mean+Std", "Median", "75%", "90%", "95%")


def run_contributions_experiments_in_lfr_networks(apply_lapin=False, use_desired_k=True):
    results_dir = create_results_dir(RESULTS_BASE_DIR_PATH)

    # Stage 1
    network_family_dirs = sorted(
        [directory for directory in Path(NETWORKS_BASE_DIR_PATH).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )
    for network_family_idx, network_family_dir in enumerate(network_family_dirs, start=1):
        print(f"#### [{network_family_idx}/{len(network_family_dirs)}] Network Family '{network_family_dir.name}'")

        network_family_results_dir = os.path.join(results_dir, network_family_dir.name)
        os.makedirs(network_family_results_dir)

        networks = sorted({file.stem for file in network_family_dir.iterdir() if file.suffix not in {".txt", ".json"}})
        with (open(os.path.join(network_family_results_dir, RAW_CONTRIBUTIONS_FILENAME), "w", newline="",
                   encoding="utf-8") as out_file):
            writer = csv.writer(out_file)
            writer.writerow(["Network", "K"])

            for network_idx, network in enumerate(networks, start=1):
                print(f"## [{network_idx}/{len(networks)}] Network '{network}'")
                try:
                    graph, _, k = load_lfr_benchmark_network(
                        dir_path=os.path.join(NETWORKS_BASE_DIR_PATH, network_family_dir.name), filename=network
                    )
                    A = compute_adjacency_matrix(graph)
                    W = A if not apply_lapin else lapin(A)

                    if use_desired_k:
                        _, _, contributions, _, _, _, _ = faddis(W=W, desired_k=k + 1 if not apply_lapin else k)
                    else:
                        _, _, contributions, _, _, _, _ = faddis(W=W, epsilon=-np.inf, tau=-np.inf, k_max=1000)

                    writer.writerow([network, k] + list(contributions))
                except Exception as e:
                    print(f"[ERROR] {e}")
                    continue

    save_normalized_contributions_and_draw_line_plots(
        results_dir, RAW_CONTRIBUTIONS_FILENAME, NORMALIZED_CONTRIBUTIONS_FILENAME
    )
    save_statistics_and_draw_histograms(
        results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, STATISTICS_FILENAME, HISTOGRAM_FILENAME
    )
    draw_boxplot(results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, BOXPLOT_FILENAME)
    draw_line_plot(results_dir, STATISTICS_FILENAME, LINE_PLOT_FILENAME)
    save_candidate_thresholds(results_dir, STATISTICS_FILENAME, CANDIDATE_THRESHOLDS_FILENAME, THRESHOLDS_METRICS)

    # Stage 2
    selected_thresholds_using_bootstrap_and_mse(
        results_dir=results_dir,
        raw_contributions_input_filename=RAW_CONTRIBUTIONS_FILENAME,
        candidate_thresholds_input_filename=CANDIDATE_THRESHOLDS_FILENAME,
        bootstrap_statistics_output_filename=BOOTSTRAP_STATISTICS_FILENAME,
        thresholds_output_filename=SELECTED_THRESHOLDS_FILENAME,
        threshold_metrics=THRESHOLDS_METRICS,
        maximum_number_of_bootstraps=1000,
        subsample_fraction=0.8
    )

    # Report
    save_experiment_report(results_dir, REPORT_FILENAME, apply_lapin, network_family_dirs, use_desired_k)

    return results_dir
