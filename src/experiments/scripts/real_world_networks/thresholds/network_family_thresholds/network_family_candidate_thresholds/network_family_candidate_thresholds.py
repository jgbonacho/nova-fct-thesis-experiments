import csv
import os
from pathlib import Path

import numpy as np


def compute_thresholds_per_family(
        results_dir: str,
        input_filename: str,
        input_fieldnames: list[str],
        k_boundary_thresholds_by_network_output_filename: str,
        k_boundary_thresholds_by_network_output_fieldnames: list[str],
        k_boundary_thresholds_by_family_output_filename: str,
        k_boundary_thresholds_by_family_output_fieldnames: list[str],
        discard_global_component: bool
) -> list[dict]:
    """
    Compute the K-boundary thresholds for each network and aggregate them by network family.

    Parameters:
        results_dir : (str)
            Path to the results directory containing the network-family subdirectories.
        input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        input_fieldnames : (list[str])
            Base field names of the raw contributions CSV file.
        k_boundary_thresholds_by_network_output_filename : (str)
            Name of the output CSV file containing the K-boundary thresholds by network.
        k_boundary_thresholds_by_network_output_fieldnames : (list[str])
            Field names of the K-boundary thresholds by network CSV file.
        k_boundary_thresholds_by_family_output_filename : (str)
            Name of the output CSV file containing the K-boundary thresholds by network family.
        k_boundary_thresholds_by_family_output_fieldnames : (list[str])
            Field names of the K-boundary thresholds by network family CSV file.
        discard_global_component : (bool)
            Whether the first extracted global/background component is discarded.

    Returns:
        thresholds_per_family : (list[dict])
            K-boundary threshold statistics for each network family.
    """

    # K-boundary thresholds by network.
    families = compute_k_boundary_thresholds_by_network(
        input_filename=input_filename,
        input_fieldnames=input_fieldnames,
        results_dir=results_dir,
        k_boundary_thresholds_by_network_output_filename=k_boundary_thresholds_by_network_output_filename,
        k_boundary_thresholds_by_network_output_fieldnames=k_boundary_thresholds_by_network_output_fieldnames,
        discard_global_component=discard_global_component
    )

    # K-boundary thresholds by network family.
    thresholds_per_family = compute_k_boundary_thresholds_by_family(
        families=families,
        results_dir=results_dir,
        k_boundary_thresholds_by_family_output_filename=k_boundary_thresholds_by_family_output_filename,
        k_boundary_thresholds_by_family_output_fieldnames=k_boundary_thresholds_by_family_output_fieldnames,
    )

    return thresholds_per_family


def compute_k_boundary_thresholds_by_network(
        input_filename: str,
        input_fieldnames: list[str],
        results_dir: str,
        k_boundary_thresholds_by_network_output_filename: str,
        k_boundary_thresholds_by_network_output_fieldnames: list[str],
        discard_global_component: bool
) -> dict:
    """
    Compute the K-boundary threshold for each network.

    Parameters:
        input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        input_fieldnames : (list[str])
            Base field names of the raw contributions CSV file.
        results_dir : (str)
            Path to the results directory containing the network-family subdirectories.
        k_boundary_thresholds_by_network_output_filename : (str)
            Name of the output CSV file.
        k_boundary_thresholds_by_network_output_fieldnames : (list[str])
            Field names of the output CSV file.
        discard_global_component : (bool)
            Whether the first extracted global/background component is discarded when locating
            the contributions at K and K + 1.

    Returns:
        families : (dict)
            Network-family statistics, including the number of networks and valid K-boundary thresholds.
    """

    family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )

    families = {}

    k_boundary_thresholds_by_network_file = os.path.join(results_dir, k_boundary_thresholds_by_network_output_filename)
    with open(file=k_boundary_thresholds_by_network_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(k_boundary_thresholds_by_network_output_fieldnames)

        for network_family_dir in family_dirs:
            families[network_family_dir.name] = {
                "number_of_networks": 0,
                "number_of_valid_thresholds": 0,
                "valid_thresholds": [],
            }

            input_file = os.path.join(network_family_dir, input_filename)
            with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
                reader = csv.reader(in_file)
                next(reader, None)

                for network in reader:
                    families[network_family_dir.name]["number_of_networks"] += 1

                    network_name = network[0]
                    k = int(network[1])
                    contributions = [float(x) for x in network[len(input_fieldnames):] if x != ""]

                    k_index = k if discard_global_component else k - 1
                    k_plus_1_index = k + 1 if discard_global_component else k
                    c_k = contributions[k_index] if 0 <= k_index < len(contributions) else None
                    c_k_plus_1 = contributions[k_plus_1_index] if 0 <= k_plus_1_index < len(contributions) else None

                    if c_k is None or c_k_plus_1 is None or c_k_plus_1 >= c_k:
                        # Invalid K-Boundary Threshold.
                        writer.writerow([network_name, len(contributions), k, c_k, c_k_plus_1, False, None])
                    else:
                        # Valid K-Boundary Threshold.
                        threshold = float(np.sqrt(c_k * c_k_plus_1))
                        writer.writerow([network_name, len(contributions), k, c_k, c_k_plus_1, True, threshold])

                        families[network_family_dir.name]["valid_thresholds"].append(threshold)
                        families[network_family_dir.name]["number_of_valid_thresholds"] += 1

    return families


def compute_k_boundary_thresholds_by_family(
        families: dict,
        results_dir: str,
        k_boundary_thresholds_by_family_output_filename: str,
        k_boundary_thresholds_by_family_output_fieldnames: list[str]
) -> list[dict]:
    """
    Aggregate the valid K-boundary thresholds by network family.

    Parameters:
        families : (dict)
            Network-family statistics and valid K-boundary thresholds by network.
        results_dir : (str)
            Path to the results' directory.
        k_boundary_thresholds_by_family_output_filename : (str)
            Name of the output CSV file.
        k_boundary_thresholds_by_family_output_fieldnames : (list[str])
            Field names of the output CSV file.

    Returns:
        thresholds_per_family : (list[dict])
            Threshold statistics for each network family, including the family and global medians.
    """

    thresholds_per_family = []
    all_valid_thresholds = []
    for family_name, values in families.items():
        number_of_networks = values["number_of_networks"]
        valid_thresholds = values["valid_thresholds"]

        all_valid_thresholds.extend(valid_thresholds)
        e_family = _median_or_none(valid_thresholds)

        thresholds_per_family.append({
            "network_family": family_name,
            "number_of_networks": number_of_networks,
            "number_of_valid_thresholds": len(valid_thresholds),
            "valid_thresholds": valid_thresholds,
            "e_family": e_family
        })

    e_global = _median_or_none(all_valid_thresholds)

    k_boundary_thresholds_by_family_file = os.path.join(results_dir, k_boundary_thresholds_by_family_output_filename)
    with open(file=k_boundary_thresholds_by_family_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.writer(out_file)
        writer.writerow(k_boundary_thresholds_by_family_output_fieldnames)

        for family in thresholds_per_family:
            family["e_global"] = e_global

            writer.writerow([
                family["network_family"],
                family["number_of_networks"],
                family["number_of_valid_thresholds"],
                family["valid_thresholds"],
                family["e_family"],
                family["e_global"]
            ])

    return thresholds_per_family


def _median_or_none(values: list[float]) -> float:
    """
    Compute the median of a list of values.

    Parameters:
        values : (list[float])
            Values whose median is computed.

    Returns:
        median : (float | None)
            Median of the values. None if the list is empty.
    """

    if len(values) == 0:
        return None

    return float(np.median(values))
