import csv
import os
from pathlib import Path

import numpy as np

from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.loaders.adjacency_matrix import compute_adjacency_matrix
from experiments.loaders.synthetic_data_loader import load_lfr_benchmark_network
from experiments.utils.utils import create_results_dir, save_normalized_contributions, draw_histograms, \
    save_global_statistics, draw_line_plot, draw_boxplot, save_thresholds, save_experiment_report

ROOT_DIR_PATH = os.path.join(os.path.dirname(__file__), '..', '..')
NETWORKS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'networks', 'synthetic')
RESULTS_BASE_DIR_PATH = os.path.join(ROOT_DIR_PATH, 'results')

CONTRIBUTIONS_FILENAME = "contributions.csv"
NORMALIZED_CONTRIBUTIONS_FILENAME = "normalized_contributions.csv"
HISTOGRAM_FILENAME = "histogram.pdf"

STATISTICS_FILENAME = "statistics.csv"
LINE_PLOT_FILENAME = "line_plot.pdf"
BOXPLOT_FILENAME = "boxplot.pdf"
THRESHOLDS_FILENAME = "thresholds.csv"
THRESHOLDS_METRICS = ("Median", "75%", "90%", "95%")


def run_contributions_experiments_in_lfr_networks(apply_lapin=False, desired_k=True, threshold_metrics=THRESHOLDS_METRICS):
    """
    Run contribution experiments on all LFR network families.

    Parameters:
        apply_lapin : (bool, optional)
            Whether to apply the LAPIN transformation as preprocessing step.
            Default is False.
        desired_k : (bool, optional)
            Whether to stop iterative extraction when the desired number of clusters is extracted
            or when the eigenvalues of the residual matrix are not positive.
            Default is True.
        threshold_metrics : (list[str])
            Statistics used to generate the threshold files.
            Default is THRESHOLDS_METRICS.

    Saves:
        For each network family:
            - A CSV file with raw contribution values for each network.
            - A CSV file with normalized contribution values.
            - One histogram with threshold lines.

        In the global results directory:
            - A CSV file with summary statistics per network family.
            - A line plot of contribution percentiles by network family.
            - A boxplot of normalized contributions by network family.
            - A CSV file with for each selected threshold per network family.
            - A JSON report with experiment metadata.
    """

    results_dir = create_results_dir(RESULTS_BASE_DIR_PATH)

    network_family_dirs = [directory for directory in Path(NETWORKS_BASE_DIR_PATH).iterdir() if directory.is_dir()]
    networks_by_family = {}
    for network_family_dir_idx, network_family_dir in enumerate(network_family_dirs, start=1):
        network_family = network_family_dir.name
        print(f"====== [{network_family_dir_idx}/{len(network_family_dirs)}] Network Family '{network_family}' ======")

        network_family_results_dir = os.path.join(results_dir, network_family)
        os.makedirs(network_family_results_dir)
        networks = sorted({file.stem for file in network_family_dir.iterdir() if file.suffix not in {".txt", ".md"}})
        networks_by_family[network_family] = networks

        with (open(os.path.join(network_family_results_dir, CONTRIBUTIONS_FILENAME), "w", newline="", encoding="utf-8")
              as out_file):
            writer = csv.writer(out_file)
            writer.writerow(["Network", "K"])

            for network_idx, network in enumerate(networks, start=1):
                print(f"=== [{network_idx}/{len(networks)}] Network '{network}' ===")
                try:
                    graph, _, k = load_lfr_benchmark_network(
                        path=os.path.join(NETWORKS_BASE_DIR_PATH, network_family),
                        filename=network
                    )
                    A = compute_adjacency_matrix(graph)

                    W = A if not apply_lapin else lapin(A)

                    if desired_k:
                        _, _, contributions, _, _, _ = faddis(W=W, desired_k=k)
                    else:
                        _, _, contributions, _, _, _ = faddis(W=W, epsilon=-np.inf, tau=-np.inf, k_max=np.inf)

                    writer.writerow([network, k] + list(contributions))

                except Exception as e:
                    print(f"[ERROR] {e}")
                    continue

    save_normalized_contributions(results_dir, CONTRIBUTIONS_FILENAME, NORMALIZED_CONTRIBUTIONS_FILENAME)

    save_global_statistics(results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, STATISTICS_FILENAME)
    draw_line_plot(results_dir, STATISTICS_FILENAME, LINE_PLOT_FILENAME)

    draw_boxplot(results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, BOXPLOT_FILENAME)
    draw_histograms(results_dir, NORMALIZED_CONTRIBUTIONS_FILENAME, STATISTICS_FILENAME, HISTOGRAM_FILENAME)

    save_thresholds(results_dir, STATISTICS_FILENAME, THRESHOLDS_FILENAME, threshold_metrics)

    save_experiment_report(
        results_dir, apply_lapin, threshold_metrics, desired_k, network_family_dirs, networks_by_family
    )
