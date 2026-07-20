import os

from experiments.faddis.faddis import faddis
from experiments.scripts.real_world_networks.thresholds.network_thresholds.extrinsic_evaluation.extrinsic_evaluation_dataclass import \
    ExtrinsicEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.extrinsic_evaluation.extrinsic_metrics.extrinsic_metrics import \
    compute_extrinsic_metrics
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.thresholds.utils.utils import write_candidate_threshold_to_file
from experiments.scripts.real_world_networks.utils.defuzzification.defuzzification import apply_defuzzification_rule


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
    """
    Evaluate the selected threshold using extrinsic community-detection metrics.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        graph_and_matrices : (tuple[nx.Graph, np.ndarray, np.ndarray])
            Original graph, adjacency matrix, and affinity matrix.
        overlapping_ground_truth : (bool)
            Whether the ground-truth community structure is overlapping.
        ground_truth : (tuple[list, int])
            Ground-truth community labels and number of communities.
        final_threshold : (CandidateThreshold)
            Selected candidate threshold.
        output_filename : (str)
            Name of the output CSV file.
        output_base_fieldnames : (list)
            Base field names included in the output CSV file.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

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

    write_candidate_threshold_to_file(
        candidate_threshold=final_threshold,
        output_file=os.path.join(results_dir, output_filename),
        output_fieldnames=output_base_fieldnames + extrinsic_fieldnames
    )
