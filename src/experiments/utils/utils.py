import csv
import json
import math
import os
from datetime import datetime
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from sklearn.utils import resample


def create_results_dir(base_dir):
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
    sorted_values = sorted(normalized_values)
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

    return round(mean, number_of_decimal_places), \
        round(std, number_of_decimal_places), \
        round(median, number_of_decimal_places), \
        round(p75, number_of_decimal_places), \
        round(p90, number_of_decimal_places), \
        round(p95, number_of_decimal_places), \
        round(min_value, number_of_decimal_places), \
        round(max_value, number_of_decimal_places)


def _percentile(sorted_values, p):
    k = (len(sorted_values) - 1) * p
    f = math.floor(k)
    c = math.ceil(k)

    if f == c:
        return sorted_values[int(k)]

    return sorted_values[f] * (c - k) + sorted_values[c] * (k - f)


def _draw_histogram(results_dir, output_filename, normalized_values, mean, std, median, p75, p90, p95):
    plt.figure(figsize=(8, 5))
    plt.hist(normalized_values, bins=30, edgecolor="black")

    for threshold_value, threshold_label, threshold_color in [
        (mean - std, "mean-std", "purple"),
        (mean, "mean", "gray"),
        (mean + std, "mean+std", "yellow"),
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
    families = []
    mean_minus_stds = []
    means = []
    mean_plus_stds = []
    medians = []
    p75s = []
    p90s = []
    p95s = []
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            families.append(row["Network Family"])
            mean_minus_stds.append(float(row["Mean"]) - float(row["Std"]))
            means.append(float(row["Mean"]))
            mean_plus_stds.append(float(row["Mean"]) + float(row["Std"]))
            medians.append(float(row["Median"]))
            p75s.append(float(row["75%"]))
            p90s.append(float(row["90%"]))
            p95s.append(float(row["95%"]))

    plt.figure(figsize=(10, 4.5))
    plt.plot(families, mean_minus_stds, marker="o", label="mean-std")
    plt.plot(families, means, marker="o", label="mean")
    plt.plot(families, mean_plus_stds, marker="o", label="mean+std")
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
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file, \
            open(os.path.join(results_dir, output_filename), "w", newline="", encoding="utf-8") as out_file:
        reader = csv.DictReader(in_file)
        writer = csv.writer(out_file)

        writer.writerow(["Network Family"] + list(threshold_metrics))
        for row in reader:
            mean = float(row["Mean"])
            std = float(row["Std"])
            threshold_values = []
            for threshold_metric in threshold_metrics:
                if threshold_metric == "Mean-Std":
                    threshold_values.append(round(mean - std, 6))
                elif threshold_metric == "Mean+Std":
                    threshold_values.append(round(mean + std, 6))
                else:
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
                # TODO: Check replacement.
                sampled_indices = _bootstrapping(
                    number_of_networks=number_of_networks,
                    with_replacement=True,
                    sample_size=subsample_size,
                    random_seed=bootstrap_idx
                )
                contributions = _get_contributions(network_raw_contributions, sampled_indices)
                # TODO: Check normalization denominator.
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

                if mse < selected_threshold_mse:
                    selected_threshold_mse = mse
                    selected_threshold_metric = threshold_metric
                    selected_threshold_value = candidate_threshold

            thresholds_writer.writerow([
                network_family_dir.name,
                selected_threshold_metric,
                round(selected_threshold_value, 6)
            ])


def _load_candidate_thresholds(results_dir, input_filename, threshold_metrics):
    candidate_thresholds_by_family = {}
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            candidate_thresholds_by_family[row["Network Family"]] = {
                threshold_metric: float(row[threshold_metric]) for threshold_metric in threshold_metrics
            }
    return candidate_thresholds_by_family


def _load_network_contributions(results_dir, input_filename, number_of_columns_to_skip=2):
    network_raw_contributions = []
    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        next(reader, None)
        for row in reader:
            contributions = [float(x) for x in row[number_of_columns_to_skip:]]
            network_raw_contributions.append(contributions)
    return network_raw_contributions


def _bootstrapping(number_of_networks, with_replacement, sample_size, random_seed):
    return resample(
        list(range(number_of_networks)),
        replace=with_replacement,
        n_samples=sample_size,
        random_state=random_seed
    )


def _get_contributions(network_contributions, selected_indices):
    contributions = []
    for idx in selected_indices:
        contributions.extend(network_contributions[idx])
    return contributions


def _normalize_contributions(contributions):
    total = sum(contributions)
    return [value / total for value in contributions]


def _compute_candidate_thresholds(normalized_values, threshold_metrics):
    mean, std, median, p75, p90, p95, min_value, max_value = _compute_statistics(normalized_values)
    thresholds = {
        "Mean-Std": mean - std,
        "Mean": mean,
        "Mean+Std": mean + std,
        "Median": median,
        "75%": p75,
        "90%": p90,
        "95%": p95
    }

    return {threshold_metric: thresholds[threshold_metric] for threshold_metric in threshold_metrics}


def save_experiment_report(results_dir, output_filename, apply_lapin, network_family_dirs, desired_k=None):
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
    thresholds = {}
    with open(os.path.join(config_dir, input_filename), "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            thresholds[row["Network Family"]] = float(row["Threshold"])
    return thresholds


def draw_line_plots(results_dir, input_filename, metrics_to_plot):
    networks = []
    results_by_metric = {metric: [] for metric in metrics_to_plot}

    with open(os.path.join(results_dir, input_filename), "r", newline="", encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file)
        for row in reader:
            networks.append(row["Network"])
            for metric in metrics_to_plot:
                results_by_metric[metric].append(float(row[metric]))

    for metric in metrics_to_plot:
        plt.figure(figsize=(14, 5))
        plt.plot(networks, results_by_metric[metric], marker="o")
        plt.xlabel("Network")
        plt.ylabel(metric)
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        name = metric if metric != "|K'-K|/K" else "relative_error_of_k"
        output_filename = f"{name}.pdf"
        plt.savefig(os.path.join(results_dir, output_filename), dpi=300)
        plt.close()
