import networkx as nx
import numpy as np

from experiments.scripts.real_world_networks.utils.network_properties.network_properties_dataclass import \
    NetworkProperties


def compute_network_properties(
        network_name: str,
        graph: nx.Graph,
        ground_truth: bool,
        overlapping_ground_truth: bool
) -> NetworkProperties:
    """
    Compute the structural properties of a network.

    Parameters:
        network_name : (str)
            Name of the network.
        graph : (nx.Graph)
            Network whose structural properties are computed.
        ground_truth : (bool)
            Whether the network has ground-truth community labels.
        overlapping_ground_truth : (bool)
            Whether the ground-truth community structure is overlapping.

    Returns:
        network_properties : (NetworkProperties)
            Structural properties of the network.
    """

    nodes = graph.number_of_nodes()
    edges = graph.number_of_edges()
    degrees = np.asarray([degree for _, degree in graph.degree()], dtype=np.float64)
    min_degree = float(np.min(degrees)) if nodes > 0 else None
    max_degree = float(np.max(degrees)) if nodes > 0 else None
    average_degree = float(np.mean(degrees)) if nodes > 0 else None
    degree_std = float(np.std(degrees, ddof=1)) if nodes > 1 else 0.0
    degree_cv = (degree_std / average_degree if average_degree is not None and average_degree > 0 else None)
    degree_hub_ratio = (
        max_degree / average_degree
        if max_degree is not None and average_degree is not None and average_degree > 0
        else None
    )
    degree_assortativity = float(nx.degree_assortativity_coefficient(graph)) if nodes > 0 else None
    density = nx.density(graph) if nodes > 1 else 0.0
    sparsity = 1.0 - density
    global_clustering_coefficient = nx.transitivity(graph) if nodes > 0 else None
    average_clustering = nx.average_clustering(graph) if nodes > 0 else None

    return NetworkProperties(
        network=network_name,
        nodes_lcc=nodes,
        edges_lcc=edges,
        min_degree=min_degree,
        max_degree=max_degree,
        average_degree=average_degree,
        degree_std=degree_std,
        degree_cv=degree_cv,
        degree_hub_ratio=degree_hub_ratio,
        degree_assortativity=degree_assortativity,
        density=density,
        sparsity=sparsity,
        global_clustering_coefficient=global_clustering_coefficient,
        average_clustering=average_clustering,
        ground_truth=ground_truth,
        overlapping_ground_truth=overlapping_ground_truth
    )
