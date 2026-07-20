import os

import networkx as nx
import numpy as np

from experiments.faddis.faddis import faddis
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.intrinsic_metrics.intrinsic_metrics import \
    compute_intrinsic_metrics
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold
from experiments.scripts.real_world_networks.thresholds.network_thresholds.null_model_evaluation.null_model_evaluation_dataclass import \
    NullModelEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_filtering_and_parsimony_selection import \
    evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.thresholds.utils.utils import generate_a_perturbed_graph, \
    write_candidate_thresholds_to_file
from experiments.scripts.real_world_networks.utils.defuzzification.defuzzification import apply_defuzzification_rule


def evaluate_candidate_thresholds_under_null_model(
        results_dir: str,
        graph_and_matrices: tuple,
        candidate_thresholds: list[CandidateThreshold],
        output_filename: str,
        output_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> list[CandidateThreshold]:
    """
    Evaluate candidate thresholds using null-model graphs.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        graph_and_matrices : (tuple[nx.Graph, np.ndarray, np.ndarray])
            Original graph, adjacency matrix, and affinity matrix.
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds retained after stability evaluation.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list)
            Field names of the output CSV file.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        updated_candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds containing their null-model evaluation results.
    """

    graph, A, W = graph_and_matrices

    null_graphs_and_matrices = []
    number_of_swaps = config.compute_number_of_edges_swaps_in_null_models(graph.number_of_edges())
    for null_number in range(1, config.number_of_null_models + 1):
        null_graph, null_A, null_W = generate_a_perturbed_graph(
            graph=graph,
            number_of_swaps=number_of_swaps,
            affinity_design=config.affinity_design,
            apply_lapin=config.apply_lapin,
            seed=null_number
        )
        null_graphs_and_matrices.append((null_graph, null_A, null_W))

    updated_candidate_thresholds = []
    for candidate_threshold in candidate_thresholds:
        null_modularities, null_conductances = _compute_null_modularities_and_conductances(
            candidate_threshold=candidate_threshold,
            graph=graph,
            null_graphs_and_matrices=null_graphs_and_matrices,
            config=config
        )

        mean_null_modularity, std_null_modularity, modularity_z_score, modularity_empirical_p_value, modularity_rank = (
            _compute_null_modularities_statistics(
                candidate_threshold=candidate_threshold,
                null_modularities=null_modularities,
                number_of_null_models=config.number_of_null_models
            )
        )

        mean_null_conductance, std_null_conductance, conductance_z_score, conductance_empirical_p_value, conductance_rank = (
            _compute_null_conductances_statistics(
                candidate_threshold=candidate_threshold,
                null_conductances=null_conductances,
                number_of_null_models=config.number_of_null_models
            )
        )

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

    evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds=updated_candidate_thresholds,
        config=config,
        check_null_model=True
    )

    write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_fieldnames
    )

    return updated_candidate_thresholds


def _compute_null_modularities_and_conductances(
        candidate_threshold: CandidateThreshold,
        graph: nx.Graph,
        null_graphs_and_matrices: list,
        config: RealWorldThresholdEstimationConfig,
):
    """
    Compute modularity and conductance values for a candidate threshold across null-model networks.

    Parameters:
        candidate_threshold : (CandidateThreshold)
            Candidate threshold whose value is used as the FADDIS stopping threshold.
        graph : (nx.Graph)
            Original network, used to determine the maximum number of clusters.
        null_graphs_and_matrices : (list[tuple[nx.Graph, np.ndarray, np.ndarray]])
            List containing each null-model graph, its adjacency matrix, and its affinity matrix.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        null_modularities : (list[float])
            Modularity or fuzzy modularity values obtained from the valid null-model community structures.
        null_conductances : (list[float])
            Conductance or boundary-node conductance values obtained from the valid null-model community structures.
    """

    tau, k_max = config.tau, config.compute_k_max(graph.number_of_nodes())

    null_modularities = []
    null_conductances = []

    for null_graph_and_matrices in null_graphs_and_matrices:
        null_graph, null_A, null_W = null_graph_and_matrices

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

    return null_modularities, null_conductances


def _compute_null_modularities_statistics(
        candidate_threshold: CandidateThreshold,
        null_modularities: list,
        number_of_null_models: int
) -> tuple[float, float, float, float, int]:
    """
    Compute modularity statistics by comparing a candidate threshold against null-model results.

    Parameters:
        candidate_threshold : (CandidateThreshold)
            Candidate threshold containing the modularity obtained for the real network.
        null_modularities : (list[float])
            Modularity values obtained from the null-model networks.
        number_of_null_models : (int)
            Total number of null models.

    Returns:
        mean_null_modularity : (float | None)
            Mean modularity across the null-model networks.
            None if no null modularities are provided.
        std_null_modularity : (float | None)
            Sample standard deviation of the null-model modularities.
            None if no null modularities are provided.
        modularity_z_score : (float | None)
            Standardized difference between the real modularity and the mean null modularity (Z score).
            None if no null modularities are provided or the standard deviation is zero.
        modularity_empirical_p_value : (float | None)
            Empirical upper-tail p-value of the real modularity under the null model.
            None if no null modularities are provided.
        modularity_rank : (int | None)
            Rank of the real modularity among the null-model modularities.
            None if no null modularities are provided.
    """

    number_of_invalid_results = number_of_null_models - len(null_modularities)

    if not null_modularities:
        return None, None, None, 1.0, number_of_null_models + 1

    real_modularity = candidate_threshold.intrinsic_evaluation.modularity

    mean_null_modularity = float(np.mean(null_modularities))
    std_null_modularity = float(np.std(null_modularities, ddof=1)) if len(null_modularities) > 1 else 0.0
    modularity_z_score = (
        (real_modularity - mean_null_modularity) / std_null_modularity
        if std_null_modularity > 0 else None
    )
    modularity_empirical_p_value = (
            (1 + number_of_invalid_results + sum(q_null >= real_modularity for q_null in null_modularities)) /
            (number_of_null_models + 1))
    modularity_rank = (
            1 + number_of_invalid_results + sum(q_null > real_modularity for q_null in null_modularities)
    )

    return mean_null_modularity, std_null_modularity, modularity_z_score, modularity_empirical_p_value, modularity_rank


def _compute_null_conductances_statistics(
        candidate_threshold: CandidateThreshold,
        null_conductances: list,
        number_of_null_models: int
) -> tuple[float, float, float, float, int]:
    """
    Compute conductance statistics by comparing a candidate threshold against null-model results.

    Parameters:
        candidate_threshold : (CandidateThreshold)
            Candidate threshold containing the conductance obtained for the real network.
        null_conductances : (list[float])
            Conductance values obtained from the null-model networks.
        number_of_null_models : (int)
            Total number of null models.

    Returns:
        mean_null_conductance : (float | None)
            Mean conductance across the null-model networks.
            None if no null conductances are provided.
        std_null_conductance : (float | None)
            Sample standard deviation of the null-model conductances.
            None if no null conductances are provided.
        conductance_z_score : (float | None)
            Standardized difference between the mean null conductance and the real conductance (Z score).
            None if no null conductances are provided or the standard deviation is zero.
        conductance_empirical_p_value : (float | None)
            Empirical lower-tail p-value of the real conductance under the null model.
            None if no null conductances are provided.
        conductance_rank : (int | None)
            Rank of the real conductance among the null-model conductances.
            None if no null conductances are provided.
    """

    number_of_invalid_results = number_of_null_models - len(null_conductances)

    if not null_conductances:
        return None, None, None, 1.0, number_of_null_models + 1

    real_conductance = candidate_threshold.intrinsic_evaluation.conductance

    mean_null_conductance = float(np.mean(null_conductances))
    std_null_conductance = float(np.std(null_conductances, ddof=1)) if len(null_conductances) > 1 else 0.0
    conductance_z_score = (
        (mean_null_conductance - real_conductance) / std_null_conductance
        if std_null_conductance > 0 else None
    )
    conductance_empirical_p_value = (
            (1 + number_of_invalid_results + sum(phi_null <= real_conductance for phi_null in null_conductances)) /
            (number_of_null_models + 1))
    conductance_rank = (
            1 + number_of_invalid_results + sum(phi_null < real_conductance for phi_null in null_conductances)
    )

    return mean_null_conductance, std_null_conductance, conductance_z_score, conductance_empirical_p_value, conductance_rank
