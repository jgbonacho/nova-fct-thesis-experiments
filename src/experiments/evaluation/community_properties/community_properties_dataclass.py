from dataclasses import dataclass, field


@dataclass
class CommunityProperties:
    number_of_communities: int = field(metadata={"label": "K'"})
    community_size_distribution: list[int] = field(metadata={"label": "Community Size Distribution"})
    singleton_or_near_singleton_count: int = field(metadata={"label": "#Singleton/Near-Singleton Communities"})
    singleton_or_near_singleton_fraction: float = field(metadata={"label": "Singleton/Near-Singleton Fraction"})
    largest_community_fraction: float = field(metadata={"label": "Largest-Community Fraction"})
