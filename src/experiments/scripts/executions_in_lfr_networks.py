import csv
import os
from pathlib import Path

import numpy as np

from experiments.defuzzification.defuzzification import apply_defuzzification_rule
from experiments.evaluation_metrics.extrinsic.extrinsic_metrics_for_overlapping_ground_truth import \
    compute_extrinsic_metrics_for_overlapping_ground_truth
from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.loaders.adjacency_matrix import compute_adjacency_matrix
from experiments.loaders.synthetic_data_loader import load_lfr_benchmark_network
from experiments.scripts.contributions_in_lfr_networks import RESULTS_BASE_DIR_PATH, NETWORKS_BASE_DIR_PATH, \
    THRESHOLDS_METRICS, THRESHOLDS_FILENAME, ROOT_DIR_PATH
from experiments.utils.utils import read_thresholds, draw_threshold_metric_line_plot, create_results_dir, \
    save_threshold_metric_votes, save_experiment_report

CONFIG_PATH = os.path.join(ROOT_DIR_PATH, 'config')
EXTRINSIC_RESULTS_FILENAME = "extrinsic_results.csv"
BY_THRESHOLD_FILENAME = "by_threshold.pdf"
THRESHOLD_METRIC_VOTES = "threshold_metric_votes.csv"


def run_executions_experiments_in_lfr_networks(apply_lapin=False, threshold_metrics=THRESHOLDS_METRICS):
    """
    Run execution experiments on all LFR network families using predefined threshold metrics.

    Parameters:
        apply_lapin : (bool)
            Whether to apply the LAPIN transformation as preprocessing step.
        threshold_metrics : (list[str])
            List of threshold metrics to evaluate, for example: ["Median", "75%", "90%", "95%"].

    Saves:
        For each network family:
            - A CSV file with extrinsic evaluation results for each network and threshold metric.
            - A line plot of ONMI by threshold metric across networks.
            - A line plot of Omega by threshold metric across networks.
            - A line plot of relative cluster-count error |K'-K|/K by threshold metric across networks.
    """

    results_dir = create_results_dir(RESULTS_BASE_DIR_PATH)

    thresholds = read_thresholds(CONFIG_PATH, THRESHOLDS_FILENAME, threshold_metrics)

    network_family_dirs = [directory for directory in Path(NETWORKS_BASE_DIR_PATH).iterdir() if directory.is_dir()]
    for network_family_dir_idx, network_family_dir in enumerate(network_family_dirs, start=1):
        network_family = network_family_dir.name
        print(f"====== [{network_family_dir_idx}/{len(network_family_dirs)}] Network Family '{network_family}' ======")

        network_family_results_dir = os.path.join(results_dir, network_family)
        os.makedirs(network_family_results_dir)
        networks = sorted({file.stem for file in network_family_dir.iterdir() if file.suffix not in {".txt", ".md"}})

        with (open(os.path.join(network_family_results_dir, EXTRINSIC_RESULTS_FILENAME), "w", newline="",
                   encoding="utf-8") as out_file):
            writer = csv.writer(out_file)
            writer.writerow(["Network", "Threshold Metric", "Epsilon", "K' | K", "|K'-K|/K", "ONMI", "Omega"])

            for network_idx, network in enumerate(networks, start=1):
                for threshold_metric in threshold_metrics:
                    print(f"=== [{network_idx}/{len(networks)}] Network '{network}' | Threshold '{threshold_metric}' ===")
                    try:
                        graph, ground_truth_labels, k = load_lfr_benchmark_network(
                            path=os.path.join(NETWORKS_BASE_DIR_PATH, network_family),
                            filename=network
                        )
                        A = compute_adjacency_matrix(graph)

                        W = A if not apply_lapin else lapin(A)

                        epsilon = thresholds[threshold_metric][network_family]
                        _, membership_matrix, _, _, _, number_of_clusters = faddis(
                            W=W,
                            epsilon=epsilon,
                            tau=-np.inf,
                            k_max=int(min(100, graph.number_of_nodes() / 2))
                        )

                        predicted_labels, first_cluster_discarded = apply_defuzzification_rule(
                            U=np.asarray(membership_matrix),
                            gamma=0.5,
                            conditionally_discard_first_cluster=True
                        )
                        k_predicted = number_of_clusters - 1 if first_cluster_discarded else number_of_clusters

                        extrinsic_results = compute_extrinsic_metrics_for_overlapping_ground_truth(
                            graph, ground_truth_labels, predicted_labels, k, k_predicted
                        )

                        writer.writerow([
                            network, threshold_metric, epsilon,
                            extrinsic_results["K' | K"],
                            extrinsic_results["|K'-K|/K"],
                            extrinsic_results["ONMI"],
                            extrinsic_results["Omega"]
                        ])

                    except Exception as e:
                        print(f"[ERROR] {e}")
                        continue

        draw_threshold_metric_line_plot(
            network_family_results_dir, EXTRINSIC_RESULTS_FILENAME, BY_THRESHOLD_FILENAME, y_metric="ONMI"
        )
        draw_threshold_metric_line_plot(
            network_family_results_dir, EXTRINSIC_RESULTS_FILENAME, BY_THRESHOLD_FILENAME, y_metric="Omega"
        )
        draw_threshold_metric_line_plot(
            network_family_results_dir, EXTRINSIC_RESULTS_FILENAME, BY_THRESHOLD_FILENAME, y_metric="|K'-K|/K"
        )

    save_threshold_metric_votes(results_dir, EXTRINSIC_RESULTS_FILENAME, THRESHOLD_METRIC_VOTES, threshold_metrics)

    save_experiment_report(results_dir, apply_lapin, threshold_metrics)
