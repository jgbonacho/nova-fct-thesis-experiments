import numpy as np

from experiments.scripts.real_world_networks.utils.ground_truth_properties.ground_truth_properties_dataclass import \
    GroundTruthProperties


def compute_ground_truth_properties(
        network_name: str,
        ground_truth_labels: list,
        k: int,
        overlapping_ground_truth: bool,
        number_of_nodes: int
) -> GroundTruthProperties:
    """
    Compute the properties of a ground-truth community structure.

    Parameters:
        network_name : (str)
            Name of the network.
        ground_truth_labels : (list | None)
            Ground-truth community labels for each node.
        k : (int)
            Number of ground-truth communities.
        overlapping_ground_truth : (bool)
            Whether the ground-truth community structure is overlapping.
        number_of_nodes : (int)
            Number of nodes in the network.

    Returns:
        ground_truth_properties : (GroundTruthProperties | None)
            Properties of the ground-truth community structure. None if no ground-truth labels
            are provided.
    """

    if ground_truth_labels is None:
        return None

    community_sizes = {}
    nodes_without_community = 0
    overlapping_nodes = 0
    labeled_nodes = 0

    if not overlapping_ground_truth:
        for label in ground_truth_labels:
            if label == -1:
                nodes_without_community += 1
                continue

            labeled_nodes += 1
            community_sizes[label] = community_sizes.get(label, 0) + 1

        overlap_fraction = 0.0
    else:
        for labels in ground_truth_labels:
            if labels == [-1] or len(labels) == 0:
                nodes_without_community += 1
                continue

            valid_labels = [label for label in labels if label != -1]

            if len(valid_labels) == 0:
                nodes_without_community += 1
                continue

            labeled_nodes += 1

            if len(valid_labels) > 1:
                overlapping_nodes += 1

            for label in valid_labels:
                community_sizes[label] = community_sizes.get(label, 0) + 1

        overlap_fraction = overlapping_nodes / labeled_nodes if labeled_nodes > 0 else None

    sizes = np.asarray(list(community_sizes.values()), dtype=np.float64)

    if len(sizes) == 0:
        min_community_size = None
        max_community_size = None
        average_community_size = None
        community_size_std = None
        community_size_cv = None
    else:
        min_community_size = float(np.min(sizes))
        max_community_size = float(np.max(sizes))
        average_community_size = float(np.mean(sizes))
        community_size_std = float(np.std(sizes, ddof=1)) if len(sizes) > 1 else 0.0
        community_size_cv = community_size_std / average_community_size if average_community_size > 0 else None

    nodes_fraction_without_community = nodes_without_community / number_of_nodes

    return GroundTruthProperties(
        network=network_name,
        overlapping_ground_truth=overlapping_ground_truth,
        overlap_fraction=overlap_fraction,
        k=k,
        community_proportion=k / number_of_nodes,
        min_community_size=min_community_size,
        max_community_size=max_community_size,
        average_community_size=average_community_size,
        community_size_std=community_size_std,
        community_size_cv=community_size_cv,
        nodes_without_community=nodes_without_community,
        nodes_fraction_without_community=nodes_fraction_without_community
    )
