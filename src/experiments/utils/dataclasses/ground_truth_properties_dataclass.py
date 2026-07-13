from dataclasses import dataclass, field, fields


@dataclass
class GroundTruthProperties:
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
        return [f.metadata["label"] for f in fields(cls)]

    def to_dict(self) -> dict:
        return {f.metadata["label"]: getattr(self, f.name) for f in fields(self)}
