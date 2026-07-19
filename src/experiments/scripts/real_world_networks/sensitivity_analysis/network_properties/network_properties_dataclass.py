from dataclasses import dataclass, field, fields


@dataclass
class NetworkProperties:
    """
    Dataclass for network properties.

    Attributes:
        network : (str)
            Name of the network.
        nodes_lcc : (int)
            Number of nodes in the largest connected component.
        edges_lcc : (int)
            Number of edges in the largest connected component.
        min_degree : (float)
            Minimum node degree.
        max_degree : (float)
            Maximum node degree.
        average_degree : (float)
            Average node degree.
        degree_std : (float)
            Standard deviation of the node degrees.
        degree_cv : (float)
            Coefficient of variation of the node degrees.
        degree_hub_ratio : (float)
            Ratio between the maximum degree and the average degree.
        degree_assortativity : (float)
            Degree assortativity coefficient of the network.
        density : (float)
            Density of the network.
        sparsity : (float)
            Sparsity of the network, computed as one minus the density.
        global_clustering_coefficient : (float)
            Global clustering coefficient of the network.
        average_clustering : (float)
            Average local clustering coefficient of the network.
        ground_truth : (bool)
            Whether the network has ground-truth community labels.
        overlapping_ground_truth : (bool)
            Whether the ground-truth community structure is overlapping.
    """

    network: str = field(metadata={"label": "Network"})
    nodes_lcc: int = field(metadata={"label": "Nodes LCC"})
    edges_lcc: int = field(metadata={"label": "Edges LCC"})
    min_degree: float = field(metadata={"label": "Min Degree"})
    max_degree: float = field(metadata={"label": "Max Degree"})
    average_degree: float = field(metadata={"label": "Average Degree"})
    degree_std: float = field(metadata={"label": "Degree Std"})
    degree_cv: float = field(metadata={"label": "Degree CV"})
    degree_hub_ratio: float = field(metadata={"label": "Degree Hub Ratio"})
    degree_assortativity: float = field(metadata={"label": "Degree Assortativity"})
    density: float = field(metadata={"label": "Density"})
    sparsity: float = field(metadata={"label": "Sparsity"})
    global_clustering_coefficient: float = field(metadata={"label": "Global Clustering Coefficient"})
    average_clustering: float = field(metadata={"label": "Average Clustering"})

    ground_truth: bool = field(metadata={"label": "Ground-Truth?"})
    overlapping_ground_truth: bool = field(metadata={"label": "Overlapping Ground-Truth?"})

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
        Convert the network properties into a dictionary.

        Returns:
            properties : (dict)
                Dictionary mapping each field label to its corresponding value.
        """

        return {f.metadata["label"]: getattr(self, f.name) for f in fields(self)}
