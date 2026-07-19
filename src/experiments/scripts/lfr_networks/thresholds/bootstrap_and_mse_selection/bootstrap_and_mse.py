import csv
import math
import os
from pathlib import Path

import numpy as np
from sklearn.utils import resample

from experiments.scripts.lfr_networks.thresholds.utils.utils import get_family_dirs, compute_statistics


def selected_thresholds_using_bootstrap_and_mse(
        results_dir: str,
        raw_contributions_input_filename: str,
        candidate_thresholds_input_filename: str,
        bootstrap_statistics_output_filename: str,
        bootstrap_statistics_output_fieldnames: list[str],
        thresholds_output_filename: str,
        thresholds_output_fieldnames: list[str],
        maximum_number_of_bootstraps: int,
        subsample_fraction: float,
        threshold_metrics: tuple = ("Mean", "Median", "75%", "90%", "95%")
) -> None:
    """
    For each network family, perform bootstrapping to compute new thresholds and their MSE against pre-computed
    candidate thresholds, then select the best threshold metric based on MSE.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        raw_contributions_input_filename : (str)
            The name of the input file containing raw contributions for each network.
        candidate_thresholds_input_filename : (str)
            The name of the input file containing pre-computed candidate thresholds for each network family.
        bootstrap_statistics_output_filename : (str)
            The name of the output file to save bootstrap statistics, including MSE for each threshold metric.
        bootstrap_statistics_output_fieldnames : (list[str])
            Field names of the bootstrap statistics output CSV file.
        thresholds_output_filename : (str)
            The name of the output file to save the selected threshold metric and value for each network family.
        thresholds_output_fieldnames : (list[str])
            Field names of the thresholds output CSV file.
        maximum_number_of_bootstraps : (int, optional)
            The maximum number of bootstrap iterations to perform.
        subsample_fraction : (float, optional)
            The fraction of networks to include in each bootstrap sample.
        threshold_metrics : (tuple)
            The list of threshold metrics to evaluate.
             Default is ("Mean", "Median", "75%", "90%", "95%").

    Saves:
        A CSV file with bootstrap statistics and MSE for each threshold metric, and a CSV file with the selected
        threshold metric and value for each network family, both within the specified results' directory.
    """

    candidate_thresholds_by_family = _load_candidate_thresholds(
        results_dir, candidate_thresholds_input_filename, threshold_metrics
    )

    bootstrap_statistics_output_file = os.path.join(results_dir, bootstrap_statistics_output_filename)
    thresholds_output_file = os.path.join(results_dir, thresholds_output_filename)
    with open(file=bootstrap_statistics_output_file, mode="w", newline="", encoding="utf-8") as bootstrap_out_file, \
            open(file=thresholds_output_file, mode="w", newline="", encoding="utf-8") as thresholds_out_file:
        bootstrap_writer = csv.writer(bootstrap_out_file)
        bootstrap_writer.writerow(bootstrap_statistics_output_fieldnames)
        thresholds_writer = csv.writer(thresholds_out_file)
        thresholds_writer.writerow(thresholds_output_fieldnames)

        family_dirs = get_family_dirs(results_dir)

        for family_dir in family_dirs:
            network_raw_contributions = _load_network_contributions(family_dir, raw_contributions_input_filename)
            number_of_networks = len(network_raw_contributions)
            subsample_size = math.ceil(subsample_fraction * number_of_networks)
            number_of_bootstraps = 0
            squared_errors_by_metric = {threshold_metric: [] for threshold_metric in threshold_metrics}
            candidate_thresholds = candidate_thresholds_by_family[family_dir.name]

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

                bootstrap_writer.writerow(
                    [family_dir.name, number_of_networks, subsample_size, number_of_bootstraps, threshold_metric,
                     candidate_threshold, mse]
                )

                if candidate_threshold > 0 and mse < selected_threshold_mse:
                    selected_threshold_mse = mse
                    selected_threshold_metric = threshold_metric
                    selected_threshold_value = candidate_threshold

            thresholds_writer.writerow(
                [family_dir.name, selected_threshold_metric, selected_threshold_value]
            )


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
    input_file = os.path.join(results_dir, input_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
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
    input_file = os.path.join(results_dir, input_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
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
            A dictionary mapping each specified threshold metric to its computed value based on the normalized
            contribution values.
    """

    mean, _, median, p75, p90, p95, _, _ = compute_statistics(normalized_values)
    thresholds = {
        "Mean": mean,
        "Median": median,
        "75%": p75,
        "90%": p90,
        "95%": p95
    }

    return {threshold_metric: thresholds[threshold_metric] for threshold_metric in threshold_metrics}
