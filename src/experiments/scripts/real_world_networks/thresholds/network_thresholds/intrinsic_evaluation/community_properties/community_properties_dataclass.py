from dataclasses import dataclass, field


@dataclass
class CommunityProperties:
    """
    Dataclass for community properties.

    Attributes:
        number_of_communities : (int)
            Number of predicted communities.
        community_size_distribution : (list[int])
            List containing the number of nodes assigned to each predicted community.
        singleton_or_near_singleton_count : (int)
            Number of predicted communities whose size is less than or equal to the near-singleton boundary.
        singleton_or_near_singleton_fraction : (float)
            Fraction of predicted communities classified as singletons or near-singletons.
        largest_community_fraction : (float)
            Fraction of network nodes assigned to the largest predicted community.
    """

    number_of_communities: int = field(metadata={"label": "K'"})
    community_size_distribution: list[int] = field(metadata={"label": "Community Size Distribution"})
    singleton_or_near_singleton_count: int = field(metadata={"label": "#Singleton/Near-Singleton Communities"})
    singleton_or_near_singleton_fraction: float = field(metadata={"label": "Singleton/Near-Singleton Fraction"})
    largest_community_fraction: float = field(metadata={"label": "Largest-Community Fraction"})
