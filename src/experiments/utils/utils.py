import csv
import json
import math
import os
from collections import defaultdict
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt


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


def save_normalized_contributions(results_dir, input_filename, output_filename, number_of_columns_to_skip=2):
    """
    Normalize contribution values across all network families using a global sum.

    Parameters:
        results_dir : (str)
            Path to the results directory containing one subdirectory per network family.
        input_filename : (str)
            Name of the input CSV file inside each family directory.
        output_filename : (str)
            Name of the output CSV file to save inside each family directory.
        number_of_columns_to_skip : (int, optional)
            Number of leading columns in each row that should not be normalized.
            Default is 2.

    Saves:
        For each network family directory, a CSV file with the same leading columns and normalized contribution values,
        where each value is divided by the global sum of all contribution values across all families.
    """

    global_sum = 0.0

    network_family_dirs = [directory for directory in Path(results_dir).iterdir() if directory.is_dir()]
    for network_family_dir in network_family_dirs:
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                values = [float(x) for x in row[number_of_columns_to_skip:]]
                global_sum += sum(values)

    for network_family_dir in network_family_dirs:
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file, \
                open(os.path.join(network_family_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
            reader = csv.reader(in_file)
            writer = csv.writer(out_file)
            for row in reader:
                values = [float(x) for x in row[number_of_columns_to_skip:]]
                normalized_values = [value / global_sum for value in values]
                rounded_normalized_values = [round(value, 6) for value in normalized_values]
                writer.writerow(row[:number_of_columns_to_skip] + rounded_normalized_values)


def save_global_statistics(results_dir, input_filename, output_filename, number_of_columns_to_skip=2):
    """
    Compute summary statistics of normalized contributions for each network family.

    Parameters:
        results_dir : (str)
            Path to the results directory containing one subdirectory per network family.
        input_filename : (str)
            Name of the normalized contributions CSV file inside each family directory.
        output_filename : (str)
            Name of the CSV file to save global statistics in the results directory.
        number_of_columns_to_skip : (int, optional)
            Number of leading columns in each row that should be ignored when reading values.
            Default is 2.

    Saves:
        A CSV file in 'results_dir' containing one statistics row per network family.
    """

    statistics = []

    network_family_dirs = [directory for directory in Path(results_dir).iterdir() if directory.is_dir()]
    for network_family_dir in network_family_dirs:
        network_family = network_family_dir.name

        values = []
        number_of_networks = 0
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                values.extend(float(x) for x in row[number_of_columns_to_skip:])
                number_of_networks += 1

        sorted_values = sorted(values)
        n = len(sorted_values)

        mean = sum(sorted_values) / n
        variance = sum((x - mean) ** 2 for x in sorted_values) / n
        std = math.sqrt(variance)
        median = (sorted_values[n // 2] if n % 2 == 1 else (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2)
        p75 = _percentile(sorted_values, 0.75)
        p90 = _percentile(sorted_values, 0.90)
        p95 = _percentile(sorted_values, 0.95)
        min_value = sorted_values[0]
        max_value = sorted_values[-1]
        statistics.append((
            network_family,
            number_of_networks - 1,
            round(mean, 6),
            round(std, 6),
            round(median, 6),
            round(p75, 6),
            round(p90, 6),
            round(p95, 6),
            round(min_value, 6),
            round(max_value, 6)
        ))

    with open(os.path.join(results_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Network Family", "#Networks", "Mean", "Std", "Median", "75%", "90%", "95%", "Min", "Max"])
        writer.writerows(statistics)


def draw_line_plot(results_dir, input_filename, output_filename):
    """
    Draw a line plot of contribution percentiles for each network family.

    Parameters:
        results_dir : (str)
            Path to the results' directory.
        input_filename : (str)
            Name of the statistics CSV file in the results' directory.
        output_filename : (str)
            Name of the line plot file to save in the results' directory.

    Saves:
        A line plot in 'results_dir' showing the median, 75th percentile, 90th percentile and 95th percentile
        of normalized contributions for each network family.
    """

    families = []
    medians = []
    p75s = []
    p90s = []
    p95s = []
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            families.append(row["Network Family"])
            medians.append(float(row["Median"]))
            p75s.append(float(row["75%"]))
            p90s.append(float(row["90%"]))
            p95s.append(float(row["95%"]))

    plt.figure(figsize=(10, 4.5))
    plt.plot(families, medians, marker="o", label="Median")
    plt.plot(families, p75s, marker="o", label="75%")
    plt.plot(families, p90s, marker="o", label="90%")
    plt.plot(families, p95s, marker="o", label="95%")

    plt.xlabel("Network Family")
    plt.ylabel("Normalized Contribution")
    plt.xticks(rotation=45, ha="right")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def draw_boxplot(results_dir, input_filename, output_filename, number_of_columns_to_skip=2):
    """
    Draw a boxplot of normalized contributions for each network family.

    Parameters:
        results_dir : (str)
            Path to the results directory containing one subdirectory per network family.
        input_filename : (str)
            Name of the normalized contributions CSV file inside each family directory.
        output_filename : (str)
            Name of the boxplot file to save in the results' directory.
        number_of_columns_to_skip : (int, optional)
            Number of leading columns in each row that should be ignored when reading values.
            Default is 2.

    Saves:
        A boxplot in 'results_dir' where each box represents the distribution of normalized contributions for one network family.
    """

    boxplot_data = []
    boxplot_labels = []

    network_family_dirs = [directory for directory in Path(results_dir).iterdir() if directory.is_dir()]
    for network_family in network_family_dirs:
        values = []
        with (open(os.path.join(results_dir, network_family, input_filename), "r", newline="", encoding="utf-8")
              as input_file):
            reader = csv.reader(input_file)
            for row in reader:
                values.extend(float(x) for x in row[number_of_columns_to_skip:])

        boxplot_data.append(values)
        boxplot_labels.append(network_family.name)

    plt.figure(figsize=(10, 4.5))
    plt.boxplot(boxplot_data, labels=boxplot_labels, patch_artist=True)

    plt.xlabel("Network Family")
    plt.ylabel("Normalized Contribution")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
    plt.close()


def draw_histograms(results_dir, input_filename, statistics_filename, output_filename, number_of_columns_to_skip=2):
    """
    Draw one histogram per network family with percentile threshold lines.

    Parameters:
        results_dir : (str)
            Path to the results directory containing one subdirectory per network family.
        input_filename : (str)
            Name of the normalized contributions CSV file inside each family directory.
        statistics_filename : (str)
            Name of the statistics CSV file in the results' directory.
        output_filename : (str)
            Name of the histogram file to save inside each family directory.
        number_of_columns_to_skip : (int, optional)
            Number of leading columns in each row that should be ignored when reading values.
            Default is 2.

    Saves:
        For each network family directory, a histogram of normalized contributions with vertical lines for the median,
        75th percentile, 90th percentile and 95th percentile taken from the global statistics file.
    """

    statistics_by_family = {}

    network_family_dirs = [directory for directory in Path(results_dir).iterdir() if directory.is_dir()]
    with open(os.path.join(results_dir, statistics_filename), "r", newline="", encoding="utf-8") as stats_in_file:
        reader = csv.DictReader(stats_in_file)
        for row in reader:
            statistics_by_family[row["Network Family"]] = {
                "Median": float(row["Median"]),
                "75%": float(row["75%"]),
                "90%": float(row["90%"]),
                "95%": float(row["95%"]),
            }

    for network_family_dir in network_family_dirs:
        network_family = network_family_dir.name
        values = []
        with open(os.path.join(network_family_dir / input_filename), "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            for row in reader:
                values.extend(float(x) for x in row[number_of_columns_to_skip:])

        thresholds = statistics_by_family.get(network_family)

        plt.figure(figsize=(8, 5))
        plt.hist(values, bins=30, edgecolor="black")
        plt.axvline(
            thresholds["Median"], color="blue", linestyle="--", linewidth=1.5,
            label=f"median = {thresholds['Median']:.4f}"
        )
        plt.axvline(
            thresholds["75%"], color="orange", linestyle="--", linewidth=1.5,
            label=f"75% = {thresholds['75%']:.4f}"
        )
        plt.axvline(
            thresholds["90%"], color="green", linestyle="--", linewidth=1.5,
            label=f"90% = {thresholds['90%']:.4f}"
        )
        plt.axvline(
            thresholds["95%"], color="red", linestyle="--", linewidth=1.5,
            label=f"95% = {thresholds['95%']:.4f}"
        )

        plt.xlabel("Normalized Contribution")
        plt.ylabel("Frequency")
        plt.legend()
        plt.tight_layout()
        plt.savefig(os.path.join(network_family_dir, output_filename), dpi=300)
        plt.close()


def save_thresholds(results_dir, input_filename, output_filename, threshold_metrics):
    """
    Save one threshold value per network family from the statistics file.

    Parameters:
        results_dir : (str)
            Path to the results' directory.
        input_filename : (str)
            Name of the statistics CSV file in the results' directory.
        output_filename : (str)
            Name of the CSV file to save thresholds in the results directory.
        threshold_metrics : (tuple)
            Column names in the statistics file to use as the threshold (for example: "Median", "75%", "90%" or "95%").

    Saves:
        A CSV file in 'results_dir' containing two columns: network family and selected threshold value, for each threshold metric.
    """

    for threshold_metric in threshold_metrics:
        with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file, \
                open(os.path.join(results_dir, output_filename.replace(".csv", f"_{threshold_metric}.csv")), "w",
                     newline="", encoding="utf-8") as out_file:
            reader = csv.DictReader(in_file)
            writer = csv.writer(out_file)
            writer.writerow(["Network Family", f"Threshold ({threshold_metric})"])

            for row in reader:
                writer.writerow([row["Network Family"], row[threshold_metric]])


def _percentile(sorted_values, p):
    """
    Compute a percentile value from a sorted list using linear interpolation.

    Parameters:
        sorted_values : (list[float])
            List of numeric values already sorted in ascending order.
        p : (float)
            Percentile to compute, expressed between 0 and 1.

    Returns:
        percentile_value : (float)
            The interpolated percentile value.
    """

    k = (len(sorted_values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_values[int(k)]

    return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)


def save_experiment_report(
        results_dir,
        apply_lapin,
        threshold_metrics,
        desired_k=None,
        network_family_dirs=None,
        networks_by_family=None
):
    """
    Save a report with experiment metadata and generated files.

    Parameters:
        results_dir : (str)
            Path to the experiment results directory.
        apply_lapin : (bool)
            Whether LAPIN preprocessing was applied.
        threshold_metrics : (list[str])
            Statistics used to generate the threshold files.
        desired_k : (bool)
            Whether FADDIS used the desired number of clusters as stopping criterion.
        network_family_dirs : (list[str])
            List of network family directories.
        networks_by_family : (dict[str, list[str]])
            Mapping from each family to its network names.

    Saves:
        A JSON report file named 'report.json' in the results' directory.
    """

    report = {
        "apply_lapin": apply_lapin,
        "threshold_metrics": threshold_metrics
    }

    if desired_k is not None:
        report["desired_k"] = desired_k
    if network_family_dirs is not None:
        report["number_of_families"] = len(network_family_dirs)
        report["families"] = [directory.name for directory in network_family_dirs]
    if networks_by_family is not None:
        report["total_number_of_networks"] = sum(len(networks) for networks in networks_by_family.values())
        report["networks_by_family"] = networks_by_family

    with open(os.path.join(results_dir, "report.json"), "w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)


def read_thresholds(config_path, thresholds_filename, threshold_metrics):
    """
    Read threshold values for each network family and threshold metric.

    Parameters:
        config_path : (str)
            Path to the configuration directory containing threshold CSV files.
        thresholds_filename : (str)
            Base filename for the thresholds files, for example "thresholds.csv".
        threshold_metrics : (list[str])
            List of threshold metrics to read, for example: ["Median", "75%", "90%", "95%"].

    Returns:
        thresholds : (dict)
            Nested dictionary of threshold values.
    """

    thresholds = {}

    for threshold_metric in threshold_metrics:
        thresholds[threshold_metric] = {}
        with open(os.path.join(config_path, thresholds_filename.replace(".csv", f"_{threshold_metric}.csv")), "r",
                  newline="", encoding="utf-8") as input_file:
            reader = csv.DictReader(input_file)
            for row in reader:
                network_family = row["Network Family"]
                threshold = float(row[f"Threshold ({threshold_metric})"])
                thresholds[threshold_metric][network_family] = threshold

    return thresholds


def draw_threshold_metric_line_plot(results_dir, input_filename, output_filename, y_metric="ONMI"):
    """
    Draw a line plot comparing threshold metrics across networks.

    Parameters:
        results_dir : (str)
            Path to the results' directory.
        input_filename : (str)
            Name of the CSV file with extrinsic evaluation results.
        output_filename : (str)
            Name of the plot file to save in the results' directory.
        y_metric : (str)
            Column name to use on the y-axis, for example "ONMI" or "Omega".

    Saves:
        A line plot in 'results_dir' with:
            - x-axis: network
            - y-axis: selected evaluation metric
            - one line per threshold metric
    """

    data_by_threshold = defaultdict(list)
    network_order = []
    seen_networks = set()

    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:
            network = row["Network"]
            threshold_metric = row["Threshold Metric"]
            y_value = float(row[y_metric])

            data_by_threshold[threshold_metric].append((network, y_value))

            if network not in seen_networks:
                seen_networks.add(network)
                network_order.append(network)

    plt.figure(figsize=(14, 5))

    for threshold_metric, values in data_by_threshold.items():
        values_by_network = {network: y for network, y in values}
        y_series = [values_by_network.get(network, None) for network in network_order]
        plt.plot(network_order, y_series, marker="o", label=threshold_metric)

    plt.xlabel("Network")
    plt.ylabel(y_metric)
    plt.xticks(rotation=45, ha="right")
    plt.legend(title="Threshold Metric")
    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, f"{y_metric if y_metric != "|K'-K|/K" else "relative_error_of_k"}_{output_filename}"), dpi=300)
    plt.close()


def save_threshold_metric_votes(results_dir, input_filename, output_filename, threshold_metrics):
    """
    Compute the number of wins for each threshold metric by reading result files.

    Parameters:
        results_dir : (str)
            Path to the results directory containing one subdirectory per network family.
        input_filename : (str)
            Name of the extrinsic results CSV file inside each family directory.
        output_filename : (str)
            Name of the CSV file to save in the results directory.
        threshold_metrics : (list[str])
            List of threshold metrics to evaluate.

    Saves:
        A CSV file in 'results_dir' with two columns:
            - Threshold Metric
            - Votes
    """

    votes_by_threshold_metric = {threshold_metric: 0 for threshold_metric in threshold_metrics}
    threshold_priority = {threshold_metric: idx for idx, threshold_metric in enumerate(threshold_metrics)}

    network_family_dirs = [directory for directory in Path(results_dir).iterdir() if directory.is_dir()]
    for network_family_dir in network_family_dirs:
        networks_results = {}
        with open(os.path.join(network_family_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
            reader = csv.DictReader(in_file)

            for row in reader:
                network = row["Network"]

                if network not in networks_results:
                    networks_results[network] = []

                networks_results[network].append({
                    "Threshold Metric": row["Threshold Metric"],
                    "ONMI": float(row["ONMI"]),
                    "Omega": float(row["Omega"]),
                    "|K'-K|/K": float(row["|K'-K|/K"]),
                })

        for network, network_results in networks_results.items():
            best_result = min(
                network_results,
                key=lambda result: (
                    -result["ONMI"],
                    -result["Omega"],
                    result["|K'-K|/K"],
                    threshold_priority[result["Threshold Metric"]],
                )
            )
            votes_by_threshold_metric[best_result["Threshold Metric"]] += 1

    with open(os.path.join(results_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(["Threshold Metric", "Votes"])

        for threshold_metric in threshold_metrics:
            writer.writerow([threshold_metric, votes_by_threshold_metric[threshold_metric]])
