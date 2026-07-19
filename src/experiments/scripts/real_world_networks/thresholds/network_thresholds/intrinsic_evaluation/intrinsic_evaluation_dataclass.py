from dataclasses import field, dataclass

from experiments.scripts.real_world_networks.thresholds.utils.csv_dataclass import CsvDataclass


@dataclass
class IntrinsicEvaluation(CsvDataclass):
    """
    Dataclass for intrinsic evaluation results.

    Attributes:
        k_predicted : (int)
            Number of predicted communities.
        overlapping_communities : (bool)
            Whether the predicted community structure is overlapping.
        community_size_distribution : (list)
            List containing the number of nodes assigned to each predicted community.
        singleton_or_near_singleton_communities : (int)
            Number of predicted communities classified as singletons or near-singletons.
        singleton_or_near_singleton_fraction : (float)
            Fraction of predicted communities classified as singletons or near-singletons.
        largest_community_fraction : (float)
            Fraction of network nodes assigned to the largest predicted community.
        modularity : (float)
            Modularity or fuzzy modularity of the predicted community structure.
        conductance : (float)
            Conductance or boundary-node conductance of the predicted community structure.
        runtime : (float)
            Runtime of the community extraction and evaluation.
        acceptable_modularity : (bool | None)
            Whether the modularity satisfies the acceptability criterion.
            None if not yet evaluated.
        acceptable_conductance : (bool | None)
            Whether the conductance satisfies the acceptability criterion.
            None if not yet evaluated.
        acceptable_non_degenerate : (bool | None)
            Whether the predicted community structure satisfies the non-degeneracy criteria.
            None if not yet evaluated.
    """

    k_predicted: int = field(metadata={"label": "K'"})
    overlapping_communities: bool = field(metadata={"label": "Overlapping Communities"})
    community_size_distribution: list = field(metadata={"label": "Community Size Distribution"})
    singleton_or_near_singleton_communities: int = field(metadata={"label": "#Singleton/Near-Singleton Communities"})
    singleton_or_near_singleton_fraction: float = field(metadata={"label": "Singleton/Near-Singleton Fraction"})
    largest_community_fraction: float = field(metadata={"label": "Largest-Community Fraction"})
    modularity: float = field(metadata={"label": "Modularity"})
    conductance: float = field(metadata={"label": "Conductance"})
    runtime: float = field(metadata={"label": "Runtime"})
    acceptable_modularity: bool = field(metadata={"label": "Acceptable Modularity?"}, default=None)
    acceptable_conductance: bool = field(metadata={"label": "Acceptable Conductance?"}, default=None)
    acceptable_non_degenerate: bool = field(metadata={"label": "Acceptable Non-Degenerate?"}, default=None)
