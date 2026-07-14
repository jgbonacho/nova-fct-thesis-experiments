import csv
import json
import os
from dataclasses import asdict
from pathlib import Path

import networkx as nx
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from networkx import connected_double_edge_swap
from numpy.linalg import norm
from sklearn.metrics import normalized_mutual_info_score

from experiments.defuzzification.defuzzification import apply_defuzzification_rule
from experiments.evaluation.community_properties.community_properties import compute_community_properties
from experiments.evaluation.computational_metrics.computational_metrics import get_computation_start_time, \
    get_computation_end_time, compute_computational_metrics
from experiments.evaluation.extrinsic_metrics.extrinsic_metrics import compute_extrinsic_metrics
from experiments.evaluation.intrinsic_metrics.intrinsic_metrics import compute_intrinsic_metrics
from experiments.faddis.faddis import faddis
from experiments.lapin.lapin import lapin
from experiments.loaders.adjacency_matrix import compute_adjacency_matrix
from experiments.utils.dataclasses.candidate_threshold_dataclass import CandidateThreshold, IntrinsicEvaluation, \
    StabilityEvaluation, CandidateThresholdName, NullModelEvaluation, ParetoPlusParsimonySelection, ExtrinsicEvaluation
from experiments.utils.dataclasses.ground_truth_properties_dataclass import GroundTruthProperties
from experiments.utils.dataclasses.network_config_dataclass import NetworkConfig
from experiments.utils.dataclasses.network_properties_dataclass import NetworkProperties
from experiments.utils.dataclasses.real_world_threshold_estimation_config import RealWorldThresholdEstimationConfig

THRESHOLD_PLOT_STYLES = {
    "e_family": {"label": r"$\epsilon_{\mathrm{family}}$", "color": "tab:red", "marker": "o"},
    "e_global": {"label": r"$\epsilon_{\mathrm{global}}$", "color": "tab:grey", "marker": "s"},
    "e_below": {"label": r"$\epsilon_{\mathrm{below}}$", "color": "tab:brown", "marker": "^"},
    "e_above": {"label": r"$\epsilon_{\mathrm{above}}$", "color": "tab:green", "marker": "D"},
    "e_elbow": {"label": r"$\epsilon_{\mathrm{elbow}}$", "color": "tab:purple", "marker": "*"}
}


def load_real_world_network_configs(network_directory: Path, input_filename: str) -> list[NetworkConfig]:
    file = os.path.join(network_directory, f"{input_filename}.json")
    with open(file=file, mode="r", encoding="utf-8") as in_file:
        json_networks = json.load(in_file)

    return [NetworkConfig.from_dict(json_network) for json_network in json_networks]


def compute_network_properties(
        network_name: str,
        graph: nx.Graph,
        ground_truth: bool,
        overlapping_ground_truth: bool
) -> NetworkProperties:
    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()

    degrees = np.asarray([degree for _, degree in graph.degree()], dtype=np.float64)
    min_degree = float(np.min(degrees)) if nodes > 0 else None
    max_degree = float(np.max(degrees)) if nodes > 0 else None
    average_degree = float(np.mean(degrees)) if nodes > 0 else None
    degree_std = float(np.std(degrees, ddof=1)) if nodes > 1 else 0.0
    degree_cv = (
        degree_std / average_degree
        if average_degree is not None and average_degree > 0
        else None
    )
    degree_hub_ratio = (
        max_degree / average_degree
        if max_degree is not None and average_degree is not None and average_degree > 0
        else None
    )
    degree_assortativity = float(nx.degree_assortativity_coefficient(graph)) if nodes > 0 else None

    density = nx.density(graph) if nodes > 1 else 0.0
    sparsity = 1.0 - density
    global_clustering_coefficient = nx.transitivity(graph) if nodes > 0 else None
    average_clustering = nx.average_clustering(graph) if nodes > 0 else None

    return NetworkProperties(
        network=network_name,
        nodes_lcc=nodes,
        edges_lcc=edges,
        min_degree=min_degree,
        max_degree=max_degree,
        average_degree=average_degree,
        degree_std=degree_std,
        degree_cv=degree_cv,
        degree_hub_ratio=degree_hub_ratio,
        degree_assortativity=degree_assortativity,
        density=density,
        sparsity=sparsity,
        global_clustering_coefficient=global_clustering_coefficient,
        average_clustering=average_clustering,
        ground_truth=ground_truth,
        overlapping_ground_truth=overlapping_ground_truth
    )


def compute_ground_truth_properties(
        network_name: str,
        ground_truth_labels: list,
        k: int,
        overlapping_ground_truth: bool,
        number_of_nodes: int
) -> GroundTruthProperties:
    if ground_truth_labels is None:
        return None

    community_sizes = {}
    nodes_without_community = 0
    overlapping_nodes = 0
    labeled_nodes = 0

    if not overlapping_ground_truth:
        for label in ground_truth_labels:
            if label == -1:
                nodes_without_community += 1
                continue

            labeled_nodes += 1
            community_sizes[label] = community_sizes.get(label, 0) + 1

        overlap_fraction = 0.0
    else:
        for labels in ground_truth_labels:
            if labels == [-1] or len(labels) == 0:
                nodes_without_community += 1
                continue

            valid_labels = [label for label in labels if label != -1]

            if len(valid_labels) == 0:
                nodes_without_community += 1
                continue

            labeled_nodes += 1

            if len(valid_labels) > 1:
                overlapping_nodes += 1

            for label in valid_labels:
                community_sizes[label] = community_sizes.get(label, 0) + 1

        overlap_fraction = overlapping_nodes / labeled_nodes if labeled_nodes > 0 else None

    sizes = np.asarray(list(community_sizes.values()), dtype=np.float64)

    if len(sizes) == 0:
        min_community_size = None
        max_community_size = None
        average_community_size = None
        community_size_std = None
        community_size_cv = None
    else:
        min_community_size = float(np.min(sizes))
        max_community_size = float(np.max(sizes))
        average_community_size = float(np.mean(sizes))
        community_size_std = float(np.std(sizes, ddof=1)) if len(sizes) > 1 else 0.0
        community_size_cv = (
            community_size_std / average_community_size
            if average_community_size > 0
            else None
        )

    nodes_fraction_without_community = nodes_without_community / number_of_nodes

    return GroundTruthProperties(
        network=network_name,
        overlapping_ground_truth=overlapping_ground_truth,
        overlap_fraction=overlap_fraction,
        k=k,
        community_proportion=k / number_of_nodes,
        min_community_size=min_community_size,
        max_community_size=max_community_size,
        average_community_size=average_community_size,
        community_size_std=community_size_std,
        community_size_cv=community_size_cv,
        nodes_without_community=nodes_without_community,
        nodes_fraction_without_community=nodes_fraction_without_community
    )


def append_properties(
        results_dir: str,
        output_filename: str,
        output_fieldnames: list[str],
        properties
) -> None:
    os.makedirs(results_dir, exist_ok=True)

    file = os.path.join(results_dir, output_filename)
    write_header = not os.path.exists(file) or os.path.getsize(file) == 0

    with open(file=file, mode="a", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(properties.to_dict())


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
    properties_by_network = {}
    with open(input_path, "r", newline="", encoding="utf-8") as in_file:
        reader = csv.DictReader(in_file)
        for row in reader:
            properties_by_network[row["Network"]] = row

    return properties_by_network


def save_sensitivity_experiment_report(
        results_dir: str,
        output_filename: str,
        execution_elapsed_time: float,
        apply_lapin: bool
) -> None:
    report = {
        "apply_lapin": apply_lapin,
        "execution_elapsed_time_secs": execution_elapsed_time
    }

    file = os.path.join(results_dir, output_filename)
    with open(file=file, mode="w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)


def _load_valid_contributions_at_k(
        results_dir: str,
        raw_contributions_input_filename: str,
        raw_contributions_input_fieldnames: list,
        apply_lapin: bool
) -> dict[str, float]:
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


def _parse_optional_float(value: any) -> float:
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
    x = np.asarray(x_values, dtype=np.float64)
    y = np.asarray(y_values, dtype=np.float64)

    if np.std(x) == 0 or np.std(y) == 0:
        return None

    return float(np.corrcoef(x, y)[0, 1])


def _spearman_correlation(x_values: list[float], y_values: list[float]) -> float:
    return _pearson_correlation(_rank_values(x_values), _rank_values(y_values))


def _rank_values(values: list[float]) -> list[float]:
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


# ----------------------------------------------------------------------------------------------------------------------


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
    # K-boundary thresholds by network
    families = compute_k_boundary_thresholds_by_network(
        input_filename=input_filename,
        input_fieldnames=input_fieldnames,
        results_dir=results_dir,
        k_boundary_thresholds_by_network_output_filename=k_boundary_thresholds_by_network_output_filename,
        k_boundary_thresholds_by_network_output_fieldnames=k_boundary_thresholds_by_network_output_fieldnames,
        discard_global_component=discard_global_component
    )

    # K-boundary thresholds by network family
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
                        # Invalid K-Boundary Threshold
                        writer.writerow([network_name, len(contributions), k, c_k, c_k_plus_1, False, None])
                    else:
                        # Valid K-Boundary Threshold
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


# ----------------------------------------------------------------------------------------------------------------------


def compute_candidate_thresholds(
        results_dir: str,
        network_family: str,
        k_boundary_thresholds_per_family: list[dict],
        input_filename: str,
        input_fieldnames: list[str],
        output_filename: str,
        output_fieldnames: list[str]
) -> list[CandidateThreshold]:
    # Assuming the network family and its thresholds always exist.
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
                # Valid K-Contribution Threshold
                contribution_boundaries.append(float(np.sqrt(c_j * c_j_plus_1)))
                adjacent_drops.append(float(np.log(c_j / c_j_plus_1)))

        below_boundaries = [boundary for boundary in contribution_boundaries if boundary < e_family]
        above_boundaries = [boundary for boundary in contribution_boundaries if boundary > e_family]

        candidate_thresholds = [
            # 'e_family'
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_FAMILY,
                value=e_family
            ),
            # 'e_global'
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_GLOBAL,
                value=e_global
            ),
            # Closest valid contribution-boundary value below 'e_family'
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_BELOW,
                value=max(below_boundaries) if below_boundaries else None
            ),
            # Closest valid contribution-boundary value above 'e_family'
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_ABOVE,
                value=min(above_boundaries) if above_boundaries else None
            ),
            # Valid boundary associated with the strongest adjacent drop
            CandidateThreshold(
                family=network_family, network=network_name, name=CandidateThresholdName.E_ELBOW,
                value=contribution_boundaries[int(np.argmax(adjacent_drops))] if adjacent_drops else None
            )
        ]

        _write_candidate_thresholds_to_file(
            candidate_thresholds=candidate_thresholds,
            output_file=os.path.join(results_dir, output_filename),
            output_fieldnames=output_fieldnames
        )

        return candidate_thresholds


def evaluate_candidate_thresholds_using_intrinsic_metrics(
        results_dir: str,
        graph_and_matrices: tuple,
        candidate_thresholds: list[CandidateThreshold],
        output_filename: str,
        output_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> list[CandidateThreshold]:
    graph, A, W = graph_and_matrices
    tau, k_max = config.tau, config.compute_k_max(graph.number_of_nodes())

    updated_candidate_thresholds = []
    for candidate_threshold in candidate_thresholds:
        # Check candidate exists
        if candidate_threshold.value is None: continue

        start_time = get_computation_start_time()
        U, _, _, _, _, _ = faddis(W=W, epsilon=candidate_threshold.value, tau=tau, k_max=k_max)
        end_time = get_computation_end_time()

        # Check if clusters were extracted
        if U.shape[1] == 0: continue

        predicted_labels, k_predicted, first_cluster_discarded = apply_defuzzification_rule(
            U=U,
            gamma=config.defuzzification_gamma,
            overlapping=config.overlapping_communities
        )

        intrinsic_results = compute_intrinsic_metrics(
            graph=graph,
            A=A,
            U=U if not first_cluster_discarded else np.asarray(U)[:, 1:],
            predicted_labels=predicted_labels,
            overlapping=config.overlapping_communities
        )
        community_properties = compute_community_properties(
            number_of_nodes=graph.number_of_nodes(),
            predicted_labels=predicted_labels,
            overlapping_communities=config.overlapping_communities,
            near_singleton_boundary=config.near_singleton_boundary
        )
        computational_results = compute_computational_metrics(start_time, end_time)

        candidate_threshold.intrinsic_evaluation = IntrinsicEvaluation(
            k_predicted=community_properties.number_of_communities,
            overlapping_communities=config.overlapping_communities,
            community_size_distribution=community_properties.community_size_distribution,
            singleton_or_near_singleton_communities=community_properties.singleton_or_near_singleton_count,
            singleton_or_near_singleton_fraction=community_properties.singleton_or_near_singleton_fraction,
            largest_community_fraction=community_properties.largest_community_fraction,
            modularity=intrinsic_results.modularity if not config.overlapping_communities else intrinsic_results.fuzzy_modularity,
            conductance=intrinsic_results.conductance if not config.overlapping_communities else intrinsic_results.conductance_bn,
            runtime=computational_results.runtime
        )

        updated_candidate_thresholds.append(candidate_threshold)

    _evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds=updated_candidate_thresholds,
        config=config,
        check_modularity=True,
        check_conductance=True,
        check_non_degenerate=True
    )

    _write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_fieldnames
    )

    filtered_candidate_thresholds = _filter_candidate_thresholds_using_pareto_and_parsimony(
        candidate_thresholds=updated_candidate_thresholds,
        number_of_thresholds_to_retain=config.number_of_thresholds_to_retain_after_intrinsic_evaluation,
        check_modularity=True,
        check_conductance=True,
        check_non_degenerate=True
    )

    return filtered_candidate_thresholds


def evaluate_candidate_thresholds_under_perturbation_stability(
        results_dir: str,
        graph_and_matrices: tuple,
        candidate_thresholds: list[CandidateThreshold],
        output_filename: str,
        output_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> list[CandidateThreshold]:
    graph, A, W = graph_and_matrices
    tau, k_max = config.tau, config.compute_k_max(graph.number_of_nodes())

    updated_candidate_thresholds = []
    for candidate_threshold in candidate_thresholds:

        U, _, _, _, _, _ = faddis(W=W, epsilon=candidate_threshold.value, tau=tau, k_max=k_max)
        predicted_labels, k_predicted, first_cluster_discarded = apply_defuzzification_rule(
            U=U,
            gamma=config.defuzzification_gamma,
            overlapping=config.overlapping_communities
        )

        sims = []
        for perturbation_number in range(1, config.number_of_perturbed_graphs + 1):
            perturbed_graph, perturbed_A, perturbed_W = _generate_a_perturbed_graph(
                graph=graph,
                number_of_swaps=config.compute_number_of_edges_swaps_in_perturbed_graphs(graph.number_of_edges()),
                apply_lapin=config.apply_lapin,
                seed=perturbation_number
            )

            perturbed_U, _, _, _, _, _ = faddis(W=perturbed_W, epsilon=candidate_threshold.value, tau=tau, k_max=k_max)

            # Check if clusters were extracted
            if perturbed_U.shape[1] == 0: continue

            perturbed_predicted_labels, perturbed_k_predicted, perturbed_first_cluster_discarded = apply_defuzzification_rule(
                U=perturbed_U,
                gamma=config.defuzzification_gamma,
                overlapping=config.overlapping_communities
            )

            if not config.overlapping_communities:
                sim = float(normalized_mutual_info_score(predicted_labels, perturbed_predicted_labels))
            else:
                sim = _compute_fuzzy_co_membership_similarity(
                    U, first_cluster_discarded, perturbed_U, perturbed_first_cluster_discarded
                )

            if sim is None:
                continue

            sims.append(sim)

        stability = float(sum(sims) / len(sims)) if len(sims) > 0 else 0

        candidate_threshold.stability_evaluation = StabilityEvaluation(
            number_of_perturbed_graphs=config.number_of_perturbed_graphs,
            number_of_valid_similarities=len(sims),
            similarities=sims,
            stability=stability
        )

        updated_candidate_thresholds.append(candidate_threshold)

    _evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds=updated_candidate_thresholds,
        config=config,
        # check_modularity=True,
        # check_conductance=True,
        # check_non_degenerate=True,
        check_stability=True
    )

    _write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_fieldnames
    )

    filtered_candidate_thresholds = _filter_candidate_thresholds_using_pareto_and_parsimony(
        candidate_thresholds=updated_candidate_thresholds,
        number_of_thresholds_to_retain=config.number_of_thresholds_to_retain_after_stability_evaluation,
        check_modularity=True,
        check_conductance=True,
        check_non_degenerate=True,
        check_stability=True
    )

    return filtered_candidate_thresholds


def evaluate_candidate_thresholds_under_null_model(
        results_dir: str,
        graph_and_matrices: tuple,
        candidate_thresholds: list[CandidateThreshold],
        output_filename: str,
        output_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> list[CandidateThreshold]:
    graph, A, W = graph_and_matrices
    tau, k_max = config.tau, config.compute_k_max(graph.number_of_nodes())

    updated_candidate_thresholds = []
    for candidate_threshold in candidate_thresholds:
        null_modularities = []
        null_conductances = []
        for null_number in range(1, config.number_of_null_models + 1):
            null_graph, null_A, null_W = _generate_a_perturbed_graph(
                graph=graph,
                number_of_swaps=config.compute_number_of_edges_swaps_in_null_models(graph.number_of_edges()),
                apply_lapin=config.apply_lapin,
                seed=null_number
            )

            null_U, _, _, _, _, _ = faddis(W=null_W, epsilon=candidate_threshold.value, tau=tau, k_max=k_max)

            # Check if clusters were extracted
            if null_U.shape[1] == 0: continue

            null_predicted_labels, null_k_predicted, null_first_cluster_discarded = apply_defuzzification_rule(
                U=null_U,
                gamma=config.defuzzification_gamma,
                overlapping=config.overlapping_communities
            )

            null_intrinsic_results = compute_intrinsic_metrics(
                graph=null_graph,
                A=null_A,
                U=null_U if not null_first_cluster_discarded else np.asarray(null_U)[:, 1:],
                predicted_labels=null_predicted_labels,
                overlapping=config.overlapping_communities
            )

            null_modularities.append(
                float(
                    null_intrinsic_results.modularity
                    if not config.overlapping_communities
                    else null_intrinsic_results.fuzzy_modularity
                )
            )
            null_conductances.append(
                float(
                    null_intrinsic_results.conductance
                    if not config.overlapping_communities else
                    null_intrinsic_results.conductance_bn
                )
            )

        if null_modularities:
            real_modularity = candidate_threshold.intrinsic_evaluation.modularity

            mean_null_modularity = float(np.mean(null_modularities))
            std_null_modularity = float(np.std(null_modularities, ddof=1)) if len(null_modularities) > 1 else 0.0

            modularity_z_score = (
                (real_modularity - mean_null_modularity) / std_null_modularity
                if std_null_modularity > 0 else None
            )
            modularity_empirical_p_value = (
                    (1 + sum(q_null >= real_modularity for q_null in null_modularities)) /
                    (len(null_modularities) + 1)
            )
            modularity_rank = 1 + sum(q_null > real_modularity for q_null in null_modularities)
        else:
            mean_null_modularity = None
            std_null_modularity = None
            modularity_z_score = None
            modularity_empirical_p_value = None
            modularity_rank = None

        if null_conductances:
            real_conductance = candidate_threshold.intrinsic_evaluation.conductance

            mean_null_conductance = float(np.mean(null_conductances))
            std_null_conductance = float(np.std(null_conductances, ddof=1)) if len(null_conductances) > 1 else 0.0

            conductance_z_score = (
                (mean_null_conductance - real_conductance) / std_null_conductance
                if std_null_conductance > 0 else None
            )
            conductance_empirical_p_value = (
                    (1 + sum(phi_null <= real_conductance for phi_null in null_conductances)) /
                    (len(null_conductances) + 1))
            conductance_rank = 1 + sum(phi_null < real_conductance for phi_null in null_conductances)
        else:
            mean_null_conductance = None
            std_null_conductance = None
            conductance_z_score = None
            conductance_empirical_p_value = None
            conductance_rank = None

        candidate_threshold.null_model_evaluation = NullModelEvaluation(
            number_of_null_graphs=config.number_of_null_models,
            number_of_valid_results=min(len(null_modularities), len(null_conductances)),
            null_modularities=null_modularities,
            mean_null_modularity=mean_null_modularity,
            std_null_modularity=std_null_modularity,
            modularity_z_score=modularity_z_score,
            modularity_empirical_p_value=modularity_empirical_p_value,
            modularity_rank=modularity_rank,
            null_conductances=null_conductances,
            mean_null_conductance=mean_null_conductance,
            std_null_conductance=std_null_conductance,
            conductance_z_score=conductance_z_score,
            conductance_empirical_p_value=conductance_empirical_p_value,
            conductance_rank=conductance_rank
        )

        updated_candidate_thresholds.append(candidate_threshold)

    _evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds=updated_candidate_thresholds,
        config=config,
        # check_modularity=True,
        # check_conductance=True,
        # check_non_degenerate=True,
        # check_stability=True,
        check_null_model=True
    )

    _write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_fieldnames
    )

    return updated_candidate_thresholds


def select_final_threshold_by_pareto_and_parsimony(
        results_dir: str,
        candidate_thresholds: list[CandidateThreshold],
        final_thresholds_output_filename: str,
        final_thresholds_output_fieldnames: list,
        threshold_output_filename: str
) -> CandidateThreshold:
    updated_candidate_thresholds = []
    for candidate_threshold in candidate_thresholds:
        acceptable = (
                candidate_threshold.intrinsic_evaluation.acceptable_modularity
                and candidate_threshold.intrinsic_evaluation.acceptable_conductance
                and candidate_threshold.intrinsic_evaluation.acceptable_non_degenerate
                and candidate_threshold.stability_evaluation.acceptable_stability
                and candidate_threshold.null_model_evaluation.acceptable_null_model
        )

        candidate_threshold.pareto_plus_parsimony_selection = ParetoPlusParsimonySelection(
            acceptable=acceptable
        )

        updated_candidate_thresholds.append(candidate_threshold)

    _write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, final_thresholds_output_filename),
        output_fieldnames=final_thresholds_output_fieldnames
    )

    final_threshold = _select_final_threshold_using_pareto_and_parsimony(
        candidate_thresholds=updated_candidate_thresholds
    )

    _write_candidate_threshold_to_file(
        candidate_threshold=final_threshold,
        output_file=os.path.join(results_dir, threshold_output_filename),
        output_fieldnames=final_thresholds_output_fieldnames
    )

    return final_threshold


def generate_final_outputs(
        results_dir: str,
        raw_contributions_filename: str,
        raw_contributions_fieldnames: list,
        candidate_thresholds_filename: str,
        intrinsic_evaluation_filename: str,
        stability_evaluation_filename: str,
        null_model_evaluation_filename: str,
        final_threshold: CandidateThreshold,
        config: RealWorldThresholdEstimationConfig
) -> None:
    candidate_thresholds = _load_csv_rows(os.path.join(results_dir, candidate_thresholds_filename))
    intrinsic_results = _load_csv_rows(os.path.join(results_dir, intrinsic_evaluation_filename))
    stability_results = _load_csv_rows(os.path.join(results_dir, stability_evaluation_filename))
    null_model_results = _load_csv_rows(os.path.join(results_dir, null_model_evaluation_filename))

    e_family_candidate = next(
        (row for row in candidate_thresholds if row["Name"] == CandidateThresholdName.E_FAMILY.value),
        None
    )
    e_global_candidate = next(
        (row for row in candidate_thresholds if row["Name"] == CandidateThresholdName.E_GLOBAL.value),
        None
    )

    e_family_intrinsic = next(
        (row for row in intrinsic_results if row["Name"] == CandidateThresholdName.E_FAMILY.value),
        None
    )

    summary = {
        "Family": final_threshold.family,
        "Network": final_threshold.network,
        "e_family": (e_family_candidate["Value"] if e_family_candidate is not None else None),
        "e_global": (e_global_candidate["Value"] if e_global_candidate is not None else None),
        "e* (Name)": final_threshold.name,
        "e*": final_threshold.value,
        "K'(e_family)": (e_family_intrinsic["K'"] if e_family_intrinsic is not None else None),
        "K'(e*)": final_threshold.intrinsic_evaluation.k_predicted,
        "Modularity": final_threshold.intrinsic_evaluation.modularity,
        "Conductance": final_threshold.intrinsic_evaluation.conductance,
        "Singleton/Near-Singleton Fraction": final_threshold.intrinsic_evaluation.singleton_or_near_singleton_fraction,
        "Largest-Community Fraction": final_threshold.intrinsic_evaluation.largest_community_fraction,
        "Runtime": final_threshold.intrinsic_evaluation.runtime,
        "Stability": final_threshold.stability_evaluation.stability,
        "Z Modularity": final_threshold.null_model_evaluation.modularity_z_score,
        "Modularity Empirical p-value": final_threshold.null_model_evaluation.modularity_empirical_p_value,
        "Modularity Rank": final_threshold.null_model_evaluation.modularity_rank,
        "Z Conductance": final_threshold.null_model_evaluation.conductance_z_score,
        "Conductance Empirical p-value": final_threshold.null_model_evaluation.conductance_empirical_p_value,
        "Conductance Rank": final_threshold.null_model_evaluation.conductance_rank,
        "Acceptable Modularity?": final_threshold.intrinsic_evaluation.acceptable_modularity,
        "Acceptable Conductance?": final_threshold.intrinsic_evaluation.acceptable_conductance,
        "Acceptable Non-Degenerate?": final_threshold.intrinsic_evaluation.acceptable_non_degenerate,
        "Acceptable Stability?": final_threshold.stability_evaluation.acceptable_stability,
        "Acceptable Null Model?": final_threshold.null_model_evaluation.acceptable_null_model,
        "Acceptable?": final_threshold.pareto_plus_parsimony_selection.acceptable
    }

    summary_file = os.path.join(results_dir, "_summary.csv")
    with open(file=summary_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    _plot_candidate_thresholds(
        results_dir=results_dir,
        raw_contributions_filename=raw_contributions_filename,
        raw_contributions_fieldnames=raw_contributions_fieldnames,
        candidate_thresholds=candidate_thresholds,
        final_threshold=final_threshold
    )

    _plot_k_line_by_threshold(results_dir, intrinsic_results)
    _plot_intrinsic_evaluation(results_dir, intrinsic_results)
    _plot_stability_evaluation(results_dir, stability_results)
    _plot_null_model_z_scores(results_dir, null_model_results)
    _plot_null_model_empirical_p_values(results_dir, null_model_results, config.pareto_null_model_p_value_boundary)
    _plot_null_model_empirical_ranks(results_dir, null_model_results)


def evaluate_final_threshold_using_extrinsic_metrics(
        results_dir: str,
        graph_and_matrices: tuple,
        overlapping_ground_truth: bool,
        ground_truth: tuple,
        final_threshold: CandidateThreshold,
        output_filename: str,
        output_base_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> None:
    graph, A, W = graph_and_matrices
    tau, epsilon, k_max = config.tau, final_threshold.value, config.compute_k_max(graph.number_of_nodes())
    ground_truth_labels, k = ground_truth

    U, _, _, _, _, _ = faddis(W=W, epsilon=epsilon, tau=tau, k_max=k_max)

    predicted_labels, k_predicted, _ = apply_defuzzification_rule(
        U=U,
        gamma=config.defuzzification_gamma,
        overlapping=overlapping_ground_truth
    )

    extrinsic_results = compute_extrinsic_metrics(
        graph, ground_truth_labels, predicted_labels, k, k_predicted, overlapping_ground_truth
    )

    if not overlapping_ground_truth:
        extrinsic_fieldnames = ["K' | K", "|K'-K|/K", "AMI", "F-measure", "ARI", "FMI", "NMI", "VI"]
        final_threshold.extrinsic_evaluation = ExtrinsicEvaluation(
            diff_of_k=extrinsic_results.diff_of_k,
            relative_error_of_k=extrinsic_results.relative_error_of_k,
            ami=extrinsic_results.ami,
            f_measure=extrinsic_results.f_measure,
            ari=extrinsic_results.ari,
            fmi=extrinsic_results.fmi,
            nmi=extrinsic_results.nmi,
            vi=extrinsic_results.vi
        )
    else:
        extrinsic_fieldnames = ["K' | K", "|K'-K|/K", "ONMI", "Omega"]
        final_threshold.extrinsic_evaluation = ExtrinsicEvaluation(
            diff_of_k=extrinsic_results.diff_of_k,
            relative_error_of_k=extrinsic_results.relative_error_of_k,
            onmi=extrinsic_results.onmi,
            omega=extrinsic_results.omega
        )

    _write_candidate_threshold_to_file(
        candidate_threshold=final_threshold,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_base_fieldnames + extrinsic_fieldnames
    )


def save_contributions_experiment_report(
        results_dir: str,
        output_filename: str,
        execution_elapsed_time: float,
        config: RealWorldThresholdEstimationConfig
) -> None:
    report = asdict(config)
    report["execution_elapsed_time_secs"] = execution_elapsed_time

    output_file = os.path.join(results_dir, output_filename)
    with open(file=output_file, mode="w", encoding="utf-8") as out_file:
        json.dump(report, out_file, indent=2)


def _evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
        check_modularity: bool = False,
        check_conductance: bool = False,
        check_non_degenerate: bool = False,
        check_stability: bool = False,
        check_null_model: bool = False
) -> None:
    if check_modularity:
        modularities = [threshold.intrinsic_evaluation.modularity for threshold in candidate_thresholds]
        q_max = max(modularities)
        delta_q = config.pareto_tolerance_fraction_modularity * (max(modularities) - min(modularities))

        for threshold in candidate_thresholds:
            threshold.intrinsic_evaluation.acceptable_modularity = (
                    threshold.intrinsic_evaluation.modularity >= q_max - delta_q
            )

    if check_conductance:
        conductances = [threshold.intrinsic_evaluation.conductance for threshold in candidate_thresholds]
        phi_min = min(conductances)
        delta_phi = config.pareto_tolerance_fraction_conductance * (max(conductances) - min(conductances))

        for threshold in candidate_thresholds:
            threshold.intrinsic_evaluation.acceptable_conductance = (
                    threshold.intrinsic_evaluation.conductance <= phi_min + delta_phi
            )

    if check_non_degenerate:
        for threshold in candidate_thresholds:
            threshold.intrinsic_evaluation.acceptable_non_degenerate = (
                    threshold.intrinsic_evaluation.k_predicted > 1
                    and threshold.intrinsic_evaluation.largest_community_fraction < config.pareto_largest_community_fraction_boundary
                    and threshold.intrinsic_evaluation.singleton_or_near_singleton_fraction < config.pareto_singleton_or_near_singleton_fraction_boundary
            )

    if check_stability:
        stabilities = [threshold.stability_evaluation.stability for threshold in candidate_thresholds]
        s_max = max(stabilities)
        delta_s = config.pareto_tolerance_fraction_stability * (max(stabilities) - min(stabilities))

        for threshold in candidate_thresholds:
            threshold.stability_evaluation.acceptable_stability = (
                    threshold.stability_evaluation.stability >= s_max - delta_s
            )

    if check_null_model:
        for threshold in candidate_thresholds:
            modularity_p_value = threshold.null_model_evaluation.modularity_empirical_p_value
            conductance_p_value = threshold.null_model_evaluation.conductance_empirical_p_value

            threshold.null_model_evaluation.acceptable_null_model = (
                    (modularity_p_value is not None and modularity_p_value <= config.pareto_null_model_p_value_boundary)
                    or  # and
                    (
                            conductance_p_value is not None and conductance_p_value <= config.pareto_null_model_p_value_boundary)
            )


def _filter_candidate_thresholds_using_pareto_and_parsimony(
        candidate_thresholds: list[CandidateThreshold],
        number_of_thresholds_to_retain: int,
        check_modularity: bool = False,
        check_conductance: bool = False,
        check_non_degenerate: bool = False,
        check_stability: bool = False,
        keep_e_family: bool = True
) -> list[CandidateThreshold]:
    # Check acceptability
    acceptable_candidate_thresholds = [
        threshold
        for threshold in candidate_thresholds
        if (
                (
                        not check_modularity
                        or threshold.intrinsic_evaluation.acceptable_modularity
                )
                and (
                        not check_conductance
                        or threshold.intrinsic_evaluation.acceptable_conductance
                )
                and (
                        not check_non_degenerate
                        or threshold.intrinsic_evaluation.acceptable_non_degenerate
                )
                and (
                        not check_stability
                        or threshold.stability_evaluation.acceptable_stability
                )
        )
    ]

    # Filter
    if acceptable_candidate_thresholds:
        # Parsimony among acceptable candidates
        acceptable_candidate_thresholds.sort(key=lambda threshold: threshold.value, reverse=True)
        filtered_candidate_thresholds = acceptable_candidate_thresholds[:number_of_thresholds_to_retain]
    else:
        # Fallback: use the evaluation criteria in priority order
        fallback_candidate_thresholds = candidate_thresholds.copy()
        fallback_candidate_thresholds.sort(
            key=lambda threshold: (
                not threshold.intrinsic_evaluation.acceptable_non_degenerate if check_non_degenerate else False,
                -threshold.intrinsic_evaluation.modularity if check_modularity else 0,
                threshold.intrinsic_evaluation.conductance if check_conductance else 0,
                -threshold.stability_evaluation.stability if check_stability else 0,
                -threshold.value
            )
        )
        filtered_candidate_thresholds = fallback_candidate_thresholds[:number_of_thresholds_to_retain]

    # Keep 'e_family' if required
    if keep_e_family:
        if CandidateThresholdName.E_FAMILY not in [threshold.name for threshold in filtered_candidate_thresholds]:
            e_family = next(
                (threshold for threshold in candidate_thresholds if threshold.name == CandidateThresholdName.E_FAMILY),
                None
            )

            if e_family is not None:
                filtered_candidate_thresholds.append(e_family)

    return filtered_candidate_thresholds


def _select_final_threshold_using_pareto_and_parsimony(
        candidate_thresholds: list[CandidateThreshold]
) -> CandidateThreshold:
    # TODO: Check is "e_family" is practically indistinguishable from the best candidate.

    acceptable_thresholds = [th for th in candidate_thresholds if th.pareto_plus_parsimony_selection.acceptable]
    if acceptable_thresholds:
        # Parsimony: prefer the largest thresholds of the acceptable thresholds
        final_threshold = max(acceptable_thresholds, key=lambda th: th.value)
    else:
        # Fallback: Prefer the largest thresholds of the candidate thresholds
        final_threshold = max(candidate_thresholds, key=lambda th: th.value)

    return final_threshold


def _median_or_none(values: list[float]) -> float:
    if len(values) == 0:
        return None

    return float(np.median(values))


def _write_candidate_thresholds_to_file(
        candidate_thresholds: list[CandidateThreshold],
        output_file,
        output_fieldnames
):
    with open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerows(threshold.to_dict() for threshold in candidate_thresholds)


def _write_candidate_threshold_to_file(
        candidate_threshold: CandidateThreshold,
        output_file,
        output_fieldnames
):
    candidate_threshold_dict = candidate_threshold.to_dict()
    output_row = {fieldname: candidate_threshold_dict.get(fieldname) for fieldname in output_fieldnames}

    with open(file=output_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=output_fieldnames)
        writer.writeheader()
        writer.writerow(output_row)


def _generate_a_perturbed_graph(
        graph: nx.Graph,
        number_of_swaps: int,
        apply_lapin: bool,
        seed: int
) -> tuple[nx.Graph, np.ndarray, np.ndarray]:
    perturbed_graph = graph.copy()
    successful_swaps = connected_double_edge_swap(perturbed_graph, nswap=number_of_swaps, seed=seed)
    print(f"[DEBUG] {number_of_swaps} / {successful_swaps}")

    perturbed_A = compute_adjacency_matrix(perturbed_graph)
    perturbed_W = np.asarray(perturbed_A if not apply_lapin else lapin(perturbed_A), dtype=np.float64)

    return perturbed_graph, perturbed_A, perturbed_W


def _compute_fuzzy_co_membership_similarity(
        U: np.ndarray,
        first_cluster_discarded: bool,
        perturbed_U: np.ndarray,
        perturbed_first_cluster_discarded: bool
) -> float:
    U = np.asarray(U)[:, 1:] if first_cluster_discarded else np.asarray(U)
    perturbed_U = np.asarray(perturbed_U)[:, 1:] if perturbed_first_cluster_discarded else np.asarray(perturbed_U)

    if U.shape[1] == 0 or perturbed_U.shape[1] == 0:
        return None

    co_membership = U @ U.T
    perturbed_co_membership = perturbed_U @ perturbed_U.T

    denominator = (norm(co_membership, "fro") * norm(perturbed_co_membership, "fro"))
    if denominator == 0:
        return None

    similarity = (np.sum(co_membership * perturbed_co_membership) / denominator)

    return float(np.clip(similarity, 0.0, 1.0))


def _load_csv_rows(input_file: str) -> list[dict]:
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
        return list(csv.DictReader(in_file))


def _plot_candidate_thresholds(
        results_dir: str,
        raw_contributions_filename: str,
        raw_contributions_fieldnames: list,
        candidate_thresholds: list[dict],
        final_threshold: CandidateThreshold
) -> None:
    input_file = os.path.join(results_dir, raw_contributions_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        next(reader, None)
        network = next(reader, None)

    contributions = [float(value) for value in network[len(raw_contributions_fieldnames):] if value != ""]
    extraction_numbers = list(range(1, len(contributions) + 1))

    plt.figure()
    plt.plot(extraction_numbers, contributions, marker="o", markersize=4, linewidth=1.5)
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for candidate in candidate_thresholds:
        if candidate["Value"] in [None, ""]:
            continue

        candidate_name = candidate["Name"]
        candidate_value = float(candidate["Value"])
        style = THRESHOLD_PLOT_STYLES.get(candidate_name, {"label": candidate_name, "color": "black"})

        if candidate_name == final_threshold.name.value:
            plt.axhline(
                final_threshold.value,
                color=style["color"],
                linewidth=2,
                label=f'{style["label"]} = {round(final_threshold.value, 6)}'
            )
        else:
            plt.axhline(
                candidate_value,
                color=style["color"],
                linestyle="--",
                label=f'{style["label"]} = {round(candidate_value, 6)}'
            )

    plt.xlabel("Extraction Number")
    plt.ylabel("Contribution")

    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend(handles=handles, labels=labels, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_candidate_thresholds_plot.pdf"))
    plt.close()


def _plot_k_line_by_threshold(
        results_dir: str,
        intrinsic_results: list[dict]
) -> None:
    points = sorted(
        [
            (np.log(float(row["Value"])), int(row["K'"]), row["Name"])
            for row in intrinsic_results if row["Value"] not in [None, ""]
        ],
        key=lambda point: point[0]
    )

    if not points:
        return

    log_thresholds = [point[0] for point in points]
    k_values = [point[1] for point in points]

    plt.figure()
    plt.plot(log_thresholds, k_values, linestyle="--")
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for log_threshold, k_value, name in points:
        style = THRESHOLD_PLOT_STYLES.get(name, {"label": name, "color": "black", "marker": "o"})
        plt.plot(
            log_threshold,
            k_value,
            marker=style["marker"],
            color=style["color"],
            linestyle="None",
            markersize=5,
            label=style["label"]
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel(r"$K'(\epsilon)$")

    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend(handles=handles, labels=labels, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_k_line_by_threshold_plot.pdf"))
    plt.close()


def _plot_intrinsic_evaluation(
        results_dir: str,
        intrinsic_results: list[dict]
) -> None:
    points = sorted(
        [
            (row["Name"], np.log(float(row["Value"])), float(row["Modularity"]), float(row["Conductance"]))
            for row in intrinsic_results if row["Value"] not in [None, ""]
        ],
        key=lambda point: point[1]
    )

    if not points:
        return

    threshold_names = [point[0] for point in points]
    log_thresholds = [point[1] for point in points]
    modularities = [point[2] for point in points]
    conductances = [point[3] for point in points]

    plt.figure()
    plt.plot(log_thresholds, modularities, linestyle="--", color="tab:blue", label="Modularity")
    plt.plot(log_thresholds, conductances, linestyle=":", color="tab:orange", label="Conductance")
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for threshold_name, log_threshold, modularity, conductance in zip(
            threshold_names,
            log_thresholds,
            modularities,
            conductances
    ):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        plt.plot(log_threshold, modularity, marker=style["marker"], color="tab:blue", linestyle="None")
        plt.plot(log_threshold, conductance, marker=style["marker"], color="tab:orange", linestyle="None")

    legend_handles = [
        Line2D([0], [0], color="tab:blue", linestyle="--", label="Modularity"),
        Line2D([0], [0], color="tab:orange", linestyle=":", label="Conductance")
    ]

    for threshold_name in dict.fromkeys(threshold_names):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        legend_handles.append(
            Line2D([0], [0], color="black", marker=style["marker"], linestyle="None", label=style["label"])
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel("Intrinsic Metric")

    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_intrinsic_evaluation_plot.pdf"))
    plt.close()


def _plot_stability_evaluation(
        results_dir: str,
        stability_results: list[dict]
) -> None:
    if not stability_results:
        return

    names = [row["Name"] for row in stability_results]
    labels = [THRESHOLD_PLOT_STYLES.get(name, {"label": name})["label"] for name in names]
    colors = [THRESHOLD_PLOT_STYLES.get(name, {"color": "black"})["color"] for name in names]
    stabilities = [float(row["Stability"]) for row in stability_results]

    plt.figure()
    plt.bar(labels, stabilities, color=colors)
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    plt.xlabel(r"$\epsilon$")
    plt.ylabel("Stability")
    plt.tight_layout()

    plt.savefig(os.path.join(results_dir, "_stability_evaluation_plot.pdf"))
    plt.close()


def _plot_null_model_z_scores(
        results_dir: str,
        null_model_results: list[dict]
) -> None:
    points = sorted(
        [
            (
                row["Name"],
                np.log(float(row["Value"])),
                float(row["Z Modularity"]),
                float(row["Z Conductance"])
            )
            for row in null_model_results
            if (
                row["Value"] not in [None, ""]
                and row["Z Modularity"] not in [None, ""]
                and row["Z Conductance"] not in [None, ""]
        )
        ],
        key=lambda point: point[1]
    )

    if not points:
        return

    threshold_names = [point[0] for point in points]
    log_thresholds = [point[1] for point in points]
    modularity_z_scores = [point[2] for point in points]
    conductance_z_scores = [point[3] for point in points]

    plt.figure()

    plt.plot(log_thresholds, modularity_z_scores, linestyle="--", color="tab:blue", label="Z Modularity")
    plt.plot(log_thresholds, conductance_z_scores, linestyle=":", color="tab:orange", label="Z Conductance")
    plt.axhline(y=0, color="black", linewidth=1, linestyle="-")
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for threshold_name, log_threshold, modularity_z_score, conductance_z_score in zip(
            threshold_names,
            log_thresholds,
            modularity_z_scores,
            conductance_z_scores
    ):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        plt.plot(log_threshold, modularity_z_score, marker=style["marker"], color="tab:blue", linestyle="None")
        plt.plot(log_threshold, conductance_z_score, marker=style["marker"], color="tab:orange", linestyle="None")

    legend_handles = [
        Line2D([0], [0], color="tab:blue", linestyle="--", label="Z Modularity"),
        Line2D([0], [0], color="tab:orange", linestyle=":", label="Z Conductance")
    ]

    for threshold_name in dict.fromkeys(threshold_names):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        legend_handles.append(
            Line2D([0], [0], color="black", marker=style["marker"], linestyle="None", label=style["label"])
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel("Null-Model Z-Score")

    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_null_model_z_scores_plot.pdf"))
    plt.close()


def _plot_null_model_empirical_p_values(
        results_dir: str,
        null_model_results: list[dict],
        p_value_boundary: float
) -> None:
    points = sorted(
        [
            (
                row["Name"],
                np.log(float(row["Value"])),
                float(row["Modularity Empirical p-value"]),
                float(row["Conductance Empirical p-value"])
            )
            for row in null_model_results
            if (
                row["Value"] not in [None, ""]
                and row["Modularity Empirical p-value"] not in [None, ""]
                and row["Conductance Empirical p-value"] not in [None, ""]
        )
        ],
        key=lambda point: point[1]
    )

    if not points:
        return

    threshold_names = [point[0] for point in points]
    log_thresholds = [point[1] for point in points]
    modularity_p_values = [point[2] for point in points]
    conductance_p_values = [point[3] for point in points]

    plt.figure()

    plt.plot(log_thresholds, modularity_p_values, linestyle="--", color="tab:blue")
    plt.plot(log_thresholds, conductance_p_values, linestyle=":", color="tab:orange")

    plt.axhline(y=p_value_boundary, color="black", linestyle="-.", linewidth=1)
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for threshold_name, log_threshold, modularity_p_value, conductance_p_value in zip(
            threshold_names,
            log_thresholds,
            modularity_p_values,
            conductance_p_values
    ):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        plt.plot(log_threshold, modularity_p_value, marker=style["marker"], color="tab:blue", linestyle="None")
        plt.plot(log_threshold, conductance_p_value, marker=style["marker"], color="tab:orange", linestyle="None")

    legend_handles = [
        Line2D([0], [0], color="tab:blue", linestyle="--", label="Modularity empirical p-value"),
        Line2D([0], [0], color="tab:orange", linestyle=":", label="Conductance empirical p-value"),
        Line2D([0], [0], color="black", linestyle="-.", label=f"Boundary = {p_value_boundary:g}")
    ]

    for threshold_name in dict.fromkeys(threshold_names):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        legend_handles.append(
            Line2D([0], [0], color="black", marker=style["marker"], linestyle="None", label=style["label"])
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel("Empirical p-value")
    plt.ylim(0.0, 1.0)
    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_null_model_empirical_p_values_plot.pdf"))
    plt.close()


def _plot_null_model_empirical_ranks(
        results_dir: str,
        null_model_results: list[dict]
) -> None:
    valid_results = [
        row
        for row in null_model_results
        if (
                row["Modularity Rank"] not in [None, ""]
                and row["Conductance Rank"] not in [None, ""]
        )
    ]

    if not valid_results:
        return

    names = [row["Name"] for row in valid_results]
    labels = [THRESHOLD_PLOT_STYLES.get(name, {"label": name})["label"] for name in names]
    colors = [THRESHOLD_PLOT_STYLES.get(name, {"color": "black"})["color"] for name in names]

    modularity_ranks = [int(row["Modularity Rank"]) for row in valid_results]
    conductance_ranks = [int(row["Conductance Rank"]) for row in valid_results]

    x = np.arange(len(labels))
    width = 0.35

    plt.figure()
    plt.bar(x - width / 2, modularity_ranks, width, color=colors, edgecolor="black", hatch="//")
    plt.bar(x + width / 2, conductance_ranks, width, color=colors, edgecolor="black", hatch="\\")

    legend_handles = [
        Patch(facecolor="white", edgecolor="black", hatch="//", label="Modularity rank"),
        Patch(facecolor="white", edgecolor="black", hatch="\\", label="Conductance rank")
    ]

    for name in dict.fromkeys(names):
        style = THRESHOLD_PLOT_STYLES.get(name, {"label": name, "color": "black"})

        legend_handles.append(
            Patch(facecolor=style["color"], label=style["label"])
        )

    plt.xticks(x, labels)
    plt.ylabel("Empirical Rank")
    plt.xlabel(r"$\epsilon$")
    plt.yticks(np.arange(0, max(modularity_ranks + conductance_ranks) + 1, 1))

    plt.grid(axis="y", linestyle=":", alpha=0.5)
    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_null_model_empirical_ranks_plot.pdf"))
    plt.close()
