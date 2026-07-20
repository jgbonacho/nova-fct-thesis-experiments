import os

from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold, CandidateThresholdName
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_plus_parsimony_selection_dataclass import \
    ParetoPlusParsimonySelection
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.thresholds.utils.utils import write_candidate_thresholds_to_file, \
    write_candidate_threshold_to_file


def select_final_threshold_by_pareto_and_parsimony(
        results_dir: str,
        candidate_thresholds: list[CandidateThreshold],
        final_thresholds_output_filename: str,
        final_thresholds_output_fieldnames: list,
        threshold_output_filename: str
) -> CandidateThreshold:
    """
    Select the final threshold using Pareto acceptability and parsimony.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds containing all evaluation results.
        final_thresholds_output_filename : (str)
            Name of the output CSV file containing all final candidate evaluations.
        final_thresholds_output_fieldnames : (list)
            Field names of the final candidate evaluation CSV file.
        threshold_output_filename : (str)
            Name of the output CSV file containing the selected threshold.

    Returns:
        final_threshold : (CandidateThreshold)
            Candidate threshold selected using Pareto acceptability and parsimony.
    """

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

    write_candidate_thresholds_to_file(
        candidate_thresholds=updated_candidate_thresholds,
        output_file=os.path.join(results_dir, final_thresholds_output_filename),
        output_fieldnames=final_thresholds_output_fieldnames
    )

    final_threshold = select_final_threshold_using_pareto_and_parsimony(
        candidate_thresholds=updated_candidate_thresholds
    )

    write_candidate_threshold_to_file(
        candidate_threshold=final_threshold,
        output_file=os.path.join(results_dir, threshold_output_filename),
        output_fieldnames=final_thresholds_output_fieldnames
    )

    return final_threshold


def evaluate_acceptability_in_place_of_candidate_thresholds_using_pareto(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
        check_modularity: bool = False,
        check_conductance: bool = False,
        check_non_degenerate: bool = False,
        check_stability: bool = False,
        check_null_model: bool = False
) -> None:
    """
    Evaluate the acceptability criteria of candidate thresholds in place using Pareto-based rules.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds whose acceptability fields are updated.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.
        check_modularity : (bool, optional)
            If True, evaluate modularity acceptability.
            Default is False.
        check_conductance : (bool, optional)
            If True, evaluate conductance acceptability.
            Default is False.
        check_non_degenerate : (bool, optional)
            If True, evaluate non-degeneracy acceptability.
            Default is False.
        check_stability : (bool, optional)
            If True, evaluate stability acceptability.
            Default is False.
        check_null_model : (bool, optional)
            If True, evaluate null-model acceptability.
            Default is False.

    Returns:
        None
    """

    if check_modularity:
        _check_modularity(candidate_thresholds, config)

    if check_conductance:
        _check_conductance(candidate_thresholds, config)

    if check_non_degenerate:
        _check_non_degenerate(candidate_thresholds, config)

    if check_stability:
        _check_stability(candidate_thresholds, config)

    if check_null_model:
        _check_null_model(candidate_thresholds, config)


def _check_modularity(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
):
    """
    Evaluate modularity acceptability in place using a Pareto tolerance.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds whose modularity acceptability field is updated.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    modularities = [threshold.intrinsic_evaluation.modularity for threshold in candidate_thresholds]
    q_max = max(modularities)
    delta_q = config.pareto_tolerance_fraction_modularity * (max(modularities) - min(modularities))

    for threshold in candidate_thresholds:
        threshold.intrinsic_evaluation.acceptable_modularity = (
                threshold.intrinsic_evaluation.modularity >= q_max - delta_q
        )


def _check_conductance(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
):
    """
    Evaluate conductance acceptability in place using a Pareto tolerance.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds whose conductance acceptability field is updated.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    conductances = [threshold.intrinsic_evaluation.conductance for threshold in candidate_thresholds]
    phi_min = min(conductances)
    delta_phi = config.pareto_tolerance_fraction_conductance * (max(conductances) - min(conductances))

    for threshold in candidate_thresholds:
        threshold.intrinsic_evaluation.acceptable_conductance = (
                threshold.intrinsic_evaluation.conductance <= phi_min + delta_phi
        )


def _check_non_degenerate(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
):
    """
    Evaluate non-degeneracy acceptability in place.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds whose non-degeneracy acceptability field is updated.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    for threshold in candidate_thresholds:
        threshold.intrinsic_evaluation.acceptable_non_degenerate = (
                threshold.intrinsic_evaluation.k_predicted > 1
                and threshold.intrinsic_evaluation.largest_community_fraction < config.pareto_largest_community_fraction_boundary
                and threshold.intrinsic_evaluation.singleton_or_near_singleton_fraction < config.pareto_singleton_or_near_singleton_fraction_boundary
        )


def _check_stability(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
):
    """
    Evaluate stability acceptability in place using a Pareto tolerance.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds whose stability acceptability field is updated.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    stabilities = [threshold.stability_evaluation.stability for threshold in candidate_thresholds]
    s_max = max(stabilities)
    delta_s = config.pareto_tolerance_fraction_stability * (max(stabilities) - min(stabilities))

    for threshold in candidate_thresholds:
        threshold.stability_evaluation.acceptable_stability = (
                threshold.stability_evaluation.stability >= s_max - delta_s
        )


def _check_null_model(
        candidate_thresholds: list[CandidateThreshold],
        config: RealWorldThresholdEstimationConfig,
):
    """
    Evaluate null-model acceptability in place using modularity and conductance evidence.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds whose null-model acceptability field is updated.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    for threshold in candidate_thresholds:
        null_evaluation = threshold.null_model_evaluation

        modularity_is_acceptable = (
                null_evaluation.modularity_z_score is not None
                and null_evaluation.modularity_z_score >= config.pareto_null_model_z_score_boundary
                and null_evaluation.modularity_empirical_p_value is not None
                and null_evaluation.modularity_empirical_p_value <= config.pareto_null_model_p_value_boundary
                and null_evaluation.modularity_rank is not None
                and null_evaluation.modularity_rank <= config.pareto_null_model_rank_boundary

        )

        conductance_is_acceptable = (
                null_evaluation.conductance_z_score is not None
                and null_evaluation.conductance_z_score >= config.pareto_null_model_z_score_boundary
                and null_evaluation.conductance_empirical_p_value is not None
                and null_evaluation.conductance_empirical_p_value <= config.pareto_null_model_p_value_boundary
                and null_evaluation.conductance_rank is not None
                and null_evaluation.conductance_rank <= config.pareto_null_model_rank_boundary
        )

        null_evaluation.acceptable_null_model = modularity_is_acceptable and conductance_is_acceptable


def filter_candidate_thresholds_using_pareto_and_parsimony(
        candidate_thresholds: list[CandidateThreshold],
        number_of_thresholds_to_retain: int,
        check_modularity: bool = False,
        check_conductance: bool = False,
        check_non_degenerate: bool = False,
        check_stability: bool = False,
        keep_e_family: bool = True
) -> list[CandidateThreshold]:
    """
    Filter candidate thresholds using Pareto acceptability and parsimony.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds to filter.
        number_of_thresholds_to_retain : (int)
            Maximum number of thresholds to retain before optionally adding the 'e_family' threshold.
        check_modularity : (bool, optional)
            If True, require acceptable modularity.
            Default is False.
        check_conductance : (bool, optional)
            If True, require acceptable conductance.
            Default is False.
        check_non_degenerate : (bool, optional)
            If True, require an acceptable non-degenerate community structure.
            Default is False.
        check_stability : (bool, optional)
            If True, require acceptable stability.
            Default is False.
        keep_e_family : (bool, optional)
            If True, retain the 'e_family' threshold even when it is not selected by the filtering process.
            Default is True.

    Returns:
        filtered_candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds retained according to Pareto acceptability, parsimony, and the fallback criteria.
    """

    # Check acceptability.
    acceptable_candidate_thresholds = [
        threshold
        for threshold in candidate_thresholds
        if (
                (not check_modularity or threshold.intrinsic_evaluation.acceptable_modularity) and
                (not check_conductance or threshold.intrinsic_evaluation.acceptable_conductance) and
                (not check_non_degenerate or threshold.intrinsic_evaluation.acceptable_non_degenerate) and
                (not check_stability or threshold.stability_evaluation.acceptable_stability)
        )
    ]

    # Filter.
    if acceptable_candidate_thresholds:
        # Parsimony among acceptable candidates.
        acceptable_candidate_thresholds.sort(key=lambda threshold: threshold.value, reverse=True)
        filtered_candidate_thresholds = acceptable_candidate_thresholds[:number_of_thresholds_to_retain]
    else:
        # Fallback: use the evaluation criteria in priority order.
        fallback_candidate_thresholds = candidate_thresholds.copy()
        fallback_candidate_thresholds.sort(
            key=lambda th: (
                not th.intrinsic_evaluation.acceptable_non_degenerate if check_non_degenerate else False,
                -th.intrinsic_evaluation.modularity if check_modularity else 0,
                th.intrinsic_evaluation.conductance if check_conductance else 0,
                -th.stability_evaluation.stability if check_stability else 0,
                -th.value
            )
        )
        filtered_candidate_thresholds = fallback_candidate_thresholds[:number_of_thresholds_to_retain]

    # Keep 'e_family' if required.
    if keep_e_family:
        if CandidateThresholdName.E_FAMILY not in [threshold.name for threshold in filtered_candidate_thresholds]:
            e_family = next(
                (threshold for threshold in candidate_thresholds if threshold.name == CandidateThresholdName.E_FAMILY),
                None
            )

            if e_family is not None:
                filtered_candidate_thresholds.append(e_family)

    return filtered_candidate_thresholds


def select_final_threshold_using_pareto_and_parsimony(
        candidate_thresholds: list[CandidateThreshold]
) -> CandidateThreshold:
    """
    Select the final candidate threshold using Pareto acceptability and parsimony.

    Parameters:
        candidate_thresholds : (list[CandidateThreshold])
            Candidate thresholds from which the final threshold is selected.

    Returns:
        final_threshold : (CandidateThreshold)
            Selected candidate threshold. The largest acceptable threshold is preferred (parsimony principle),
            with the 'e_family' threshold retained when it is acceptable and produces the same
            number of communities as the best candidate.
    """

    acceptable_thresholds = [th for th in candidate_thresholds if th.pareto_plus_parsimony_selection.acceptable]
    if acceptable_thresholds:
        # Parsimony: prefer the largest thresholds of the acceptable thresholds.
        best_candidate = max(acceptable_thresholds, key=lambda th: th.value)
    else:
        # Fallback: use the evaluation criteria in priority order.
        fallback_candidates = sorted(
            candidate_thresholds,
            key=lambda th: (
                not th.intrinsic_evaluation.acceptable_non_degenerate,
                -th.intrinsic_evaluation.modularity,
                th.intrinsic_evaluation.conductance,
                -th.stability_evaluation.stability,
                -th.value
            )
        )

        best_candidate = fallback_candidates[0]

    # Retain 'e_family' if it is practically indistinguishable from the best candidate
    e_family = next(
        (th for th in candidate_thresholds if th.name == CandidateThresholdName.E_FAMILY),
        None
    )

    if (
            e_family is not None
            and e_family.pareto_plus_parsimony_selection.acceptable
            and e_family.intrinsic_evaluation.k_predicted == best_candidate.intrinsic_evaluation.k_predicted
    ):
        return e_family

    return best_candidate
