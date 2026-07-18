from dataclasses import dataclass, field


@dataclass
class RealWorldThresholdEstimationConfig:
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

    pareto_tolerance_fraction_stability: float = field(default=0.10)

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
