import json
import math
import os
from pathlib import Path

from experiments.scripts.lfr_networks.thresholds.lfr_threshold_estimation_config import LFRThresholdEstimationConfig


def get_family_dirs(dir: str) -> list[Path]:
    """
    Get a list of all network families in the directory.

    Parameters:
        dir : (str)
            The path to the directory containing the network families.

    Returns:
        family_dirs : (list[Path])
            The list of network families in the directory.
    """

    return sorted(
        [directory for directory in Path(dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )


def compute_statistics(
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


def save_experiment_report(
        results_dir: str,
        output_filename: str,
        config: LFRThresholdEstimationConfig,
        network_family_dirs: list[Path],
        execution_elapsed_time: float,
) -> None:
    """
    Save a report of the experiment settings to a JSON file.

    Parameters:
        results_dir : (str)
            The path to the results' directory.
        output_filename : (str)
            The name of the output file to save the report.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.
        network_family_dirs : (list[Path])
            A list of Path objects representing the directories of network families included in the experiment.
        execution_elapsed_time : (float)
            The execution elapsed time in seconds.

    Saves:
        A JSON file saved as "{output_filename}" in the specified results directory, containing a report of the
        experiment settings.
    """

    report = {
        "apply_lapin": config.apply_lapin,
        "use_desired_k": config.use_desired_k,
        "number_of_families": len(network_family_dirs),
        "families": [directory.name for directory in network_family_dirs],
        "execution_elapsed_time_secs": execution_elapsed_time
    }

    output_file = os.path.join(results_dir, output_filename)
    with open(file=output_file, mode="w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)


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
