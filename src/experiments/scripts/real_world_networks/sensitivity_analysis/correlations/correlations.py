import csv
import os
from pathlib import Path

import numpy as np


def perform_faddis_sensitivity_analysis(
        results_dir: str,
        network_properties_input_filename: str,
        network_properties_input_fieldnames: list,
        raw_contributions_input_filename: str,
        raw_contributions_input_fieldnames: list,
        output_filename: str,
        output_fieldnames: list,
        apply_lapin: bool
) -> None:
    """
    Perform the FADDIS sensitivity analysis between network properties and valid contributions at K.

    The analysis is performed separately for non-overlapping networks, overlapping networks,
    and both ground-truth types combined.

    Parameters:
        results_dir : (str)
            Path to the results directory.
        network_properties_input_filename : (str)
            Name of the input CSV file containing the network properties.
        network_properties_input_fieldnames : (list)
            Field names of the network properties CSV file.
        raw_contributions_input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        raw_contributions_input_fieldnames : (list)
            Base field names of the raw contributions CSV file.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list)
            Field names of the output CSV file.
        apply_lapin : (bool)
            Whether LAPIN was applied before running FADDIS.

    Returns:
        None
    """

    network_properties = _load_network_properties(os.path.join(results_dir, network_properties_input_filename))
    contributions_at_k = _load_valid_contributions_at_k(
        results_dir, raw_contributions_input_filename, raw_contributions_input_fieldnames, apply_lapin
    )

    ground_truth_groups = [
        ("Non-overlapping and Overlapping", network_properties),
        ("Non-overlapping",
         {
             network_name: properties for network_name, properties in network_properties.items()
             if str(properties.get("Overlapping Ground-Truth?")).lower() == "false"
         }
         ),
        ("Overlapping",
         {
             network_name: properties for network_name, properties in network_properties.items()
             if str(properties.get("Overlapping Ground-Truth?")).lower() == "true"
         }
         )
    ]

    excluded_columns = {"Network", "Ground-Truth?", "Overlapping Ground-Truth?"}
    output_rows = []
    for ground_truth_type, group_network_properties in ground_truth_groups:
        for property_name in network_properties_input_fieldnames:
            if property_name in excluded_columns:
                continue

            x_values = []
            y_values = []
            for network_name, properties in group_network_properties.items():
                if network_name not in contributions_at_k:
                    continue

                property_value = _parse_optional_float(properties.get(property_name))
                contribution_at_k = contributions_at_k[network_name]

                if property_value is None:
                    continue

                x_values.append(property_value)
                y_values.append(contribution_at_k)

            if len(x_values) < 3 or len(set(x_values)) <= 1:
                continue

            pearson_correlation = _pearson_correlation(x_values, y_values)
            spearman_correlation = _spearman_correlation(x_values, y_values)

            if pearson_correlation is None or spearman_correlation is None:
                continue

            output_rows.append({
                "Ground-Truth Type": ground_truth_type,
                "Network Property": property_name,
                "FADDIS Property": "c_K",
                "#Networks": len(x_values),
                "Spearman Correlation": spearman_correlation,
                "Pearson Correlation": pearson_correlation,
                "Abs Spearman Correlation (Sort Criterion)": abs(spearman_correlation)
            })

    ground_truth_type_order = {"Non-overlapping and Overlapping": 0, "Non-overlapping": 1, "Overlapping": 2}
    output_rows.sort(
        key=lambda r: (
            ground_truth_type_order[r["Ground-Truth Type"]],
            r["FADDIS Property"],
            -r["Abs Spearman Correlation (Sort Criterion)"]
        )
    )
    for row in output_rows:
        row.pop("Abs Spearman Correlation (Sort Criterion)")

    file = os.path.join(results_dir, output_filename)
    with open(file=file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


def _load_network_properties(input_path: str) -> dict[str, dict]:
    """
    Load network properties from a CSV file.

    Parameters:
        input_path : (str)
            Path to the input CSV file.

    Returns:
        properties_by_network : (dict[str, dict])
            Network properties indexed by network name.
    """

    properties_by_network = {}
    with open(input_path, "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            properties_by_network[row["Network"]] = row

    return properties_by_network


def _load_valid_contributions_at_k(
        results_dir: str,
        raw_contributions_input_filename: str,
        raw_contributions_input_fieldnames: list,
        apply_lapin: bool
) -> dict[str, float]:
    """
    Load the valid FADDIS contributions corresponding to the ground-truth number of communities.

    Parameters:
        results_dir : (str)
            Path to the results directory containing the network-family subdirectories.
        raw_contributions_input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        raw_contributions_input_fieldnames : (list)
            Base field names of the raw contributions CSV file.
        apply_lapin : (bool)
            Whether LAPIN was applied before running FADDIS.

    Returns:
        contributions_at_k : (dict[str, float])
            Valid contribution at K for each network.
    """

    contributions_at_k = {}

    network_family_dirs = sorted(
        [directory for directory in Path(results_dir).iterdir() if directory.is_dir()],
        key=lambda path: path.name
    )

    for network_family_dir in network_family_dirs:
        input_path = os.path.join(network_family_dir, raw_contributions_input_filename)

        if not os.path.exists(input_path):
            continue

        with open(input_path, "r", newline="", encoding="utf-8") as in_file:
            reader = csv.reader(in_file)
            next(reader, None)

            for row in reader:
                network_name = row[0]
                k = int(row[1])
                contributions = [float(value) for value in row[len(raw_contributions_input_fieldnames):] if value != ""]

                # Without LAPIN, the first extracted component is the background component, so community K is K+1.
                contribution_idx = k - 1 if apply_lapin else k

                if contribution_idx >= len(contributions):
                    continue

                contribution_at_k = contributions[contribution_idx]
                contributions_at_k[network_name] = contribution_at_k

    return contributions_at_k


def _parse_optional_float(value: str) -> float:
    """
    Parse an optional value as a finite floating-point number.

    Parameters:
        value : (str)
            Value to parse.

    Returns:
        parsed_value : (float | None)
            Parsed floating-point value. None if the value is missing, invalid, or non-finite.
    """

    if value is None or value == "":
        return None

    try:
        parsed_value = float(value)
        if not np.isfinite(parsed_value):
            return None
        return parsed_value
    except (TypeError, ValueError):
        return None


def _pearson_correlation(x_values: list[float], y_values: list[float]) -> float:
    """
    Compute the Pearson correlation coefficient between two sequences of values.

    Parameters:
        x_values : (list[float])
            Values of the first variable.
        y_values : (list[float])
            Values of the second variable.

    Returns:
        correlation : (float | None)
            Pearson correlation coefficient. None if either variable has zero variance.
    """

    x = np.asarray(x_values, dtype=np.float64)
    y = np.asarray(y_values, dtype=np.float64)

    if np.std(x) == 0 or np.std(y) == 0:
        return None

    return float(np.corrcoef(x, y)[0, 1])


def _spearman_correlation(x_values: list[float], y_values: list[float]) -> float:
    """
    Compute the Spearman rank correlation coefficient between two sequences of values.

    Parameters:
        x_values : (list[float])
            Values of the first variable.
        y_values : (list[float])
            Values of the second variable.

    Returns:
        correlation : (float | None)
            Spearman rank correlation coefficient. None if either ranked variable has zero variance.
    """

    return _pearson_correlation(_rank_values(x_values), _rank_values(y_values))


def _rank_values(values: list[float]) -> list[float]:
    """
    Assign average ranks to a sequence of values.

    Tied values receive the average of their rank positions.

    Parameters:
        values : (list[float])
            Values to rank.

    Returns:
        ranks : (list[float])
            Rank assigned to each value in its original position.
    """

    sorted_indices = sorted(range(len(values)), key=lambda idx: values[idx])

    ranks = [0.0] * len(values)
    i = 0
    while i < len(values):
        j = i

        while (
                j + 1 < len(values)
                and values[sorted_indices[j + 1]]
                == values[sorted_indices[i]]
        ):
            j += 1

        average_rank = (i + j + 2) / 2

        for rank_idx in range(i, j + 1):
            ranks[sorted_indices[rank_idx]] = average_rank

        i = j + 1

    return ranks
