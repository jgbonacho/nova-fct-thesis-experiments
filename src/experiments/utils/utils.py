import csv
import json
import math
import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from sklearn.utils import resample


def create_results_dir(base_dir):
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


def save_normalized_contributions_and_draw_line_plots(
        results_dir,
        input_filename,
        output_filename,
        number_of_columns_to_skip=2
):
    """
    For each network family, save normalized contributions to a new CSV file and draw line plots for each network.

    Parameters:
        results_dir : (str)
            The path to the results directory.
        input_filename : (str)
            The name of the input CSV file containing raw contributions.
        output_filename : (str)
            The name of the output CSV file to save normalized contributions.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.
            Default is 2, assuming the first two columns are "Network" and "K".

    Saves:
        Normalized contributions to 'output_filename' and line plots for each network, within each network family directory.
    """

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
                normalized_values = [round(value / global_sum, 6) for value in values]
                writer.writerow(row[:number_of_columns_to_skip] + normalized_values)

                _draw_normalized_contributions_line_plot(network_family_dir, row[0], row[1], normalized_values)


def _draw_normalized_contributions_line_plot(results_dir, network_name, k, normalized_values):
    """
    Draw a line plot of normalized contributions for a single network, highlighting the contribution at K.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
        network_name : (str)
            The name of the network (used for labeling and saving the plot).
        k : (str)
            The value of k to highlight on the plot.
        normalized_values : (list[float])
            The list of normalized contribution values to plot.
    
    Saves:
        A line plot saved as "{network_name}.pdf" in the specified results directory.
    """

    x_values = list(range(1, len(normalized_values) + 1))
    y_values = normalized_values

    plt.figure(figsize=(8, 5))
    plt.plot(x_values, y_values, marker="o")

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
        results_dir,
        input_filename,
        statistics_output_filename,
        histogram_output_filename,
        number_of_columns_to_skip=2
):
    """
    For each network family, compute statistics of normalized contributions, save them to a CSV file, and draw histograms.

    Parameters:
        results_dir : (str)
            The path to the results directory.
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


def _compute_statistics(normalized_values, number_of_decimal_places=6):
    """
    Compute statistics (mean, std, median, percentiles, min, max) for a list of normalized values.
    
    Parameters:
        normalized_values : (list[float])
            The list of normalized contribution values to compute statistics for.
        number_of_decimal_places : (int, optional)
            The number of decimal places to round the computed statistics to. 
            Default is 6.
    
    Returns:
        statistics : (tuple[float, float, float, float, float, float, float, float])
            A tuple containing the computed statistics: (mean, std, median, p75, p90, p95, min_value, max_value), each rounded to the specified number of decimal places.    
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

    return round(mean, number_of_decimal_places), \
        round(std, number_of_decimal_places), \
        round(median, number_of_decimal_places), \
        round(p75, number_of_decimal_places), \
        round(p90, number_of_decimal_places), \
        round(p95, number_of_decimal_places), \
        round(min_value, number_of_decimal_places), \
        round(max_value, number_of_decimal_places)


def _percentile(sorted_values, p):
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


def _draw_histogram(results_dir, output_filename, normalized_values, mean, std, median, p75, p90, p95):
    """
    Draw a histogram of normalized contributions for a network family, highlighting key statistics.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
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


def draw_boxplot(results_dir, input_filename, output_filename, number_of_columns_to_skip=2):
    """
    Draw a boxplot of normalized contributions for each network family.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
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


def draw_line_plot(results_dir, input_filename, output_filename):
    """
    Draw a line plot of mean normalized contributions with error bars for each network family, along with median and percentiles.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
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

    plt.plot(families, medians, marker="o", label="median")
    plt.plot(families, p75s, marker="o", label="75%")
    plt.plot(families, p90s, marker="o", label="90%")
    plt.plot(families, p95s, marker="o", label="95%")

    plt.xlabel("Network Family")
    plt.ylabel("Normalized Contribution")
    plt.grid(True, alpha=0.3)
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def save_candidate_thresholds(results_dir, input_filename, output_filename, threshold_metrics):
    """
    Save candidate thresholds for each network family to a new CSV file, based on specified threshold metrics.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
        input_filename : (str)
            The name of the input file containing statistics of normalized contributions.
        output_filename : (str)
            The name of the output file to save the candidate thresholds.
        threshold_metrics : (list[str])
            The list of threshold metrics to extract from the input file (e.g., ["Mean", "Median", "75%", "90%", "95%"]).

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
        results_dir,
        raw_contributions_input_filename,
        candidate_thresholds_input_filename,
        bootstrap_statistics_output_filename,
        thresholds_output_filename,
        threshold_metrics,
        maximum_number_of_bootstraps=1000,
        subsample_fraction=0.8,
        number_of_columns_to_skip=2
):
    """
    For each network family, perform bootstrapping to compute new thresholds and their MSE against pre-computed candidate thresholds, then select the best threshold metric based on MSE.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
        raw_contributions_input_filename : (str)
            The name of the input file containing raw contributions for each network.
        candidate_thresholds_input_filename : (str)
            The name of the input file containing pre-computed candidate thresholds for each network family.
        bootstrap_statistics_output_filename : (str)
            The name of the output file to save bootstrap statistics, including MSE for each threshold metric.
        thresholds_output_filename : (str)
            The name of the output file to save the selected threshold metric and value for each network family.
        threshold_metrics : (list[str])
            The list of threshold metrics to evaluate (e.g., ["Mean", "Median", "75%", "90%", "95%"]).
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
        A CSV file with bootstrap statistics and MSE for each threshold metric, and a CSV file with the selected threshold metric and value for each network family, both within the specified results directory.
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
                    round(candidate_threshold, 6),
                    round(mse, 12)
                ])

                if candidate_threshold > 0 and mse < selected_threshold_mse:
                    selected_threshold_mse = mse
                    selected_threshold_metric = threshold_metric
                    selected_threshold_value = candidate_threshold

            thresholds_writer.writerow([
                network_family_dir.name,
                selected_threshold_metric,
                round(selected_threshold_value, 6)
            ])


def _load_candidate_thresholds(results_dir, input_filename, threshold_metrics):
    """
    Load pre-computed candidate thresholds for each network family from a CSV file.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
        input_filename : (str)
            The name of the input file containing candidate thresholds for each network family.
        threshold_metrics : (list[str])
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


def _load_network_contributions(results_dir, input_filename, number_of_columns_to_skip=2):
    """
    Load raw contributions for each network from a CSV file, skipping the specified number of initial columns.

    Parameters:
        results_dir : (str)
            The path to the results directory.
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


def _bootstrapping(number_of_networks, with_replacement, sample_size, random_seed):
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


def _get_contributions(network_contributions, selected_indices):
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


def _normalize_contributions(contributions):
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


def _compute_candidate_thresholds(normalized_values, threshold_metrics):
    """
    Compute candidate thresholds based on specified threshold metrics from a list of normalized contribution values.
    
    Parameters:
        normalized_values : (list[float])
            A list of normalized contribution values to compute candidate thresholds from.
        threshold_metrics : (list[str])
            A list of threshold metrics to compute (e.g., ["Mean", "Median", "75%", "90%", "95%"]).
    
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


def save_experiment_report(results_dir, output_filename, apply_lapin, network_family_dirs, desired_k=None):
    """
    Save a report of the experiment settings to a JSON file.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
        output_filename : (str)
            The name of the output file to save the report.
        apply_lapin : (bool)
            Whether Lapin's transformation was applied in the experiment.
        network_family_dirs : (list[Path])
            A list of Path objects representing the directories of network families included in the experiment.
        desired_k : (int, optional)
            The desired value of k used in the experiment, if applicable. 
            Default is None.
    
    Saves:
        A JSON file saved as "{output_filename}" in the specified results directory, containing a report of the experiment settings.
    """

    report = {
        "apply_lapin": apply_lapin,
        "number_of_families": len(network_family_dirs),
        "families": [directory.name for directory in network_family_dirs]
    }

    if desired_k is not None:
        report["desired_k"] = desired_k

    with open(os.path.join(results_dir, output_filename), "w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)


def read_thresholds(config_dir, input_filename):
    """
    Read thresholds for each network family from a CSV file and return them as a dictionary.

    Parameters:
        config_dir : (str)
            The path to the configuration directory containing the input CSV file.
        input_filename : (str)
            The name of the input CSV file containing thresholds for each network family.
    
    Returns:
        thresholds : (dict[str, float])
            A dictionary mapping each network family to its corresponding threshold value, read from the input CSV file.
    """

    thresholds = {}
    with open(os.path.join(config_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            thresholds[row["Network Family"]] = float(row["Threshold"])
    return thresholds


def draw_line_plots(results_dir, input_filename, metrics_to_plot):
    """
    Draw line plots for specified metrics across different networks, with special handling for the relative error metric. 
    In the case of the relative error metric, add a warning gradient and horizontal lines to indicate important thresholds.
    
    Parameters:
        results_dir : (str)
            The path to the results directory.
        input_filename : (str)
            The name of the input CSV file containing the results.
        metrics_to_plot : (list[str])
            A list of metrics to plot.
    
    Saves:
        Line plots for each specified metric, saved as "{metric}.pdf" in the specified results directory.
    """

    networks = []
    results_by_metric = {metric: [] for metric in metrics_to_plot}

    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            networks.append(row["Network"])
            for metric in metrics_to_plot:
                results_by_metric[metric].append(float(row[metric]))

    for metric in metrics_to_plot:
        fig, ax = plt.subplots(figsize=(14, 5))
        ax.plot(networks, results_by_metric[metric], marker="o", zorder=3)

        if metric == "|K'-K|/K":
            _add_warning_gradient(ax, len(networks), y0=0.2, y1=0.25, y2=0.3, alpha=0.28)

            ax.axhline(0.2, linestyle="--", linewidth=1, label="0.20", zorder=2)
            ax.axhline(0.25, linestyle="--", linewidth=1, label="0.25", zorder=2)
            ax.axhline(0.3, linestyle="--", linewidth=1, label="0.30", zorder=2)
            ax.legend()

        ax.set_xlabel("Network")
        ax.set_ylabel(metric)
        ax.grid(True, alpha=0.3, zorder=1)
        plt.xticks(rotation=45, ha="right")
        fig.tight_layout()

        name = metric if metric != "|K'-K|/K" else "relative_error_of_k"
        output_filename = f"{name}.pdf"
        fig.savefig(os.path.join(results_dir, output_filename), dpi=300)
        plt.close(fig)


def _add_warning_gradient(ax, x_count, y0, y1, y2, alpha):
    """
    Add a warning gradient to the background of a plot, transitioning from yellow to orange to red as values increase from y0 to y2, with specified transparency.

    Parameters:
        ax : (matplotlib.axes.Axes)
            The axes object to which the warning gradient will be added.
        x_count : (int)
            The number of x-axis points in the plot.
        y0 : (float)
            The starting y-value for the gradient.
        y1 : (float)
            The middle y-value for the gradient.
        y2 : (float)
            The ending y-value for the gradient.
        alpha : (float)
            The transparency level of the gradient.
    """

    ymin, ymax = ax.get_ylim()
    ymax = max(ymax, y2)
    ax.set_ylim(ymin, ymax)

    cmap = LinearSegmentedColormap.from_list(
        "warning_gradient",
        [
            (0.0, "yellow"),
            ((y1 - y0) / (y2 - y0), "orange"),
            (1.0, "red"),
        ]
    )

    n = 512
    y = np.linspace(y0, ymax, n)
    t = (y - y0) / (y2 - y0)
    t = np.clip(t, 0, 1).reshape(-1, 1)

    ax.imshow(
        t,
        aspect="auto",
        cmap=cmap,
        origin="lower",
        extent=[-0.5, x_count - 0.5, y0, ymax],
        alpha=alpha,
        zorder=0,
    )
