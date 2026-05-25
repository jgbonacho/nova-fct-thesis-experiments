import csv
import json
import math
import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from sklearn.utils import resample

from experiments.utils.network_config_dataclass import NetworkConfig


def create_results_dir(base_dir: str) -> str:
    """
    Create a directory to store results, named with the current timestamp.

    Parameters:
        base_dir : (str)
            The base directory for the results.

    Returns:
        results_dir : (str)
            Path to the created results' directory.

    Saves:
        A new directory within 'base_dir' named "results_YYYY-MM-DD_HH-MM-SS-ffffff".
    """

    os.makedirs(base_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
    results_dir_name = f"results_{timestamp}"
    results_dir = os.path.join(base_dir, results_dir_name)
    os.makedirs(results_dir)

    return results_dir


def log_progress(
        current_step: int,
        total_steps: int,
        item_label: str,
        indent_level: int,
        empty_line: bool = False
) -> None:
    """
    Log a progress message to the console with a specific format.

    Parameters:
        current_step : (int)
            The current step.
        total_steps : (int)
            The total number of steps.
        item_label : (str)
            The label of the item being processed.
        indent_level : (int)
            The level of indentation (number of '#' characters).
        empty_line : (bool, optional)
            Whether to print an empty line before the progress log.
            Default is False.
    """

    prefix = "\n" if empty_line else ""
    print(f"{prefix}{indent_level * '#'} [{current_step}/{total_steps}] '{item_label}'")


def save_normalized_contributions_and_draw_line_plots(
        results_dir: str,
        input_filename: str,
        output_filename: str,
        number_of_columns_to_skip: int = 2
) -> float:
    """
    For each network family, save normalized contributions to a new CSV file and draw line plots for each network.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input CSV file containing raw contributions.
        output_filename : (str)
            The name of the output CSV file to save normalized contributions.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.
            Default is 2, assuming the first two columns are "Network" and "K".

    Returns:
        global_sum : (float)
            The global sum of contributions across all networks and families, used for normalization.

    Saves:
        Normalized contributions to 'output_filename' and line plots for each network, within each network family directory.
    """

    # network_family_dirs = sorted(
    #    [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
    #    key=lambda path: path.name
    # )
    # for network_family_dir in network_family_dirs:
    #    family_sum = 0.0
    #    with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
    #        reader = csv.reader(in_file)
    #        next(reader, None)
    #        for row in reader:
    #            values = [float(x) for x in row[number_of_columns_to_skip:]]
    #            family_sum += sum(values)
    #
    #    with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file, \
    #            open(os.path.join(network_family_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
    #        reader = csv.reader(in_file)
    #        next(reader, None)
    #        writer = csv.writer(out_file)
    #        writer.writerow(["Network", "K"])
    #        for row in reader:
    #            values = [float(x) for x in row[number_of_columns_to_skip:]]
    #            normalized_values = [value / family_sum for value in values]
    #            writer.writerow(row[:number_of_columns_to_skip] + normalized_values)
    #
    #            _draw_normalized_contributions_line_plot(network_family_dir, row[0], row[1], normalized_values)

    global_sum = 0.0

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )
    for network_family_dir in network_family_dirs:
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            next(reader, None)
            for row in reader:
                values = [float(x) for x in row[number_of_columns_to_skip:]]
                global_sum += sum(values)

    for network_family_dir in network_family_dirs:
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file, \
                open(os.path.join(network_family_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
            reader = csv.reader(in_file)
            next(reader, None)
            writer = csv.writer(out_file)
            writer.writerow(["Network", "K"])
            for row in reader:
                values = [float(x) for x in row[number_of_columns_to_skip:]]
                normalized_values = [value / global_sum for value in values]
                writer.writerow(row[:number_of_columns_to_skip] + normalized_values)

                _draw_normalized_contributions_line_plot(network_family_dir, row[0], row[1], normalized_values)

    return global_sum


def _draw_normalized_contributions_line_plot(
        results_dir: Path,
        network_name: str,
        k: str,
        normalized_values: list[float]
) -> None:
    """
    Draw a line plot of normalized contributions for a single network, highlighting the contribution at K.
    
    Parameters:
        results_dir : (Path)
            The path to the results' directory.
        network_name : (str)
            The name of the network (used for labeling and saving the plot).
        k : (str)
            The value of k to highlight on the plot.
        normalized_values : (list[float])
            The list of normalized contribution values to plot.
    
    Saves:
        A line plot saved as "{network_name}.pdf" in the specified results' directory.
    """

    x_values = list(range(1, len(normalized_values) + 1))
    y_values = normalized_values

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, marker="o")

    if k != '':
        k_int = int(k)
        if k_int in x_values:
            y_k = y_values[k_int - 1]
            plt.axvline(x=k_int, linestyle="--", alpha=0.7)
            plt.scatter([k_int], [y_k], s=80, zorder=5)
            plt.annotate(f"K", xy=(k_int, y_k), xytext=(5, 8), textcoords="offset points")

    plt.xlabel("Extraction Number")
    plt.ylabel("Normalized Contribution")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f"{network_name}.pdf"), dpi=200)
    plt.close()


def save_statistics_and_draw_histograms(
        results_dir: str,
        input_filename: str,
        statistics_output_filename: str,
        histogram_output_filename: str,
        number_of_columns_to_skip: int = 2
) -> None:
    """
    For each network family, compute statistics of normalized contributions, save them to a CSV file, and draw histograms.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input CSV file containing normalized contributions.
        statistics_output_filename : (str)
            The name of the output CSV file to save computed statistics.
        histogram_output_filename : (str)
            The name of the output file to save the histogram plot for each network family.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.
            Default is 2, assuming the first two columns are "Network" and "K".
    
    Saves:
        A CSV file with computed statistics for each network family and histogram plots for each family, within each network family directory.
    """

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )
    with open(os.path.join(results_dir, statistics_output_filename), "w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Network Family", "#Networks", "Mean", "Std", "Median", "75%", "90%", "95%", "Min", "Max"])

        for network_family_dir in network_family_dirs:
            normalized_values = []
            number_of_networks = 0
            with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
                reader = csv.reader(in_file)
                next(reader, None)
                for row in reader:
                    network_normalized_values = [float(x) for x in row[number_of_columns_to_skip:]]
                    normalized_values.extend(network_normalized_values)
                    number_of_networks += 1

            mean, std, median, p75, p90, p95, min_value, max_value = _compute_statistics(normalized_values)
            writer.writerow([
                network_family_dir.name, number_of_networks, mean, std, median, p75, p90, p95, min_value, max_value,
            ])
            _draw_histogram(
                network_family_dir, histogram_output_filename, normalized_values, mean, std, median, p75, p90, p95
            )


def _compute_statistics(
        normalized_values: list[float]
) -> tuple[float, float, float, float, float, float, float, float]:
    """
    Compute statistics (mean, std, median, percentiles, min, max) for a list of normalized values.
    
    Parameters:
        normalized_values : (list[float])
            The list of normalized contribution values to compute statistics for.
    
    Returns:
        statistics : (tuple[float, float, float, float, float, float, float, float])
            A tuple containing the computed statistics: (mean, std, median, p75, p90, p95, min_value, max_value).    
    """

    sorted_values = sorted(normalized_values)
    n = len(sorted_values)

    mean = sum(sorted_values) / n
    variance = sum((x - mean) ** 2 for x in sorted_values) / (n - 1)  # Sample variance
    std = math.sqrt(variance)
    median = (sorted_values[n // 2] if n % 2 == 1 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2)
    p75 = _percentile(sorted_values, 0.75)
    p90 = _percentile(sorted_values, 0.90)
    p95 = _percentile(sorted_values, 0.95)
    min_value = sorted_values[0]
    max_value = sorted_values[-1]

    return mean, std, median, p75, p90, p95, min_value, max_value


def _percentile(sorted_values: list[float], p: float) -> float:
    """
    Compute the p-th percentile of a sorted list of values using linear interpolation.
    
    Parameters:
        sorted_values : (list[float])
            A list of values sorted in ascending order.
        p : (float)
            The desired percentile to compute (between 0 and 1).
        
    Returns:
        percentile_value : (float)
            The p-th percentile value.
    """

    k = (len(sorted_values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_values[int(k)]

    return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)


def _draw_histogram(
        results_dir: Path,
        output_filename: str,
        normalized_values: list[float],
        mean: float,
        std: float,
        median: float,
        p75: float,
        p90: float,
        p95: float
) -> None:
    """
    Draw a histogram of normalized contributions for a network family, highlighting key statistics.
    
    Parameters:
        results_dir : (Path)
            The path to the results' directory.
        output_filename : (str)
            The name of the output file to save the histogram plot.
        normalized_values : (list[float])
            The list of normalized contribution values to plot.
        mean : (float)
            The mean of the normalized contributions.
        std : (float)
            The standard deviation of the normalized contributions.
        median : (float)
            The median of the normalized contributions.
        p75 : (float)
            The 75th percentile of the normalized contributions.
        p90 : (float)
            The 90th percentile of the normalized contributions.
        p95 : (float)
            The 95th percentile of the normalized contributions.
    
    Saves:
        A histogram plot saved as "{output_filename}" in the specified results directory, with shaded areas and lines indicating key statistics.
    """

    plt.figure(figsize=(8, 5))
    plt.hist(normalized_values, bins=30, edgecolor="black")

    plt.axvspan(
        mean - std,
        mean + std,
        alpha=0.15,
        color="gray",
        label=f"mean ± std = [{mean - std:.6f}, {mean + std:.6f}]"
    )

    for threshold_value, threshold_label, threshold_color in [
        (mean, "mean", "purple"),
        (median, "median", "orange"),
        (p75, "75%", "red"),
        (p90, "90%", "green"),
        (p95, "95%", "blue"),
    ]:
        plt.axvline(
            threshold_value,
            linestyle="--",
            linewidth=1.5,
            color=threshold_color,
            label=f"{threshold_label} = {threshold_value:.6f}"
        )

    plt.xlabel("Normalized Contribution")
    plt.ylabel("Frequency")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def draw_boxplot(results_dir: str, input_filename: str, output_filename: str, number_of_columns_to_skip: int = 2):
    """
    Draw a boxplot of normalized contributions for each network family.
    
    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input file containing normalized contribution values.
        output_filename : (str)
            The name of the output file to save the boxplot.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip in the input file.
            Default is 2, assuming the first two columns are "Network" and "K".
    
    Saves:
        A boxplot saved as "{output_filename}" in the specified results directory, comparing normalized contributions across different network families.
    """

    boxplot_data = []
    boxplot_labels = []

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )
    for network_family in network_family_dirs:
        normalized_values = []
        with (open(os.path.join(results_dir, network_family, input_filename), "r", newline="", encoding="utf-8")
              as in_file):
            reader = csv.reader(in_file)
            next(reader, None)
            for row in reader:
                normalized_values.extend(float(x) for x in row[number_of_columns_to_skip:])
        boxplot_data.append(normalized_values)
        boxplot_labels.append(network_family.name)

    plt.figure(figsize=(10, 4.5))
    plt.boxplot(boxplot_data, labels=boxplot_labels, patch_artist=True)
    plt.xlabel("Network Family")
    plt.ylabel("Normalized Contribution")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def draw_line_plot(results_dir: str, input_filename: str, output_filename: str) -> None:
    """
    Draw a line plot of mean normalized contributions with error bars for each network family, along with median and percentiles.
    
    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input file containing statistics of normalized contributions.
        output_filename : (str)
            The name of the output file to save the line plot.
    
    Saves:
        A line plot saved as "{output_filename}" in the specified results directory, showing mean normalized contributions with error bars, and lines for median and percentiles for each network family.
    """

    families = []
    means = []
    stds = []
    medians = []
    p75s = []
    p90s = []
    p95s = []
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            families.append(row["Network Family"])
            means.append(float(row["Mean"]))
            stds.append(float(row["Std"]))
            medians.append(float(row["Median"]))
            p75s.append(float(row["75%"]))
            p90s.append(float(row["90%"]))
            p95s.append(float(row["95%"]))

    plt.figure(figsize=(10, 4.5))

    plt.errorbar(
        families,
        means,
        yerr=stds,
        fmt="o-",
        capsize=4,
        label="mean ± std"
    )

    plt.plot(families, medians, marker="s", label="median")
    plt.plot(families, p75s, marker="^", label="75%")
    plt.plot(families, p90s, marker="D", label="90%")
    plt.plot(families, p95s, marker="x", label="95%")

    plt.xlabel("Network Family")
    plt.ylabel("Normalized Contribution")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def save_candidate_thresholds(
        results_dir: str,
        input_filename: str,
        output_filename: str,
        threshold_metrics: tuple
) -> None:
    """
    Save candidate thresholds for each network family to a new CSV file, based on specified threshold metrics.
    
    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input file containing statistics of normalized contributions.
        output_filename : (str)
            The name of the output file to save the candidate thresholds.
        threshold_metrics : (tuple)
            The list of threshold metrics to extract from the input file (e.g., ("Mean", "Median", "75%", "90%", "95%")).

    Saves:
        A CSV file saved as "{output_filename}" in the specified results directory, containing candidate thresholds for each network family based on the specified threshold metrics.        
    """

    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file, \
            open(os.path.join(results_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
        reader = csv.DictReader(in_file)
        writer = csv.writer(out_file)

        writer.writerow(["Network Family"] + list(threshold_metrics))
        for row in reader:
            threshold_values = []
            for threshold_metric in threshold_metrics:
                threshold_values.append(row[threshold_metric])
            writer.writerow([row["Network Family"]] + threshold_values)


def selected_thresholds_using_bootstrap_and_mse(
        results_dir: str,
        raw_contributions_input_filename: str,
        candidate_thresholds_input_filename: str,
        bootstrap_statistics_output_filename: str,
        thresholds_output_filename: str,
        threshold_metrics: tuple,
        maximum_number_of_bootstraps: int = 1000,
        subsample_fraction: float = 0.8,
        number_of_columns_to_skip: int = 2
) -> None:
    """
    For each network family, perform bootstrapping to compute new thresholds and their MSE against pre-computed candidate thresholds, then select the best threshold metric based on MSE.
    
    Parameters:
        results_dir : (str)
            The path to the results' directory.
        raw_contributions_input_filename : (str)
            The name of the input file containing raw contributions for each network.
        candidate_thresholds_input_filename : (str)
            The name of the input file containing pre-computed candidate thresholds for each network family.
        bootstrap_statistics_output_filename : (str)
            The name of the output file to save bootstrap statistics, including MSE for each threshold metric.
        thresholds_output_filename : (str)
            The name of the output file to save the selected threshold metric and value for each network family.
        threshold_metrics : (tuple)
            The list of threshold metrics to evaluate (e.g., ("Mean", "Median", "75%", "90%", "95%")).
        maximum_number_of_bootstraps : (int, optional)
            The maximum number of bootstrap iterations to perform. 
            Default is 1000.
        subsample_fraction : (float, optional)
            The fraction of networks to include in each bootstrap sample. 
            Default is 0.8.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values in the input file. 
            Default is 2, assuming the first two columns are "Network" and "K".
    
    Saves:
        A CSV file with bootstrap statistics and MSE for each threshold metric,
        and a CSV file with the selected threshold metric and value for each network family, both within the specified results' directory.
    """

    candidate_thresholds_by_family = _load_candidate_thresholds(
        results_dir, candidate_thresholds_input_filename, threshold_metrics
    )

    with open(os.path.join(results_dir, bootstrap_statistics_output_filename), "w", newline="",
              encoding="utf-8") as bootstrap_out_file, \
            open(os.path.join(results_dir, thresholds_output_filename), "w", newline="",
                 encoding="utf-8") as thresholds_out_file:
        bootstrap_writer = csv.writer(bootstrap_out_file)
        thresholds_writer = csv.writer(thresholds_out_file)

        bootstrap_writer.writerow([
            "Network Family",
            "#Networks",
            "Subsample Size",
            "#Bootstraps",
            "Metric",
            "Candidate Threshold",
            "MSE"
        ])
        thresholds_writer.writerow([
            "Network Family",
            "Selected Metric",
            "Threshold",
        ])

        network_family_dirs = sorted(
            [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
            key=lambda path: path.name
        )
        for network_family_dir in network_family_dirs:
            network_raw_contributions = _load_network_contributions(
                network_family_dir, raw_contributions_input_filename, number_of_columns_to_skip
            )
            number_of_networks = len(network_raw_contributions)
            subsample_size = math.ceil(subsample_fraction * number_of_networks)

            number_of_bootstraps = 0
            squared_errors_by_metric = {threshold_metric: [] for threshold_metric in threshold_metrics}

            candidate_thresholds = candidate_thresholds_by_family[network_family_dir.name]
            for bootstrap_idx in range(maximum_number_of_bootstraps):
                sampled_indices = _bootstrapping(
                    number_of_networks=number_of_networks,
                    with_replacement=True,
                    sample_size=subsample_size,
                    random_seed=bootstrap_idx
                )
                contributions = _get_contributions(network_raw_contributions, sampled_indices)
                normalized_contributions = _normalize_contributions(contributions)
                current_thresholds = _compute_candidate_thresholds(normalized_contributions, threshold_metrics)

                for threshold_metric in threshold_metrics:
                    candidate_threshold = candidate_thresholds[threshold_metric]
                    current_threshold = current_thresholds[threshold_metric]
                    squared_error = (candidate_threshold - current_threshold) ** 2
                    squared_errors_by_metric[threshold_metric].append(squared_error)

                number_of_bootstraps += 1

            selected_threshold_metric = None
            selected_threshold_value = None
            selected_threshold_mse = np.inf

            for threshold_metric in threshold_metrics:
                candidate_threshold = candidate_thresholds[threshold_metric]
                squared_errors = squared_errors_by_metric[threshold_metric]
                mse = sum(squared_errors) / len(squared_errors)

                bootstrap_writer.writerow([
                    network_family_dir.name,
                    number_of_networks,
                    subsample_size,
                    number_of_bootstraps,
                    threshold_metric,
                    candidate_threshold,
                    mse
                ])

                if candidate_threshold > 0 and mse < selected_threshold_mse:
                    selected_threshold_mse = mse
                    selected_threshold_metric = threshold_metric
                    selected_threshold_value = candidate_threshold

            thresholds_writer.writerow([
                network_family_dir.name,
                selected_threshold_metric,
                selected_threshold_value
            ])


def _load_candidate_thresholds(
        results_dir: str,
        input_filename: str,
        threshold_metrics: tuple
) -> dict[str, dict[str, float]]:
    """
    Load pre-computed candidate thresholds for each network family from a CSV file.
    
    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input file containing candidate thresholds for each network family.
        threshold_metrics : (tuple)
            A list of threshold metrics to be loaded from the CSV file.
    Returns:
        candidate_thresholds_by_family : (dict[str, dict[str, float]])
            A dictionary mapping each network family to its corresponding candidate thresholds.
    """

    candidate_thresholds_by_family = {}
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            candidate_thresholds_by_family[row["Network Family"]] = {
                threshold_metric: float(row[threshold_metric]) for threshold_metric in threshold_metrics
            }
    return candidate_thresholds_by_family


def _load_network_contributions(
        results_dir: Path,
        input_filename: str,
        number_of_columns_to_skip: int = 2
) -> list[list[float]]:
    """
    Load raw contributions for each network from a CSV file, skipping the specified number of initial columns.

    Parameters:
        results_dir : (Path)
            The path to the results' directory.
        input_filename : (str)
            The name of the input file containing raw contributions for each network.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values in the input file. 
            Default is 2, assuming the first two columns are "Network" and "K".
    
    Returns:
        network_raw_contributions : (list[list[float]])
            A list of lists, where each inner list contains the raw contribution values for a single network.
    """

    network_raw_contributions = []
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        next(reader, None)
        for row in reader:
            contributions = [float(x) for x in row[number_of_columns_to_skip:]]
            network_raw_contributions.append(contributions)
    return network_raw_contributions


def _bootstrapping(number_of_networks: int, with_replacement: bool, sample_size: int, random_seed: int) -> list[int]:
    """
    Perform bootstrapping by sampling indices of networks with or without replacement.

    Parameters:
        number_of_networks : (int)
            The total number of networks available for sampling.
        with_replacement : (bool)
            Whether to sample with replacement (True) or without replacement (False).
        sample_size : (int)
            The number of samples to draw in each bootstrap iteration.
        random_seed : (int)
            The random seed to ensure reproducibility of the sampling process.
    
    Returns:
        sampled_indices : (list[int])
            A list of sampled indices corresponding to the selected networks for the bootstrap iteration.
    """

    return resample(
        list(range(number_of_networks)),
        replace=with_replacement,
        n_samples=sample_size,
        random_state=random_seed
    )


def _get_contributions(network_contributions: list[list[float]], selected_indices: list[int]) -> list[float]:
    """
    Retrieve contributions for the selected network indices.

    Parameters:
        network_contributions : (list[list[float]])
            A list of lists, where each inner list contains the raw contribution values for a single network.
        selected_indices : (list[int])
            A list of indices corresponding to the selected networks.

    Returns:
        contributions : (list[float])
            A list of contributions for the selected networks.
    """

    contributions = []
    for idx in selected_indices:
        contributions.extend(network_contributions[idx])
    return contributions


def _normalize_contributions(contributions: list[float]) -> list[float]:
    """
    Normalize the contributions so that they sum to 1.

    Parameters:
        contributions : (list[float])
            A list of contribution values.

    Returns:
        normalized_contributions : (list[float])
            A list of normalized contribution values.
    """

    total = sum(contributions)
    return [value / total for value in contributions]


def _compute_candidate_thresholds(normalized_values: list[float], threshold_metrics: tuple) -> dict[str, float]:
    """
    Compute candidate thresholds based on specified threshold metrics from a list of normalized contribution values.
    
    Parameters:
        normalized_values : (list[float])
            A list of normalized contribution values to compute candidate thresholds from.
        threshold_metrics : (tuple)
            A list of threshold metrics to compute (e.g., ("Mean", "Median", "75%", "90%", "95%")).
    
    Returns:
        thresholds : (dict[str, float])
            A dictionary mapping each specified threshold metric to its computed value based on the normalized contribution values.
    """

    mean, _, median, p75, p90, p95, _, _ = _compute_statistics(normalized_values)
    thresholds = {
        "Mean": mean,
        "Median": median,
        "75%": p75,
        "90%": p90,
        "95%": p95
    }

    return {threshold_metric: thresholds[threshold_metric] for threshold_metric in threshold_metrics}


def save_experiment_report(
        results_dir: str,
        output_filename: str,
        apply_lapin: bool,
        use_desired_k: bool,
        network_family_dirs: list[Path],
) -> None:
    """
    Save a report of the experiment settings to a JSON file.
    
    Parameters:
        results_dir : (str)
            The path to the results' directory.
        output_filename : (str)
            The name of the output file to save the report.
        apply_lapin : (bool)
            Whether Lapin's transformation was applied in the experiment.
        use_desired_k : (bool)
            Whether the desired number of communities was used in the experiment.
        network_family_dirs : (list[Path])
            A list of Path objects representing the directories of network families included in the experiment.
    
    Saves:
        A JSON file saved as "{output_filename}" in the specified results directory, containing a report of the experiment settings.
    """

    report = {
        "apply_lapin": apply_lapin,
        "use_desired_k": use_desired_k,
        "number_of_families": len(network_family_dirs),
        "families": [directory.name for directory in network_family_dirs]
    }

    with open(os.path.join(results_dir, output_filename), "w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)


def load_real_world_network_configs(network_directory: Path, input_filename: str) -> list[NetworkConfig]:
    """
    Load real-world network configs from a JSON file.

    Parameters:
        network_directory : (Path)
            The path to the directory containing the JSON file.
        input_filename : (str)
            The name of the input JSON file, without the ".json" extension.

    Returns:
        networks : (list[NetworkConfig])
             A list of NetworkConfig objects loaded from the JSON file.
    """

    with open(os.path.join(network_directory, f"{input_filename}.json"), "r", encoding="utf-8") as in_file:
        json_networks = json.load(in_file)

    return [NetworkConfig.from_dict(json_network) for json_network in json_networks]


def compute_real_world_network_properties(
        network_name: str,
        graph: nx.Graph,
        ground_truth_labels: list,
        k: int,
        ground_truth: bool,
        overlapping_ground_truth: bool
) -> dict:
    """
    Compute properties (structural and ground-truth) of a real-world network.

    Parameters:
        network_name : (str)
            The network name.
        graph : (nx.Graph)
            The preprocessed graph. It is assumed that this graph is already the LCC.
        ground_truth_labels : (list[int] | list[list[int]] | None)
            The ground-truth labels.
        k : (int | None)
            The number of ground-truth communities.
        ground_truth : (bool)
            Whether the network has ground-truth labels.
        overlapping_ground_truth : (bool)
            Whether the ground-truth labels are overlapping.

    Returns:
        properties : (dict)
            Dictionary with structural network properties.
    """

    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()

    degrees = np.asarray([degree for _, degree in graph.degree()], dtype=np.float64)
    min_degree = float(np.min(degrees)) if nodes > 0 else None
    max_degree = float(np.max(degrees)) if nodes > 0 else None
    average_degree = float(np.mean(degrees)) if nodes > 0 else None
    degree_std = float(np.std(degrees, ddof=1)) if nodes > 1 else 0.0
    degree_cv = (
        degree_std / average_degree
        if average_degree is not None and average_degree > 0
        else None
    )
    degree_hub_ratio = (
        max_degree / average_degree
        if max_degree is not None and average_degree is not None and average_degree > 0
        else None
    )

    density = nx.density(graph) if nodes > 1 else 0.0
    sparsity = 1.0 - density
    global_clustering_coefficient = nx.transitivity(graph) if nodes > 0 else None
    degree_assortativity = float(nx.degree_assortativity_coefficient(graph))
    average_clustering = nx.average_clustering(graph) if nodes > 0 else None

    (
        min_community_size,
        max_community_size,
        average_community_size,
        community_size_std,
        community_size_cv,
        nodes_without_community,
        nodes_fraction_without_community,
        overlap_fraction
    ) = _compute_ground_truth_properties(ground_truth_labels, overlapping_ground_truth, nodes)

    return {
        "Network": network_name,
        "Ground-Truth?": ground_truth,
        "Nodes LCC": nodes,
        "Edges LCC": edges,
        "Min Degree": min_degree,
        "Max Degree": max_degree,
        "Average Degree": average_degree,
        "Degree Std": degree_std,
        "Degree CV": degree_cv,
        "Degree Hub Ratio": degree_hub_ratio,
        "Density": density,
        "Sparsity": sparsity,
        "Global Clustering Coefficient": global_clustering_coefficient,
        "Degree Assortativity": degree_assortativity,
        "Average Clustering": average_clustering,
        "Overlapping Ground-Truth?": overlapping_ground_truth,
        "Overlap Fraction": overlap_fraction,
        "K": k,
        "Community Proportion": k / nodes if k is not None and nodes > 0 else None,
        "Min Community Size": min_community_size,
        "Max Community Size": max_community_size,
        "Average Community Size": average_community_size,
        "Community Size Std": community_size_std,
        "Community Size CV": community_size_cv,
        "Nodes Without Community": nodes_without_community,
        "Nodes Fraction Without Community": nodes_fraction_without_community
    }


def _compute_ground_truth_properties(
        ground_truth_labels: list,
        overlapping_ground_truth: bool,
        nodes: int
) -> tuple[float, float, float, float, float, int, float, float]:
    """
    Compute ground-truth community properties.

    Parameters:
        ground_truth_labels : (list[int] | list[list[int]] | None)
            The ground-truth labels.
        overlapping_ground_truth : (bool)
            Whether the ground-truth labels are overlapping.
        nodes : (int)
            The number of nodes.

    Returns:
        min_community_size : (float | None)
            Minimum community size.
        max_community_size : (float | None)
            Maximum community size.
        average_community_size : (float | None)
            Average community size.
        community_size_std : (float | None)
            Standard deviation of community sizes.
        community_size_cv : (float | None)
            Coefficient of variation of community sizes.
        nodes_without_community : (int | None)
            Number of nodes without ground-truth community.
        nodes_fraction_without_community : (float | None)
            Fraction of nodes without ground-truth community.
        overlap_fraction : (float | None)
            Fraction of labeled nodes that belong to more than one community.
    """

    if ground_truth_labels is None or nodes == 0:
        return None, None, None, None, None, None, None, None

    community_sizes = {}
    nodes_without_community = 0
    overlapping_nodes = 0
    labeled_nodes = 0

    if not overlapping_ground_truth:
        for label in ground_truth_labels:
            if label == -1:
                nodes_without_community += 1
                continue

            labeled_nodes += 1
            community_sizes[label] = community_sizes.get(label, 0) + 1

        overlap_fraction = 0.0

    else:
        for labels in ground_truth_labels:
            if labels == [-1] or len(labels) == 0:
                nodes_without_community += 1
                continue

            valid_labels = [label for label in labels if label != -1]

            if len(valid_labels) == 0:
                nodes_without_community += 1
                continue

            labeled_nodes += 1

            if len(valid_labels) > 1:
                overlapping_nodes += 1

            for label in valid_labels:
                community_sizes[label] = community_sizes.get(label, 0) + 1

        overlap_fraction = overlapping_nodes / labeled_nodes if labeled_nodes > 0 else None

    sizes = np.asarray(list(community_sizes.values()), dtype=np.float64)

    if len(sizes) == 0:
        min_community_size = None
        max_community_size = None
        average_community_size = None
        community_size_std = None
        community_size_cv = None
    else:
        min_community_size = float(np.min(sizes))
        max_community_size = float(np.max(sizes))
        average_community_size = float(np.mean(sizes))
        community_size_std = float(np.std(sizes, ddof=1)) if len(sizes) > 1 else 0.0
        community_size_cv = (
            community_size_std / average_community_size
            if average_community_size > 0
            else None
        )

    nodes_fraction_without_community = nodes_without_community / nodes

    return (
        min_community_size,
        max_community_size,
        average_community_size,
        community_size_std,
        community_size_cv,
        nodes_without_community,
        nodes_fraction_without_community,
        overlap_fraction
    )


def selected_thresholds_using_a_statistic_metric(
        results_dir: str,
        candidate_thresholds_input_filename: str,
        thresholds_output_filename: str,
        statistics_metric: str = "Median"
) -> None:
    """
    Select thresholds using a fixed statistic metric.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        candidate_thresholds_input_filename : (str)
            The name of the input CSV file containing candidate thresholds.
        thresholds_output_filename : (str)
            The name of the output CSV file to save the selected thresholds.
        statistics_metric : (str, optional)
            The statistic metric used to select the threshold.
            Default is "Median".

    Saves:
        A CSV file with the selected threshold for each network family.
    """

    with open(os.path.join(results_dir, candidate_thresholds_input_filename), "r", newline="",
              encoding="utf-8") as in_file, \
            open(os.path.join(results_dir, thresholds_output_filename), "w", newline="",
                 encoding="utf-8") as out_file:
        reader = csv.DictReader(in_file)
        writer = csv.writer(out_file)
        writer.writerow(["Network Family", "Selected Metric", "Threshold"])

        for row in reader:
            writer.writerow([row["Network Family"], statistics_metric, row[statistics_metric]])


def draw_sorted_k_contributions_bar_plot(
        results_dir: str,
        input_filename: str,
        output_filename: str,
        remove_first_contribution: bool = False,
        number_of_columns_to_skip: int = 2
) -> None:
    """
    Draw a bar plot of the normalized contribution at K for each network.

    If 'remove_first_contribution' is True, the first extracted contribution is ignored.
    In that case, the effective c_K corresponds to the original c_{K+1}.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input CSV file containing normalized contributions.
        output_filename : (str)
            The name of the output file to save the bar plot.
        remove_first_contribution : (bool, optional)
            Whether to remove the first contribution before selecting c_K.
            This is useful for LAPIN-off, where the first contribution may behave as a global/background component.
            Default is False.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.
            Default is 2, assuming the first two columns are "Network" and "K".

    Saves:
        A sorted bar plot of normalized c_K values across all networks.
    """

    k_contribution_rows = []

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )
    for network_family_dir in network_family_dirs:
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            next(reader, None)

            for row in reader:
                network_name = row[0]
                k = _parse_optional_int(row[1])
                contributions = [float(x) for x in row[number_of_columns_to_skip:] if x != ""]

                if k is None:
                    continue

                if remove_first_contribution and len(contributions) > 0:
                    effective_contributions = contributions[1:]
                else:
                    effective_contributions = contributions

                if len(effective_contributions) < k:
                    continue

                k_contribution = effective_contributions[k - 1]

                k_contribution_rows.append({
                    "family": network_family_dir.name,
                    "network": network_name,
                    "k": k,
                    "k_contribution": k_contribution
                })

    k_contribution_rows = sorted(
        k_contribution_rows,
        key=lambda item: item["k_contribution"],
        reverse=True
    )

    labels = [row["network"] for row in k_contribution_rows]
    values = [row["k_contribution"] for row in k_contribution_rows]

    plt.figure(figsize=(max(10, 0.5 * len(values)), 5))
    plt.bar(range(len(values)), values)

    positive_values = [value for value in values if value > 0]
    if len(positive_values) > 0:
        plt.yscale("log")
        plt.ylim(min(positive_values) / 2, max(positive_values) * 2)

    plt.xticks(range(len(values)), labels, rotation=90)
    plt.xlabel("Network")
    plt.ylabel("Normalized Contribution at K")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def _parse_optional_int(value: str) -> int:
    """
    Parse an optional integer value.

    Parameters:
        value : (str)
            The value to parse.

    Returns:
        value : (int | None)
            The parsed integer, or None if the value is empty.
    """

    if value is None or value == "" or value == "None":
        return None

    return int(value)


def save_k_boundary_geometric_mean_thresholds(
        results_dir: str,
        input_filename: str,
        output_by_network_filename: str,
        output_by_family_filename: str,
        remove_first_contribution: bool = False,
        global_sum: float = None,
        number_of_columns_to_skip: int = 2
) -> None:
    """
    Save the K-boundary geometric mean thresholds by network and by family.

    The network-level K-boundary threshold is computed as: threshold = sqrt(c_K * c_K+1),
    where c_K is the contribution of the K-th extracted cluster and c_K+1 is the contribution of the next extracted cluster.

    If the contributions were globally normalized as: normalized_contribution = raw_contribution / global_sum,
    then the raw-scale threshold is recovered as: raw_threshold = normalized_threshold * global_sum.
    
    The family-level threshold is computed as the median of the valid network-level thresholds inside each family.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input CSV file containing normalized contributions.
        output_by_network_filename : (str)
            The name of the output CSV file to save network-level K-boundary thresholds.
        output_by_family_filename : (str)
            The name of the output CSV file to save family-level median K-boundary thresholds.
        remove_first_contribution : (bool, optional)
            Whether to remove the first contribution before computing the K-boundary.
            This is useful for LAPIN-off, where the first contribution may behave as a global/background component.
            Default is False.
        global_sum : (float | None, optional)
            The global sum used to normalize the raw contributions.
            If provided, the function also saves the raw-scale threshold.
            Default is None.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.
            Default is 2, assuming the first two columns are "Network" and "K".

    Saves:
        Two CSV files:
            - one with K-boundary thresholds by network;
            - one with median K-boundary thresholds by family.
    """

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )

    family_rows = {}
    by_network_path = os.path.join(results_dir, output_by_network_filename)
    by_family_path = os.path.join(results_dir, output_by_family_filename)

    with open(by_network_path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow([
            "Network Family",
            "Network",
            "K",
            "First Contribution Removed?",
            "Number of Contributions",
            "Effective Number of Contributions",
            "Normalized c_K",
            "Normalized c_K+1",
            "gap_K",
            "ratio_K",
            "Normalized Threshold",
            "Global Normalization Factor",
            "Raw Threshold",
            "Valid Threshold?"
        ])

        for network_family_dir in network_family_dirs:
            family_rows[network_family_dir.name] = {
                "number_of_networks": 0,
                "number_of_valid_thresholds": 0,
                "normalized_thresholds": [],
                "raw_thresholds": [],
                "gap_values": [],
                "ratio_values": []
            }

            input_path = os.path.join(network_family_dir, input_filename)

            with open(input_path, "r", newline="", encoding="utf-8") as in_file:
                reader = csv.reader(in_file)
                next(reader, None)

                for row in reader:
                    network_name = row[0]
                    k = _parse_optional_int(row[1])
                    contributions = [float(x) for x in row[number_of_columns_to_skip:] if x != ""]

                    family_rows[network_family_dir.name]["number_of_networks"] += 1

                    if remove_first_contribution and len(contributions) > 0:
                        effective_contributions = contributions[1:]
                    else:
                        effective_contributions = contributions

                    if k is None:
                        writer.writerow([
                            network_family_dir.name,
                            network_name,
                            None,
                            remove_first_contribution,
                            len(contributions),
                            len(effective_contributions),
                            None,
                            None,
                            None,
                            None,
                            None,
                            global_sum,
                            None,
                            False
                        ])
                        continue

                    # Need both c_K and c_K+1.
                    if len(effective_contributions) <= k:
                        writer.writerow([
                            network_family_dir.name,
                            network_name,
                            k,
                            remove_first_contribution,
                            len(contributions),
                            len(effective_contributions),
                            None,
                            None,
                            None,
                            None,
                            None,
                            global_sum,
                            None,
                            False
                        ])
                        continue

                    c_k = effective_contributions[k - 1]
                    c_k_plus_1 = effective_contributions[k]

                    gap_k = c_k - c_k_plus_1
                    ratio_k = c_k / c_k_plus_1 if c_k_plus_1 > 0 else np.inf

                    normalized_threshold = np.sqrt(c_k * c_k_plus_1)
                    raw_threshold = (
                        normalized_threshold * global_sum
                        if global_sum is not None
                        else None
                    )

                    valid_threshold = c_k > c_k_plus_1

                    if valid_threshold:
                        family_rows[network_family_dir.name]["number_of_valid_thresholds"] += 1
                        family_rows[network_family_dir.name]["normalized_thresholds"].append(normalized_threshold)
                        family_rows[network_family_dir.name]["gap_values"].append(gap_k)
                        family_rows[network_family_dir.name]["ratio_values"].append(ratio_k)

                        if raw_threshold is not None:
                            family_rows[network_family_dir.name]["raw_thresholds"].append(raw_threshold)

                    writer.writerow([
                        network_family_dir.name,
                        network_name,
                        k,
                        remove_first_contribution,
                        len(contributions),
                        len(effective_contributions),
                        c_k,
                        c_k_plus_1,
                        gap_k,
                        ratio_k,
                        normalized_threshold,
                        global_sum,
                        raw_threshold,
                        valid_threshold
                    ])

    with open(by_family_path, "w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow([
            "Network Family",
            "#Networks",
            "#Valid Thresholds",
            "Median Normalized Threshold",
            "Median Raw Threshold",
            "Median gap_K",
            "Median ratio_K",
            "Threshold"
        ])

        for family_name, values in family_rows.items():
            normalized_thresholds = values["normalized_thresholds"]
            raw_thresholds = values["raw_thresholds"]
            gap_values = values["gap_values"]
            ratio_values = values["ratio_values"]

            median_normalized_threshold = _median_or_none(normalized_thresholds)
            median_raw_threshold = _median_or_none(raw_thresholds)
            median_gap_k = _median_or_none(gap_values)
            median_ratio_k = _median_or_none(ratio_values)

            writer.writerow([
                family_name,
                values["number_of_networks"],
                values["number_of_valid_thresholds"],
                median_normalized_threshold,
                median_raw_threshold,
                median_gap_k,
                median_ratio_k,
                median_raw_threshold
            ])


def _median_or_none(values: list[float]) -> float:
    """
    Compute the median of a list, or return None if the list is empty.

    Parameters:
        values : (list[float])
            The list of values.

    Returns:
        median : (float | None)
            The median value, or None if the list is empty.
    """

    if len(values) == 0:
        return None

    return float(np.median(values))


# def save_k_boundary_geometric_mean_thresholds(
#         results_dir: str,
#         input_filename: str,
#         output_by_network_filename: str,
#         output_by_family_filename: str,
#         remove_first_contribution: bool = False,
#         global_sum: float = None,
#         number_of_columns_to_skip: int = 2
# ) -> None:
#     """
#     Save the K-boundary thresholds by network and by family.

#     The network-level K-boundary threshold is computed as: threshold = sqrt(c_K * c_K+1),
#     where c_K is the contribution of the K-th extracted cluster and c_K+1 is the contribution of the next extracted cluster.

#     The family-level threshold is computed using the common valid threshold interval: max(c_K+1) < threshold < min(c_K).
#     If the common interval exists, the family threshold is computed as: threshold = sqrt(max(c_K+1) * min(c_K)).
#     If the common interval does not exist, an approximate threshold is computed using the same formula: threshold = sqrt(max(c_K+1) * min(c_K)).
#     In this case, the threshold balances the conflict between the family lower bound and upper bound in logarithmic scale,
#     but it is not strictly valid for all networks in the family.

#     If the contributions were globally normalized as: normalized_contribution = raw_contribution / global_sum,
#     then the raw-scale threshold is recovered as: raw_threshold = normalized_threshold * global_sum

#     Parameters:
#         results_dir : (str)
#             The path to the results' directory.
#         input_filename : (str)
#             The name of the input CSV file containing normalized contributions.
#         output_by_network_filename : (str)
#             The name of the output CSV file to save network-level K-boundary thresholds.
#         output_by_family_filename : (str)
#             The name of the output CSV file to save family-level K-boundary thresholds.
#         remove_first_contribution : (bool, optional)
#             Whether to remove the first contribution before computing the K-boundary.
#             This is useful for LAPIN-off, where the first contribution may behave as a global/background component.
#             Default is False.
#         global_sum : (float | None, optional)
#             The global sum used to normalize the raw contributions.
#             If provided, the function also saves the raw-scale threshold.
#             Default is None.
#         number_of_columns_to_skip : (int, optional)
#             The number of columns to skip before reading contribution values.
#             Default is 2, assuming the first two columns are "Network" and "K".

#     Saves:
#         Two CSV files:
#             - one with K-boundary thresholds by network;
#             - one with common-interval or approximate common-interval thresholds by family.
#     """

#     network_family_dirs = sorted(
#         [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
#         key=lambda path: path.name
#     )

#     family_rows = {}
#     by_network_path = os.path.join(results_dir, output_by_network_filename)
#     by_family_path = os.path.join(results_dir, output_by_family_filename)

#     with open(by_network_path, "w", newline="", encoding="utf-8") as out_file:
#         writer = csv.writer(out_file)
#         writer.writerow([
#             "Network Family", "Network", "K",
#             "First Contribution Removed?", "Number of Contributions", "Effective Number of Contributions",
#             "Normalized c_K", "Normalized c_K+1", "gap_K", "ratio_K", "Normalized Threshold",
#             "Global Normalization Factor", "Raw Threshold", "Valid Threshold?"
#         ])

#         for network_family_dir in network_family_dirs:
#             family_rows[network_family_dir.name] = {
#                 "number_of_networks": 0,
#                 "number_of_valid_thresholds": 0,
#                 "normalized_c_k_values": [],
#                 "normalized_c_k_plus_1_values": [],
#                 "gap_values": [],
#                 "ratio_values": []
#             }

#             input_path = os.path.join(network_family_dir, input_filename)

#             with open(input_path, "r", newline="", encoding="utf-8") as in_file:
#                 reader = csv.reader(in_file)
#                 next(reader, None)

#                 for row in reader:
#                     network_name = row[0]
#                     k = _parse_optional_int(row[1])
#                     contributions = [float(x) for x in row[number_of_columns_to_skip:] if x != ""]

#                     family_rows[network_family_dir.name]["number_of_networks"] += 1

#                     if remove_first_contribution and len(contributions) > 0:
#                         effective_contributions = contributions[1:]
#                     else:
#                         effective_contributions = contributions

#                     if k is None:
#                         writer.writerow([
#                             network_family_dir.name, network_name, None,
#                             remove_first_contribution, len(contributions), len(effective_contributions),
#                             None, None, None, None, None,
#                             global_sum, None, False
#                         ])
#                         continue

#                     # Need both c_K and c_K+1.
#                     if len(effective_contributions) <= k:
#                         writer.writerow([
#                             network_family_dir.name, network_name, k,
#                             remove_first_contribution, len(contributions), len(effective_contributions),
#                             None, None, None, None, None,
#                             global_sum, None, False
#                         ])
#                         continue

#                     c_k = effective_contributions[k - 1]
#                     c_k_plus_1 = effective_contributions[k]

#                     gap_k = c_k - c_k_plus_1
#                     ratio_k = c_k / c_k_plus_1 if c_k_plus_1 > 0 else np.inf

#                     normalized_threshold = _interval_midpoint(c_k_plus_1, c_k)
#                     raw_threshold = (normalized_threshold * global_sum if global_sum is not None else None)

#                     valid_threshold = c_k > c_k_plus_1

#                     if valid_threshold:
#                         family_rows[network_family_dir.name]["number_of_valid_thresholds"] += 1
#                         family_rows[network_family_dir.name]["normalized_c_k_values"].append(c_k)
#                         family_rows[network_family_dir.name]["normalized_c_k_plus_1_values"].append(c_k_plus_1)
#                         family_rows[network_family_dir.name]["gap_values"].append(gap_k)
#                         family_rows[network_family_dir.name]["ratio_values"].append(ratio_k)

#                     writer.writerow([
#                         network_family_dir.name, network_name, k,
#                         remove_first_contribution, len(contributions), len(effective_contributions),
#                         c_k, c_k_plus_1, gap_k, ratio_k, normalized_threshold,
#                         global_sum, raw_threshold, valid_threshold
#                     ])

#     with open(by_family_path, "w", newline="", encoding="utf-8") as out_file:
#         writer = csv.writer(out_file)
#         writer.writerow([
#             "Network Family",
#             "#Networks",
#             "#Valid Thresholds",
#             "Normalized c_K Values",
#             "Normalized c_K+1 Values",
#             "Min Normalized c_K",
#             "Max Normalized c_K+1",
#             "Interval Overlaps?",
#             "Family Threshold Mode",
#             "Normalized Threshold",
#             "Global Normalization Factor",
#             "Raw Threshold",
#             "Threshold"
#         ])

#         for family_name, values in family_rows.items():
#             c_k_values = values["normalized_c_k_values"]
#             c_k_plus_1_values = values["normalized_c_k_plus_1_values"]

#             lower_bound_options = c_k_plus_1_values
#             upper_bound_options = c_k_values

#             if len(lower_bound_options) == 0 or len(upper_bound_options) == 0:
#                 family_threshold_mode = "no_valid_interval"
#                 common_interval_exists = False
#                 common_interval_lower_bound = 0
#                 common_interval_upper_bound = 0
#                 normalized_threshold = 0
#                 raw_threshold = 0

#             else:
#                 common_interval_lower_bound = max(lower_bound_options)
#                 common_interval_upper_bound = min(upper_bound_options)

#                 common_interval_exists = common_interval_lower_bound < common_interval_upper_bound

#                 if common_interval_exists:
#                     family_threshold_mode = "common_interval"
#                 else:
#                     family_threshold_mode = "approximate_common_interval"

#                 normalized_threshold = _interval_midpoint(common_interval_lower_bound, common_interval_upper_bound)

#                 raw_threshold = (normalized_threshold * global_sum if global_sum is not None else None)

#             final_threshold = (raw_threshold if global_sum is not None else normalized_threshold)

#             writer.writerow([
#                 family_name,
#                 values["number_of_networks"],
#                 values["number_of_valid_thresholds"],
#                 c_k_values,
#                 c_k_plus_1_values,
#                 common_interval_upper_bound,
#                 common_interval_lower_bound,
#                 common_interval_exists,
#                 family_threshold_mode,
#                 normalized_threshold,
#                 global_sum,
#                 raw_threshold,
#                 final_threshold
#             ])


# def _interval_midpoint(lower_bound: float, upper_bound: float) -> float:
#     """
#     Compute a midpoint between two bounds, using the geometric mean.

#     Parameters:
#         lower_bound : (float)
#             The first bound.
#         upper_bound : (float)
#             The second bound.

#     Returns:
#         midpoint : (float)
#             A threshold between the two bounds.
#     """

#     return float(np.sqrt(lower_bound * upper_bound))


def save_faddis_sensitivity_correlations(
        results_dir: str,
        network_properties_filename: str,
        threshold_source_filename: str,
        output_filename: str,
        threshold_mode: str,
        statistic_metric: str = "Median",
        threshold_column: str = "Normalized Threshold",
        valid_thresholds_only: bool = True,
        number_of_columns_to_skip: int = 3
) -> None:
    """
    Compute correlations between network properties and FADDIS threshold values.
    Two threshold modes are supported:
        - 'network_statistic': computes one threshold per network using a statistic over the normalized contribution sequence, e.g., Median.
        - 'k_boundary': uses the K-boundary threshold already saved by network.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        network_properties_filename : (str)
            The name of the CSV file containing network properties.
        threshold_source_filename : (str)
            The name of the CSV file used to obtain the threshold values.
            For 'network_statistic', this is usually 'normalized_contributions.csv'.
            For 'k_boundary', this is usually 'k_boundary_thresholds_by_network.csv'.
        output_filename : (str)
            The name of the output CSV file to save the sensitivity correlations.
        threshold_mode : (str)
            The threshold source mode. Supported values are 'network_statistic' and 'k_boundary'.
        statistic_metric : (str, optional)
            The statistic used in 'network_statistic' mode.
            Supported values are 'Mean', 'Median', '75%', '90%', and '95%'.
            Default is 'Median'.
        threshold_column : (str, optional)
            The threshold column used in 'k_boundary' mode.
            Default is 'Normalized Threshold'.
        valid_thresholds_only : (bool, optional)
            Whether to use only valid thresholds in 'k_boundary' mode.
            Default is True.
        number_of_columns_to_skip : (int, optional)
            The number of metadata columns to skip before reading contribution values.
            Default is 3, assuming the first columns are 'Network', 'K', and 'Stop Condition'.

    Saves:
        A CSV file with Pearson and Spearman correlations between each network property and the normalized FADDIS threshold.
    """

    if threshold_mode not in {"network_statistic", "k_boundary"}:
        raise ValueError("[ERROR] 'threshold_mode' must be 'network_statistic' or 'k_boundary'.")

    network_properties = _load_network_properties(os.path.join(results_dir, network_properties_filename))

    if threshold_mode == "network_statistic":
        thresholds = _compute_network_statistic_thresholds(
            results_dir=results_dir,
            input_filename=threshold_source_filename,
            statistic_metric=statistic_metric,
            number_of_columns_to_skip=number_of_columns_to_skip
        )
        threshold_label = f"{statistic_metric} Normalized Threshold"

    else:
        thresholds = _load_k_boundary_thresholds_by_network(
            input_path=os.path.join(results_dir, threshold_source_filename),
            threshold_column=threshold_column,
            valid_thresholds_only=valid_thresholds_only
        )
        threshold_label = threshold_column

    merged_rows = []
    for network_name, properties in network_properties.items():
        if network_name not in thresholds:
            continue

        threshold_value = thresholds[network_name]

        if threshold_value is None or threshold_value <= 0:
            continue

        row = dict(properties)
        row["Threshold"] = threshold_value
        merged_rows.append(row)

    groups = [
        ("Non-overlapping and Overlapping", merged_rows),
        (
            "Non-overlapping",
            [row for row in merged_rows if str(row.get("Overlapping Ground-Truth?")).lower() == "false"]
        ),
        (
            "Overlapping",
            [row for row in merged_rows if str(row.get("Overlapping Ground-Truth?")).lower() == "true"]
        )
    ]

    excluded_columns = {"Network", "Ground-Truth?", "Overlapping Ground-Truth?", "Threshold"}

    output_rows = []

    for group_name, group_rows in groups:
        if len(group_rows) < 3:
            continue

        candidate_properties = sorted(set().union(*(row.keys() for row in group_rows)))

        for property_name in candidate_properties:
            if property_name in excluded_columns:
                continue

            x_values = []
            y_values = []

            for row in group_rows:
                x = _parse_optional_float(row.get(property_name))
                y = _parse_optional_float(row.get("Threshold"))

                if x is None or y is None:
                    continue

                x_values.append(x)
                y_values.append(y)

            if len(x_values) < 3:
                continue

            if len(set(x_values)) <= 1:
                continue

            pearson_correlation = _pearson_correlation(x_values, y_values)
            spearman_correlation = _spearman_correlation(x_values, y_values)

            if pearson_correlation is None or spearman_correlation is None:
                continue

            output_rows.append({
                "Group": group_name,
                "Threshold": threshold_label,
                "Property": property_name,
                "#Networks": len(x_values),
                "Spearman Correlation": spearman_correlation,
                "Pearson Correlation": pearson_correlation,
                "Abs Spearman Correlation (Sort Criterion)": abs(spearman_correlation)
            })

    output_rows = sorted(
        output_rows,
        key=lambda row: (row["Group"], -row["Abs Spearman Correlation (Sort Criterion)"])
    )

    with open(os.path.join(results_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=[
            "Group",
            "Threshold",
            "Property",
            "#Networks",
            "Spearman Correlation",
            "Pearson Correlation",
            "Abs Spearman Correlation (Sort Criterion)"
        ])
        writer.writeheader()
        writer.writerows(output_rows)


def _load_network_properties(input_path: str) -> dict[str, dict]:
    """
    Load network properties from a CSV file.

    Parameters:
        input_path : (str)
            The path to the network properties CSV file.

    Returns:
        properties_by_network : (dict[str, dict])
            Dictionary mapping each network name to its properties.
    """

    properties_by_network = {}

    with open(input_path, "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:
            properties_by_network[row["Network"]] = row

    return properties_by_network


def _compute_network_statistic_thresholds(
        results_dir: str,
        input_filename: str,
        statistic_metric: str,
        number_of_columns_to_skip: int = 3
) -> dict[str, float]:
    """
    Compute one statistic-based normalized threshold per network.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the normalized contributions CSV file.
        statistic_metric : (str)
            The statistic used to compute the network-level threshold.
        number_of_columns_to_skip : (int, optional)
            The number of metadata columns to skip before reading contribution values.
            Default is 3.

    Returns:
        thresholds_by_network : (dict[str, float | None])
            Dictionary mapping each network name to its statistic-based threshold.
    """

    thresholds_by_network = {}

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )

    for network_family_dir in network_family_dirs:
        input_path = os.path.join(network_family_dir, input_filename)

        with open(input_path, "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            next(reader, None)

            for row in reader:
                network_name = row[0]
                values = [float(x) for x in row[number_of_columns_to_skip:] if x != ""]

                if len(values) == 0:
                    thresholds_by_network[network_name] = None
                    continue

                thresholds_by_network[network_name] = _compute_statistic(values, statistic_metric)

    return thresholds_by_network


def _load_k_boundary_thresholds_by_network(
        input_path: str,
        threshold_column: str = "Normalized Threshold",
        valid_thresholds_only: bool = True
) -> dict[str, float]:
    """
    Load K-boundary thresholds by network.

    Parameters:
        input_path : (str)
            The path to the K-boundary thresholds by network CSV file.
        threshold_column : (str, optional)
            The threshold column to load.
            Default is 'Normalized Threshold'.
        valid_thresholds_only : (bool, optional)
            Whether to keep only valid thresholds.
            Default is True.

    Returns:
        thresholds_by_network : (dict[str, float | None])
            Dictionary mapping each network name to its K-boundary threshold.
    """

    thresholds_by_network = {}
    with open(input_path, "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            network_name = row["Network"]
            if valid_thresholds_only:
                valid_threshold = str(row.get("Valid Threshold?", "")).lower() == "true"
                if not valid_threshold:
                    thresholds_by_network[network_name] = None
                    continue
            thresholds_by_network[network_name] = _parse_optional_float(row.get(threshold_column))

    return thresholds_by_network


def _compute_statistic(values: list[float], statistic_metric: str) -> float:
    """
    Compute a statistic from a list of values.

    Parameters:
        values : (list[float])
            The list of values.
        statistic_metric : (str)
            The statistic metric to compute.

    Returns:
        statistic : (float)
            The computed statistic.
    """

    if statistic_metric == "Mean":
        return float(np.mean(values))
    if statistic_metric == "Median":
        return float(np.median(values))
    if statistic_metric == "75%":
        return float(np.percentile(values, 75))
    if statistic_metric == "90%":
        return float(np.percentile(values, 90))
    if statistic_metric == "95%":
        return float(np.percentile(values, 95))

    raise ValueError(f"[ERROR] Statistic metric '{statistic_metric}' not supported.")


def _parse_optional_float(value) -> float:
    """
    Parse an optional float value.

    Parameters:
        value : (str | float | int | None)
            The value to parse.

    Returns:
        value : (float | None)
            The parsed float value, or None if the value is empty or invalid.
    """

    if value is None:
        return None

    if isinstance(value, str):
        if value == "" or value == "None" or value.lower() == "nan":
            return None

    try:
        parsed_value = float(value)

        if np.isnan(parsed_value):
            return None

        return parsed_value

    except ValueError:
        return None


def _pearson_correlation(x_values: list[float], y_values: list[float]) -> float:
    """
    Compute Pearson correlation.

    Parameters:
        x_values : (list[float])
            The first variable.
        y_values : (list[float])
            The second variable.

    Returns:
        correlation : (float | None)
            The Pearson correlation, or None if it cannot be computed.
    """

    x = np.asarray(x_values, dtype=np.float64)
    y = np.asarray(y_values, dtype=np.float64)

    if len(x) < 2 or np.std(x) == 0 or np.std(y) == 0:
        return None

    return float(np.corrcoef(x, y)[0, 1])


def _spearman_correlation(x_values: list[float], y_values: list[float]) -> float:
    """
    Compute Spearman correlation.

    Parameters:
        x_values : (list[float])
            The first variable.
        y_values : (list[float])
            The second variable.

    Returns:
        correlation : (float | None)
            The Spearman correlation, or None if it cannot be computed.
    """

    x_ranks = _rank_values(x_values)
    y_ranks = _rank_values(y_values)

    return _pearson_correlation(x_ranks, y_ranks)


def _rank_values(values: list[float]) -> list[float]:
    """
    Compute average ranks for a list of values.

    Parameters:
        values : (list[float])
            The values to rank.

    Returns:
        ranks : (list[float])
            The average ranks.
    """

    sorted_indices = sorted(range(len(values)), key=lambda idx: values[idx])
    ranks = [0.0] * len(values)

    i = 0
    while i < len(values):
        j = i

        while j + 1 < len(values) and values[sorted_indices[j + 1]] == values[sorted_indices[i]]:
            j += 1

        average_rank = (i + j + 2) / 2

        for k in range(i, j + 1):
            ranks[sorted_indices[k]] = average_rank

        i = j + 1

    return ranks
