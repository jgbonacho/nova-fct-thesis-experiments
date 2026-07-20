import csv
import json
import os
from pathlib import Path

from experiments.scripts.real_world_networks.utils.network_config_dataclass import NetworkConfig


def load_real_world_network_configs(network_directory: Path, input_filename: str) -> list[NetworkConfig]:
    """
    Load the real-world network configurations from a JSON file.

    Parameters:
        network_directory : (Path)
            Directory containing the network configuration file.
        input_filename : (str)
            Name of the configuration file without the JSON extension.

    Returns:
        network_configs : (list[NetworkConfig])
            Network configurations loaded from the JSON file.
    """

    input_file = os.path.join(network_directory, f"{input_filename}.json")
    with open(file=input_file, mode="r", encoding="utf-8") as in_file:
        json_networks = json.load(in_file)

    return [NetworkConfig.from_dict(json_network) for json_network in json_networks]


def append_properties(
        results_dir: str,
        output_filename: str,
        output_fieldnames: list[str],
        properties
) -> None:
    """
    Append a set of properties to a CSV file.

    Parameters:
        results_dir : (str)
            Path to the results directory.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list[str])
            Field names of the output CSV file.
        properties : (CsvDataclass)
            Dataclass containing the properties to append.

    Returns:
        None
    """

    os.makedirs(results_dir, exist_ok=True)

    output_file = os.path.join(results_dir, output_filename)
    write_header = not os.path.exists(output_file) or os.path.getsize(output_file) == 0

    with open(file=output_file, mode="a", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(properties.to_dict())


def save_sensitivity_experiment_report(
        results_dir: str,
        output_filename: str,
        execution_elapsed_time: float,
        apply_lapin: bool
) -> None:
    """
    Save the sensitivity analysis experiment report.

    Parameters:
        results_dir : (str)
            Path to the results directory.
        output_filename : (str)
            Name of the output JSON file.
        execution_elapsed_time : (float)
            Total execution time of the experiment in seconds.
        apply_lapin : (bool)
            Whether LAPIN was applied before running FADDIS.

    Returns:
        None
    """

    report = {
        "apply_lapin": apply_lapin,
        "execution_elapsed_time_secs": execution_elapsed_time
    }

    file = os.path.join(results_dir, output_filename)
    with open(file=file, mode="w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)
