import csv
import os
import time

import numpy as np

from experiments.config import SYNTHETIC_NETWORKS_BASE_DIR_PATH, SYNTHETIC_RESULTS_BASE_DIR_PATH
from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.scripts.lfr_networks.thresholds.bootstrap_and_mse_selection.bootstrap_and_mse import \
    selected_thresholds_using_bootstrap_and_mse
from experiments.scripts.lfr_networks.thresholds.lfr_threshold_estimation_config import LFRThresholdEstimationConfig
from experiments.scripts.lfr_networks.thresholds.network_family_candidate_thresholds.network_family_candidate_thresholds import \
    save_normalized_contributions_and_draw_line_plots, save_statistics_and_draw_histograms, draw_boxplot, \
    draw_line_plot, save_candidate_thresholds
from experiments.scripts.lfr_networks.thresholds.utils.synthetic_data_loader import \
    load_lfr_benchmark_network
from experiments.scripts.lfr_networks.thresholds.utils.utils import save_experiment_report, \
    get_family_dirs
from experiments.scripts.lfr_networks.thresholds.utils.variables import RAW_CONTRIBUTIONS_FILENAME, \
    RAW_CONTRIBUTIONS_FIELDNAMES, NORMALIZED_CONTRIBUTIONS_FILENAME, \
    NORMALIZED_CONTRIBUTIONS_FIELDNAMES, STATISTICS_FILENAME, HISTOGRAM_FILENAME, STATISTICS_FIELDNAMES, \
    BOXPLOT_FILENAME, LINE_PLOT_FILENAME, CANDIDATE_THRESHOLDS_FILENAME, CANDIDATE_THRESHOLDS_FIELDNAMES, \
    BOOTSTRAP_STATISTICS_FIELDNAMES, BOOTSTRAP_STATISTICS_FILENAME, SELECTED_THRESHOLDS_FILENAME, \
    SELECTED_THRESHOLDS_FIELDNAMES, REPORT_FILENAME
from experiments.scripts.utils.adjacency_matrix import compute_adjacency_matrix
from experiments.scripts.utils.utils import log_progress, create_results_dir, create_dir


def estimate_lfr_network_family_thresholds(config: LFRThresholdEstimationConfig) -> str:
    """
    Estimate LFR network family thresholds.
    Exceptionally, when the configuration is LAPIN-off and extraction of K desired clusters,
    the script extracts K + 1 clusters to account for the first extracted global/background component.

    Parameters:
        config : (LFRThresholdEstimationConfig)
            Configuration of the threshold estimation.
    
    Returns:
        results_dir : (str)
            The path to the results' directory.
    """

    execution_start_time = time.perf_counter()
    results_dir = create_results_dir(SYNTHETIC_RESULTS_BASE_DIR_PATH)

    # Stage 1: Obtain candidate thresholds for each network family.
    family_dirs = get_family_dirs(SYNTHETIC_NETWORKS_BASE_DIR_PATH)

    for family_idx, family_dir in enumerate(family_dirs, start=1):
        log_progress(family_idx, len(family_dirs), family_dir.name, 4, True)

        family_results_dir = create_dir(os.path.join(results_dir, family_dir.name))
        network_names = sorted({f.stem for f in family_dir.iterdir() if f.suffix not in {".txt", ".json"}})
        output_file = os.path.join(family_results_dir, RAW_CONTRIBUTIONS_FILENAME)

        with open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
            writer = csv.writer(out_file)
            writer.writerow(RAW_CONTRIBUTIONS_FIELDNAMES)

            for network_name_idx, network_name in enumerate(network_names, start=1):
                log_progress(network_name_idx, len(network_names), network_name, 2)
                try:
                    graph, _, k = load_lfr_benchmark_network(
                        dir_path=os.path.join(SYNTHETIC_NETWORKS_BASE_DIR_PATH, family_dir.name), filename=network_name
                    )
                    A = compute_adjacency_matrix(graph)
                    W = np.asarray(A if not config.apply_lapin else lapin(A), dtype=np.float64)

                    if config.use_desired_k:
                        _, contributions, _, _, _, _ = faddis(W=W, desired_k=k + 1 if not config.apply_lapin else k)
                    else:
                        _, contributions, _, _, _, _ = faddis(W=W, epsilon=-np.inf, tau=-np.inf, k_max=1000)

                    writer.writerow([network_name, k] + list(contributions))

                    out_file.flush()
                    os.fsync(out_file.fileno())
                except Exception as e:
                    print(f"[ERROR] {e}")
                    continue

    save_normalized_contributions_and_draw_line_plots(
        results_dir=results_dir,
        input_filename=RAW_CONTRIBUTIONS_FILENAME,
        output_filename=NORMALIZED_CONTRIBUTIONS_FILENAME,
        output_fieldnames=NORMALIZED_CONTRIBUTIONS_FIELDNAMES,
        number_of_columns_to_skip=len(RAW_CONTRIBUTIONS_FIELDNAMES)
    )
    save_statistics_and_draw_histograms(
        results_dir=results_dir,
        input_filename=NORMALIZED_CONTRIBUTIONS_FILENAME,
        statistics_output_filename=STATISTICS_FILENAME,
        statistics_output_fieldnames=STATISTICS_FIELDNAMES,
        histogram_output_filename=HISTOGRAM_FILENAME,
        number_of_columns_to_skip=len(NORMALIZED_CONTRIBUTIONS_FIELDNAMES)
    )
    draw_boxplot(
        results_dir=results_dir,
        input_filename=NORMALIZED_CONTRIBUTIONS_FILENAME,
        output_filename=BOXPLOT_FILENAME,
        number_of_columns_to_skip=len(NORMALIZED_CONTRIBUTIONS_FIELDNAMES)
    )
    draw_line_plot(
        results_dir=results_dir,
        input_filename=STATISTICS_FILENAME,
        output_filename=LINE_PLOT_FILENAME
    )
    save_candidate_thresholds(
        results_dir=results_dir,
        input_filename=STATISTICS_FILENAME,
        output_filename=CANDIDATE_THRESHOLDS_FILENAME,
        output_fieldnames=CANDIDATE_THRESHOLDS_FIELDNAMES
    )

    # Stage 2: Choose one of the candidate thresholds for each network family.
    selected_thresholds_using_bootstrap_and_mse(
        results_dir=results_dir,
        raw_contributions_input_filename=RAW_CONTRIBUTIONS_FILENAME,
        candidate_thresholds_input_filename=CANDIDATE_THRESHOLDS_FILENAME,
        bootstrap_statistics_output_filename=BOOTSTRAP_STATISTICS_FILENAME,
        bootstrap_statistics_output_fieldnames=BOOTSTRAP_STATISTICS_FIELDNAMES,
        thresholds_output_filename=SELECTED_THRESHOLDS_FILENAME,
        thresholds_output_fieldnames=SELECTED_THRESHOLDS_FIELDNAMES,
        maximum_number_of_bootstraps=config.bootstrapping_maximum_number_of_repetitions,
        subsample_fraction=config.bootstrapping_subsample_fraction
    )

    # Generate report.
    execution_elapsed_time = time.perf_counter() - execution_start_time
    save_experiment_report(results_dir, REPORT_FILENAME, config, family_dirs, execution_elapsed_time)

    return results_dir
