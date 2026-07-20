import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt

from experiments.scripts.lfr_networks.thresholds.utils.utils import get_family_dirs, compute_statistics


def save_normalized_contributions_and_draw_line_plots(
        results_dir: str,
        input_filename: str,
        output_filename: str,
        output_fieldnames: list[str],
        number_of_columns_to_skip: int
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
        output_fieldnames : (list[str])
            Field names of the output CSV file.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.

    Returns:
        global_sum : (float)
            The global sum of contributions across all networks and families, used for normalization.

    Saves:
        Normalized contributions to 'output_filename' and line plots for each network, within each network family directory.
    """

    # family_dirs = _get_family_dirs(results_dir)
    #
    # for family_dir in family_dirs:
    #    family_sum = 0.0
    #    input_file = os.path.join(family_dir, input_filename)
    #    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
    #        reader = csv.reader(in_file)
    #        next(reader, None)
    #        for row in reader:
    #            values = [float(x) for x in row[number_of_columns_to_skip:]]
    #            family_sum += sum(values)
    #
    #     output_file = os.path.join(family_dir, output_filename)
    #     with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file, \
    #             open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
    #        reader = csv.reader(in_file)
    #        next(reader, None)
    #        writer = csv.writer(out_file)
    #        writer.writerow(output_fieldnames)
    #        for row in reader:
    #            values = [float(x) for x in row[number_of_columns_to_skip:]]
    #            normalized_values = [value / family_sum for value in values]
    #            writer.writerow(row[:number_of_columns_to_skip] + normalized_values)
    #
    #            _draw_normalized_contributions_line_plot(family_dir, row[0], row[1], normalized_values)

    global_sum = 0.0

    family_dirs = get_family_dirs(results_dir)
    for family_dir in family_dirs:
        input_file = os.path.join(family_dir, input_filename)
        with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            next(reader, None)
            for row in reader:
                values = [float(x) for x in row[number_of_columns_to_skip:]]
                global_sum += sum(values)

    for family_dir in family_dirs:
        input_file = os.path.join(family_dir, input_filename)
        output_file = os.path.join(family_dir, output_filename)
        with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file, \
                open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
            reader = csv.reader(in_file)
            next(reader, None)
            writer = csv.writer(out_file)
            writer.writerow(output_fieldnames)
            for row in reader:
                values = [float(x) for x in row[number_of_columns_to_skip:]]
                normalized_values = [value / global_sum for value in values]
                writer.writerow(row[:number_of_columns_to_skip] + normalized_values)

                _draw_normalized_contributions_line_plot(family_dir, row[0], row[1], normalized_values)

    return global_sum


def save_statistics_and_draw_histograms(
        results_dir: str,
        input_filename: str,
        statistics_output_filename: str,
        statistics_output_fieldnames: list[str],
        histogram_output_filename: str,
        number_of_columns_to_skip: int
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
        statistics_output_fieldnames : (list[str])
            Field names of the output statistics CSV file.
        histogram_output_filename : (str)
            The name of the output file to save the histogram plot for each network family.
        number_of_columns_to_skip : (int, optional)
            The number of columns to skip before reading contribution values.

    Saves:
        A CSV file with computed statistics for each network family and histogram plots for each family, within each
        network family directory.
    """

    family_dirs = get_family_dirs(results_dir)

    output_file = os.path.join(results_dir, statistics_output_filename)
    with open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(statistics_output_fieldnames)

        for family_dir in family_dirs:
            normalized_values = []
            number_of_networks = 0
            input_file = os.path.join(family_dir, input_filename)
            with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
                reader = csv.reader(in_file)
                next(reader, None)
                for row in reader:
                    network_normalized_values = [float(x) for x in row[number_of_columns_to_skip:]]
                    normalized_values.extend(network_normalized_values)
                    number_of_networks += 1

            mean, std, median, p75, p90, p95, min_value, max_value = compute_statistics(normalized_values)
            writer.writerow([
                family_dir.name, number_of_networks, mean, std, median, p75, p90, p95, min_value, max_value,
            ])
            _draw_histogram(
                family_dir, histogram_output_filename, normalized_values, mean, std, median, p75, p90, p95
            )


def draw_boxplot(results_dir: str, input_filename: str, output_filename: str, number_of_columns_to_skip: int):
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

    Saves:
        A boxplot saved as "{output_filename}" in the specified results directory, comparing normalized contributions
        across different network families.
    """

    boxplot_data = []
    boxplot_labels = []

    family_dirs = get_family_dirs(results_dir)

    for family_dir in family_dirs:
        normalized_values = []
        input_file = os.path.join(results_dir, family_dir, input_filename)
        with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            next(reader, None)
            for row in reader:
                normalized_values.extend(float(x) for x in row[number_of_columns_to_skip:])
        boxplot_data.append(normalized_values)
        boxplot_labels.append(family_dir.name)

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
    Draw a line plot of mean normalized contributions with error bars for each network family, along with median
    and percentiles.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        input_filename : (str)
            The name of the input file containing statistics of normalized contributions.
        output_filename : (str)
            The name of the output file to save the line plot.

    Saves:
        A line plot saved as "{output_filename}" in the specified results directory, showing mean normalized
        contributions with error bars, and lines for median and percentiles for each network family.
    """

    families = []
    means = []
    stds = []
    medians = []
    p75s = []
    p90s = []
    p95s = []

    input_file = os.path.join(results_dir, input_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
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
        output_fieldnames: list[str]
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
        output_fieldnames : (list[str])
            Field names of the output CSV file.

    Saves:
        A CSV file saved as "{output_filename}" in the specified results directory, containing candidate thresholds
        for each network family based on the specified threshold metrics.
    """
    threshold_metrics = output_fieldnames.copy()
    threshold_metrics.remove("Network Family")

    input_file = os.path.join(results_dir, input_filename)
    output_file = os.path.join(results_dir, output_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file, \
            open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
        reader = csv.DictReader(in_file)
        writer = csv.writer(out_file)

        writer.writerow(output_fieldnames)
        for row in reader:
            threshold_values = []
            for threshold_metric in threshold_metrics:
                threshold_values.append(row[threshold_metric])
            writer.writerow([row["Network Family"]] + threshold_values)


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
        A histogram plot saved as "{output_filename}" in the specified results directory, with shaded areas and lines
        indicating key statistics.
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
