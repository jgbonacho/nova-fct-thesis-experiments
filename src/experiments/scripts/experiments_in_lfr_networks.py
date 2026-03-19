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
from experiments.scripts.contributions_experiments_in_lfr_networks import RESULTS_BASE_DIR_PATH, \
    NETWORKS_BASE_DIR_PATH, \
    ROOT_DIR_PATH, REPORT_FILENAME
from experiments.utils.utils import create_results_dir, save_experiment_report, draw_line_plots, read_thresholds

CONFIG_PATH = os.path.join(ROOT_DIR_PATH, 'config')

THRESHOLDS_FILENAME = "thresholds.csv"
EXTRINSIC_RESULTS_FILENAME = "extrinsic_results.csv"


def run_experiments_in_lfr_networks(config_path=CONFIG_PATH, apply_lapin=False):
    results_dir = create_results_dir(RESULTS_BASE_DIR_PATH)
    thresholds = read_thresholds(config_path, THRESHOLDS_FILENAME)

    network_family_dirs = sorted(
        [directory for directory in Path(NETWORKS_BASE_DIR_PATH).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )
    for network_family_idx, network_family_dir in enumerate(network_family_dirs, start=1):
        print(f"#### [{network_family_idx}/{len(network_family_dirs)}] Network Family '{network_family_dir.name}'")

        network_family_results_dir = os.path.join(results_dir, network_family_dir.name)
        os.makedirs(network_family_results_dir)

        networks = sorted({file.stem for file in network_family_dir.iterdir() if file.suffix not in {".txt", ".json"}})
        with (open(os.path.join(network_family_results_dir, EXTRINSIC_RESULTS_FILENAME), "w", newline="",
                   encoding="utf-8") as out_file):
            writer = csv.writer(out_file)
            writer.writerow(["Network", "FADDIS's Epsilon", "K' | K", "|K'-K|/K", "ONMI", "Omega"])

            for network_idx, network in enumerate(networks, start=1):
                print(f"## [{network_idx}/{len(networks)}] Network '{network}'")
                try:
                    graph, ground_truth_labels, k = load_lfr_benchmark_network(
                        dir_path=os.path.join(NETWORKS_BASE_DIR_PATH, network_family_dir.name),
                        filename=network
                    )
                    A = compute_adjacency_matrix(graph)
                    W = A if not apply_lapin else lapin(A)

                    epsilon = thresholds[network_family_dir.name]
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
                        network, epsilon,
                        extrinsic_results["K' | K"],
                        extrinsic_results["|K'-K|/K"],
                        extrinsic_results["ONMI"],
                        extrinsic_results["Omega"]
                    ])
                except Exception as e:
                    print(f"[ERROR] {e}")
                    continue

        draw_line_plots(
            network_family_results_dir, EXTRINSIC_RESULTS_FILENAME, metrics_to_plot=("|K'-K|/K", "ONMI", "Omega")
        )

    save_experiment_report(results_dir, REPORT_FILENAME, apply_lapin, network_family_dirs)
