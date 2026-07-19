from dataclasses import dataclass, field


@dataclass
class RealWorldThresholdEstimationConfig:
    """
    Dataclass for the real-world threshold estimation configuration.

    Attributes:
        apply_lapin : (bool)
            Whether to apply the LAPIN transformation before running FADDIS.
            Default is True.
        tau : (float)
            Minimum cluster intensity used by the FADDIS stopping criterion.
            Default is 0.05.
        k_max_boundary : (int)
            Upper boundary for the maximum number of clusters extracted by FADDIS.
            Default is 500.
        overlapping_communities : (bool)
            Whether the predicted community structures are overlapping.
            Default is False.
        defuzzification_gamma : (float)
            Hyperparameter used by the defuzzification rule for overlapping communities.
            Default is 0.8.
        number_of_thresholds_to_retain_after_intrinsic_evaluation : (int)
            Maximum number of candidate thresholds retained after the intrinsic evaluation.
            Default is 3.
        number_of_thresholds_to_retain_after_stability_evaluation : (int)
            Maximum number of candidate thresholds retained after the stability evaluation.
            Default is 2.
        near_singleton_boundary : (int)
            Maximum community size for a community to be considered a singleton or near-singleton.
            Default is 2.
        number_of_perturbed_graphs : (int)
            Number of perturbed graphs generated for the stability evaluation.
            Default is 10.
        fraction_of_edges_swaps_in_perturbed_graphs : (float)
            Fraction of network edges used to determine the number of edge swaps in each perturbed graph.
            Default is 0.05.
        number_of_null_models : (int)
            Number of null-model graphs generated for the null-model evaluation.
            Default is 10.
        fraction_of_edges_swaps_in_null_models : (float)
            Fraction of network edges used to determine the number of edge swaps in each null-model graph.
            Default is 10.
        pareto_tolerance_fraction_modularity : (float)
            Tolerance fraction applied to the modularity range in the Pareto acceptability criterion.
            Default is 0.10.
        pareto_tolerance_fraction_conductance : (float)
            Tolerance fraction applied to the conductance range in the Pareto acceptability criterion.
            Default is 0.10.
        pareto_tolerance_fraction_stability : (float)
            Tolerance fraction applied to the stability range in the Pareto acceptability criterion.
            Default is 0.15.
        pareto_largest_community_fraction_boundary : (float)
            Upper boundary for the fraction of nodes assigned to the largest community.
            Default is 0.95.
        pareto_singleton_or_near_singleton_fraction_boundary : (float)
            Upper boundary for the fraction of singleton or near-singleton communities.
            Default is 0.5.
        pareto_null_model_p_value_boundary : (float)
            Upper boundary for empirical p-values in the null-model acceptability criterion.
            Default is 0.10.
        pareto_null_model_rank_boundary : (int)
            Upper boundary for empirical ranks in the null-model acceptability criterion.
            Default is 2.
        pareto_null_model_z_score_boundary : (float)
            Lower boundary for z-scores in the null-model acceptability criterion.
            Default is 1.645.
    """

    apply_lapin: bool = field(default=True)
    tau: float = field(default=0.05)
    k_max_boundary: int = field(default=500)
    overlapping_communities: bool = field(default=False)
    defuzzification_gamma: float = field(default=0.8)
    number_of_thresholds_to_retain_after_intrinsic_evaluation: int = field(default=3)
    number_of_thresholds_to_retain_after_stability_evaluation: int = field(default=2)
    near_singleton_boundary: int = field(default=2)
    number_of_perturbed_graphs: int = field(default=10)
    fraction_of_edges_swaps_in_perturbed_graphs: float = field(default=0.05)
    number_of_null_models: int = field(default=10)
    fraction_of_edges_swaps_in_null_models: float = field(default=10)
    pareto_tolerance_fraction_modularity: float = field(default=0.10)
    pareto_tolerance_fraction_conductance: float = field(default=0.10)
    pareto_tolerance_fraction_stability: float = field(default=0.15)
    pareto_largest_community_fraction_boundary: float = field(default=0.95)
    pareto_singleton_or_near_singleton_fraction_boundary: float = field(default=0.5)
    pareto_null_model_p_value_boundary: float = field(default=0.10)
    pareto_null_model_rank_boundary: int = field(default=2)
    pareto_null_model_z_score_boundary: float = field(default=1.645)

    def compute_k_max(self, number_of_nodes: int):
        return min(self.k_max_boundary, int(number_of_nodes / 2))

    def compute_number_of_edges_swaps_in_perturbed_graphs(self, number_of_edges: int):
        return int(number_of_edges * self.fraction_of_edges_swaps_in_perturbed_graphs)

    def compute_number_of_edges_swaps_in_null_models(self, number_of_edges: int):
        return int(number_of_edges * self.fraction_of_edges_swaps_in_null_models)
