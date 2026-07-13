from collections import Counter

from experiments.evaluation.community_properties.community_properties_dataclass import CommunityProperties


def compute_community_properties(
        number_of_nodes: int,
        predicted_labels: list,
        overlapping_communities: bool,
        near_singleton_boundary: int
) -> CommunityProperties:
    if overlapping_communities:
        labels = [label for node_labels in predicted_labels for label in node_labels]
    else:
        labels = predicted_labels

    community_sizes = list(Counter(labels).values())
    number_of_communities = len(community_sizes)
    singleton_or_near_singleton_count = sum(1 for size in community_sizes if size <= near_singleton_boundary)

    return CommunityProperties(
        number_of_communities=number_of_communities,
        community_size_distribution=community_sizes,
        singleton_or_near_singleton_count=singleton_or_near_singleton_count,
        singleton_or_near_singleton_fraction=singleton_or_near_singleton_count / number_of_communities,
        largest_community_fraction=max(community_sizes) / number_of_nodes
    )
