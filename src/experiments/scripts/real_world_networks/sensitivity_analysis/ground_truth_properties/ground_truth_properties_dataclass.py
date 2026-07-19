from dataclasses import dataclass, field, fields


@dataclass
class GroundTruthProperties:
    """
    Dataclass for ground-truth community properties.

    Attributes:
        network : (str)
            Name of the network.
        overlapping_ground_truth : (bool)
            Whether the ground-truth community structure is overlapping.
        overlap_fraction : (float)
            Fraction of labeled nodes that belong to more than one ground-truth community.
        k : (int)
            Number of ground-truth communities.
        community_proportion : (float)
            Ratio between the number of ground-truth communities and the number of nodes.
        min_community_size : (float)
            Size of the smallest ground-truth community.
        max_community_size : (float)
            Size of the largest ground-truth community.
        average_community_size : (float)
            Average size of the ground-truth communities.
        community_size_std : (float)
            Standard deviation of the ground-truth community sizes.
        community_size_cv : (float)
            Coefficient of variation of the ground-truth community sizes.
        nodes_without_community : (int)
            Number of nodes without a ground-truth community assignment.
        nodes_fraction_without_community : (float)
            Fraction of nodes without a ground-truth community assignment.
    """

    network: str = field(metadata={"label": "Network"})
    overlapping_ground_truth: bool = field(metadata={"label": "Overlapping Ground-Truth?"})
    overlap_fraction: float = field(metadata={"label": "Overlap Fraction"})
    k: int = field(metadata={"label": "K"})
    community_proportion: float = field(metadata={"label": "Community Proportion"})
    min_community_size: float = field(metadata={"label": "Min Community Size"})
    max_community_size: float = field(metadata={"label": "Max Community Size"})
    average_community_size: float = field(metadata={"label": "Average Community Size"})
    community_size_std: float = field(metadata={"label": "Community Size Std"})
    community_size_cv: float = field(metadata={"label": "Community Size CV"})
    nodes_without_community: int = field(metadata={"label": "Nodes Without Community"})
    nodes_fraction_without_community: float = field(metadata={"label": "Nodes Fraction Without Community"})

    @classmethod
    def headers(cls) -> list[str]:
        """
        Return the CSV headers defined in the dataclass field metadata.

        Returns:
            headers : (list[str])
                Labels associated with the dataclass fields.
        """

        return [f.metadata["label"] for f in fields(cls)]

    def to_dict(self) -> dict:
        """
        Convert the ground-truth properties into a dictionary.

        Returns:
            properties : (dict)
                Dictionary mapping each field label to its corresponding value.
        """

        return {f.metadata["label"]: getattr(self, f.name) for f in fields(self)}
