import os

import numpy as np

from experiments.faddis.faddis import faddis
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.community_properties.community_properties import \
    compute_community_properties
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.computational_metrics.computational_metrics import \
    get_computation_start_time, get_computation_end_time, compute_computational_metrics
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.intrinsic_evaluation_dataclass import \
    IntrinsicEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.intrinsic_metrics.intrinsic_metrics import \
    compute_intrinsic_metrics
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_filtering_and_parsimony_selection import \
    evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto, \
    filter_candidate_thresholds_using_pareto_and_parsimony
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.thresholds.utils.defuzzification import apply_defuzzification_rule
from experiments.scripts.real_world_networks.thresholds.utils.utils import write_candidate_thresholds_to_file


def evaluate_candidate_thresholds_using_intrinsic_metrics(
        results_dir: str,
        graph_and_matrices: tuple,
        candidate_thresholds: list[CandidateThreshold],
        output_filename: str,
        output_fieldnames: list,
        config: RealWorldThresholdEstimationConfig
) -> list[CandidateThreshold]:
    """
    Evaluate candidate thresholds using intrinsic community-detection metrics.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        graph_and_matrices : (tuple[nx.Graph, np.ndarray, np.ndarray])
            Original graph, adjacency matrix, and affinity matrix.
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds to evaluate.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list)
            Field names of the output CSV file.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        filtered_candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds retained after intrinsic evaluation, Pareto filtering, and parsimony.
    """

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

        predicted_labels, _, first_cluster_discarded = apply_defuzzification_rule(
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

    evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds=updated_candidate_thresholds,
        config=config,
        check_modularity=True,
        check_conductance=True,
        check_non_degenerate=True
    )

    write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_fieldnames
    )

    filtered_candidate_thresholds = filter_candidate_thresholds_using_pareto_and_parsimony(
        candidate_thresholds=updated_candidate_thresholds,
        number_of_thresholds_to_retain=config.number_of_thresholds_to_retain_after_intrinsic_evaluation,
        check_modularity=True,
        check_conductance=True,
        check_non_degenerate=True
    )

    return filtered_candidate_thresholds
