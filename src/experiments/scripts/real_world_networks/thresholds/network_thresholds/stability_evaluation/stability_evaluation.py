import os

import networkx as nx
import numpy as np
from numpy.linalg import norm
from sklearn.metrics import normalized_mutual_info_score

from experiments.faddis.faddis import faddis
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_filtering_and_parsimony_selection import \
    evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto, \
    filter_candidate_thresholds_using_pareto_and_parsimony
from experiments.scripts.real_world_networks.thresholds.network_thresholds.stability_evaluation.stability_evaluation_dataclass import \
    StabilityEvaluation
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.thresholds.utils.utils import generate_a_perturbed_graph, \
    write_candidate_thresholds_to_file
from experiments.scripts.real_world_networks.utils.defuzzification.defuzzification import apply_defuzzification_rule


def evaluate_candidate_thresholds_under_perturbation_stability(
        results_dir: str,
        graph_and_matrices: tuple,
        candidate_thresholds: list[CandidateThreshold],
        output_filename: str,
        output_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> list[CandidateThreshold]:
    """
    Evaluate candidate thresholds under graph perturbations.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        graph_and_matrices : (tuple[nx.Graph, np.ndarray, np.ndarray])
            Original graph, adjacency matrix, and affinity matrix.
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds retained after intrinsic evaluation.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list)
            Field names of the output CSV file.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        filtered_candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds retained after stability evaluation, Pareto filtering, and parsimony.
    """

    graph, _, W = graph_and_matrices
    tau, k_max = config.tau, config.compute_k_max(graph.number_of_nodes())

    perturbed_Ws = []
    number_of_swaps = config.compute_number_of_edges_swaps_in_perturbed_graphs(graph.number_of_edges())
    for perturbation_number in range(1, config.number_of_perturbed_graphs + 1):
        _, _, perturbed_W = generate_a_perturbed_graph(
            graph=graph,
            number_of_swaps=number_of_swaps,
            affinity_design=config.affinity_design,
            apply_lapin=config.apply_lapin,
            seed=perturbation_number
        )
        perturbed_Ws.append(perturbed_W)

    updated_candidate_thresholds = []
    for candidate_threshold in candidate_thresholds:
        U, _, _, _, _, _ = faddis(W=W, epsilon=candidate_threshold.value, tau=tau, k_max=k_max)
        predicted_labels, k_predicted, first_cluster_discarded = apply_defuzzification_rule(
            U=U,
            gamma=config.defuzzification_gamma,
            overlapping=config.overlapping_communities
        )

        sims = _compute_similarities(
            candidate_threshold=candidate_threshold,
            graph=graph,
            predicted_labels=predicted_labels,
            U=U,
            first_cluster_discarded=first_cluster_discarded,
            perturbed_Ws=perturbed_Ws,
            config=config
        )

        stability = _compute_stability(
            sims=sims,
            number_of_perturbed_graphs=config.number_of_perturbed_graphs
        )

        candidate_threshold.stability_evaluation = StabilityEvaluation(
            number_of_perturbed_graphs=config.number_of_perturbed_graphs,
            number_of_valid_similarities=len(sims),
            similarities=sims,
            stability=stability
        )

        updated_candidate_thresholds.append(candidate_threshold)

    evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds=updated_candidate_thresholds,
        config=config,
        check_stability=True
    )

    write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_fieldnames
    )

    filtered_candidate_thresholds = filter_candidate_thresholds_using_pareto_and_parsimony(
        candidate_thresholds=updated_candidate_thresholds,
        number_of_thresholds_to_retain=config.number_of_thresholds_to_retain_after_stability_evaluation,
        check_modularity=True,
        check_conductance=True,
        check_non_degenerate=True,
        check_stability=True
    )

    return filtered_candidate_thresholds


def _compute_similarities(
        candidate_threshold: CandidateThreshold,
        graph: nx.Graph,
        predicted_labels: list,
        U: np.ndarray,
        first_cluster_discarded: bool,
        perturbed_Ws: list,
        config: RealWorldThresholdEstimationConfig,
):
    """
    Compute similarities between the original community structure and those obtained from perturbed affinity matrices.

    Parameters:
        candidate_threshold : (CandidateThreshold)
            Candidate threshold whose value is used as the FADDIS stopping threshold.
        graph : (nx.Graph)
            Original network, used to determine the maximum number of clusters.
        predicted_labels : (list[list[int]], length n | list[int], length n)
            Predicted community labels obtained for the original network.
        U : (np.ndarray, shape[n,k])
            Fuzzy membership matrix obtained for the original network.
        first_cluster_discarded : (bool)
            Whether the first cluster was discarded from the original community structure.
        perturbed_Ws : (list[np.ndarray])
            Affinity matrices obtained from perturbed versions of the original network.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        sims : (list[float])
            Similarity values between the original community structure and the valid community
            structures obtained from the perturbed affinity matrices.
    """

    tau, k_max = config.tau, config.compute_k_max(graph.number_of_nodes())

    sims = []
    for perturbed_W in perturbed_Ws:
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

    return sims


def _compute_stability(sims: list[float], number_of_perturbed_graphs: int) -> float:
    """
    Compute the average stability from a list of similarity values.

    Parameters:
        sims : (list[float])
            Similarity values obtained from the perturbed community structures.
        number_of_perturbed_graphs : (int)
            Total number of perturbed graphs.

    Returns:
        stability : (float)
            Average similarity across the perturbed community structures.
            Returns 0 if no similarity values are provided.
    """

    return float(sum(sims) / number_of_perturbed_graphs)


def _compute_fuzzy_co_membership_similarity(
        U: np.ndarray,
        first_cluster_discarded: bool,
        perturbed_U: np.ndarray,
        perturbed_first_cluster_discarded: bool
) -> float:
    """
    Compute the fuzzy co-membership similarity between two fuzzy community structures.

    Parameters:
        U : (np.ndarray, shape[n,k])
            Fuzzy membership matrix of the original community structure.
        first_cluster_discarded : (bool)
            Whether the first cluster was discarded from the original community structure.
        perturbed_U : (np.ndarray, shape[n,k'])
            Fuzzy membership matrix of the perturbed community structure.
        perturbed_first_cluster_discarded : (bool)
            Whether the first cluster was discarded from the perturbed community structure.

    Returns:
        similarity : (float | None)
            Frobenius cosine similarity between the fuzzy co-membership matrices, bounded to the range [0, 1].
            None if either membership matrix has no clusters or if the similarity denominator is zero.
    """

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
