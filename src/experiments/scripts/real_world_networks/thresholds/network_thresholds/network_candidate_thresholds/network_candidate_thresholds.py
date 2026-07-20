import csv
import os

import numpy as np

from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold, CandidateThresholdName
from experiments.scripts.real_world_networks.thresholds.utils.utils import write_candidate_thresholds_to_file


def compute_candidate_thresholds(
        results_dir: str,
        network_family: str,
        k_boundary_thresholds_per_family: list[dict],
        input_filename: str,
        input_fieldnames: list[str],
        output_filename: str,
        output_fieldnames: list[str]
) -> list[CandidateThreshold]:
    """
    Compute the candidate thresholds for a network.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        network_family : (str)
            Name of the network family.
        k_boundary_thresholds_per_family : (list[dict])
            K-boundary threshold statistics for each network family.
        input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        input_fieldnames : (list[str])
            Base field names of the raw contributions CSV file.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list[str])
            Field names of the output CSV file.

    Returns:
        candidate_thresholds : (list[CandidateThreshold])
            Family, global, adjacent-boundary, and elbow candidate thresholds for the network.
    """

    # Assuming the network family and at least e_global threshold exist.
    family = next(family for family in k_boundary_thresholds_per_family if family["network_family"] == network_family)
    e_family = family["e_family"]
    e_global = family["e_global"]

    input_file = os.path.join(results_dir, input_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        next(reader, None)

        network = next(reader, None)
        network_name = network[0]
        contributions = [float(x) for x in network[len(input_fieldnames):] if x != ""]

        contribution_boundaries = []
        adjacent_drops = []
        for j in range(len(contributions) - 1):
            c_j = contributions[j]
            c_j_plus_1 = contributions[j + 1]
            if c_j > c_j_plus_1:
                # Valid K-Contribution Threshold.
                contribution_boundaries.append(float(np.sqrt(c_j * c_j_plus_1)))
                adjacent_drops.append(float(np.log(c_j / c_j_plus_1)))

        below_boundaries = [
            boundary for boundary in contribution_boundaries if e_family is not None and boundary < e_family
        ]
        above_boundaries = [
            boundary for boundary in contribution_boundaries if e_family is not None and boundary > e_family
        ]

        candidate_thresholds = [
            # 'e_family'.
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_FAMILY,
                value=e_family
            ),
            # 'e_global'.
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_GLOBAL,
                value=e_global
            ),
            # Closest valid contribution-boundary value below 'e_family'.
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_BELOW,
                value=max(below_boundaries) if below_boundaries else None
            ),
            # Closest valid contribution-boundary value above 'e_family'.
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_ABOVE,
                value=min(above_boundaries) if above_boundaries else None
            ),
            # Valid boundary associated with the strongest adjacent drop.
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_ELBOW,
                value=contribution_boundaries[int(np.argmax(adjacent_drops))] if adjacent_drops else None
            )
        ]

        write_candidate_thresholds_to_file(
            candidate_thresholds=candidate_thresholds,
            output_file=os.path.join(results_dir, output_filename),
            output_fieldnames=output_fieldnames
        )

        return candidate_thresholds
