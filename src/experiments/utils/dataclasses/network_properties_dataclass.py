from dataclasses import dataclass, field, fields


@dataclass
class NetworkProperties:
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
        return [f.metadata["label"] for f in fields(cls)]

    def to_dict(self) -> dict:
        return {f.metadata["label"]: getattr(self, f.name) for f in fields(self)}
