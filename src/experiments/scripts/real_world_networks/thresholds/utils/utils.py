import csv
import json
import os
from dataclasses import asdict

import networkx as nx
import numpy as np
from networkx import connected_double_edge_swap

from experiments.lapin.lapin import lapin
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.utils.affinity_designs.affinity_design_dataclass import AffinityDesign
from experiments.scripts.utils.adjacency_matrix import compute_adjacency_matrix


def write_candidate_thresholds_to_file(
        candidate_thresholds: list[CandidateThreshold],
        output_file,
        output_fieldnames
):
    """
    Write multiple candidate thresholds to a CSV file.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds to write.
        output_file : (str)
            Path to the output CSV file.
        output_fieldnames : (list[str])
            Field names of the output CSV file.

    Returns:
        None
    """

    with open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(threshold.to_dict() for threshold in candidate_thresholds)


def write_candidate_threshold_to_file(
        candidate_threshold: CandidateThreshold,
        output_file,
        output_fieldnames
):
    """
    Write a candidate threshold to a CSV file.

    Parameters:
        candidate_threshold : (CandidateThreshold)
            Candidate threshold to write.
        output_file : (str)
            Path to the output CSV file.
        output_fieldnames : (list[str])
            Field names of the output CSV file.

    Returns:
        None
    """

    candidate_threshold_dict = candidate_threshold.to_dict()
    output_row = {fieldname: candidate_threshold_dict.get(fieldname) for fieldname in output_fieldnames}

    with open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerow(output_row)


def generate_a_perturbed_graph(
        graph: nx.Graph,
        number_of_swaps: int,
        affinity_design: AffinityDesign,
        apply_lapin: bool,
        seed: int
) -> tuple[nx.Graph, np.ndarray, np.ndarray]:
    """
    Generate a perturbed graph and its adjacency and affinity matrices.

    Parameters:
        graph : (nx.Graph)
            Original graph to perturb.
        number_of_swaps : (int)
            Number of connected double-edge swaps to attempt.
        affinity_design : (AffinityDesign)
            The affinity design to apply.
        apply_lapin : (bool)
            Whether to apply the LAPIN transformation to the perturbed adjacency matrix.
        seed : (int)
            Random seed used by the edge-swapping procedure.

    Returns:
        perturbed_graph : (nx.Graph)
            Perturbed graph.
        perturbed_A : (np.ndarray)
            Adjacency matrix of the perturbed graph.
        perturbed_W : (np.ndarray)
            Affinity matrix of the perturbed graph.
    """

    perturbed_graph = graph.copy()
    successful_swaps = connected_double_edge_swap(perturbed_graph, nswap=number_of_swaps, seed=seed)
    print(f"[DEBUG] Successful swaps = " f"{successful_swaps}/{number_of_swaps}")

    perturbed_A = compute_adjacency_matrix(perturbed_graph)
    perturbed_W = affinity_design.apply_affinity_design(perturbed_A)
    perturbed_W = np.asarray(perturbed_W if not apply_lapin else lapin(perturbed_W), dtype=np.float64)

    return perturbed_graph, perturbed_A, perturbed_W


def save_contributions_experiment_report(
        results_dir: str,
        output_filename: str,
        execution_elapsed_time: float,
        config: RealWorldThresholdEstimationConfig
) -> None:
    """
    Save the threshold estimation experiment report.

    Parameters:
        results_dir : (str)
            Path to the results directory.
        output_filename : (str)
            Name of the output JSON file.
        execution_elapsed_time : (float)
            Total execution time of the experiment in seconds.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    report = asdict(config)
    report["affinity_design"] = config.affinity_design.value
    report["execution_elapsed_time_secs"] = execution_elapsed_time

    output_file = os.path.join(results_dir, output_filename)
    with open(file=output_file, mode="w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)
