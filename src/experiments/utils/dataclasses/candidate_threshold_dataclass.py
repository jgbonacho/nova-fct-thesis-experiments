from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from experiments.utils.dataclasses.csv_dataclass import CsvDataclass


class CandidateThresholdName(str, Enum):
    E_FAMILY = "e_family"
    E_GLOBAL = "e_global"
    E_BELOW = "e_below"
    E_ABOVE = "e_above"
    E_ELBOW = "e_elbow"


@dataclass
class IntrinsicEvaluation(CsvDataclass):
    k_predicted: int = field(metadata={"label": "K'"})
    overlapping_communities: bool = field(metadata={"label": "Overlapping Communities"})
    community_size_distribution: list = field(metadata={"label": "Community Size Distribution"})
    singleton_or_near_singleton_communities: int = field(metadata={"label": "#Singleton/Near-Singleton Communities"})
    singleton_or_near_singleton_fraction: float = field(metadata={"label": "Singleton/Near-Singleton Fraction"})
    largest_community_fraction: float = field(metadata={"label": "Largest-Community Fraction"})
    modularity: float = field(metadata={"label": "Modularity"})
    conductance: float = field(metadata={"label": "Conductance"})
    runtime: float = field(metadata={"label": "Runtime"})


@dataclass
class StabilityEvaluation(CsvDataclass):
    number_of_perturbed_graphs: int = field(metadata={"label": "#Perturbed Graphs"})
    number_of_valid_similarities: int = field(metadata={"label": "#Valid Similarities"})
    similarities: list[float] = field(metadata={"label": "Similarities"})
    stability: float = field(metadata={"label": "Stability"})


@dataclass
class NullModelEvaluation(CsvDataclass):
    number_of_null_graphs: int = field(metadata={"label": "#Null Graphs"})
    number_of_valid_results: int = field(metadata={"label": "#Valid Null Modularities and Conductances"})

    null_modularities: list[float] = field(metadata={"label": "Null Modularities"})
    mean_null_modularity: float = field(metadata={"label": "Mean Null Modularity"})
    std_null_modularity: float = field(metadata={"label": "Std Null Modularity"})
    modularity_z_score: float = field(metadata={"label": "Z Modularity"})
    modularity_empirical_p_value: float = field(metadata={"label": "Modularity Empirical p-value"})
    modularity_rank: int = field(metadata={"label": "Modularity Rank"})

    null_conductances: list[float] = field(metadata={"label": "Null Conductances"})
    mean_null_conductance: float = field(metadata={"label": "Mean Null Conductance"})
    std_null_conductance: float = field(metadata={"label": "Std Null Conductance"})
    conductance_z_score: float = field(metadata={"label": "Z Conductance"})
    conductance_empirical_p_value: float = field(metadata={"label": "Conductance Empirical p-value"})
    conductance_rank: int = field(metadata={"label": "Conductance Rank"})


@dataclass
class ParetoPlusParsimonySelection(CsvDataclass):
    acceptable_modularity: bool = field(metadata={"label": "Acceptable Modularity?"})
    acceptable_conductance: bool = field(metadata={"label": "Acceptable Conductance?"})
    acceptable_stability: bool = field(metadata={"label": "Acceptable Stability?"})
    non_degenerate: bool = field(metadata={"label": "Non-Degenerate?"})
    acceptable_null_model: bool = field(metadata={"label": "Acceptable Null Model?"})
    acceptable: bool = field(metadata={"label": "Acceptable?"})


@dataclass
class ExtrinsicEvaluation(CsvDataclass):
    diff_of_k: str = field(metadata={"label": "K' | K"})
    relative_error_of_k: float = field(metadata={"label": "|K'-K|/K"})

    ami: float = field(default=None, metadata={"label": "AMI"})
    f_measure: float = field(default=None, metadata={"label": "F-measure"})
    ari: float = field(default=None, metadata={"label": "ARI"})
    fmi: float = field(default=None, metadata={"label": "FMI"})
    nmi: float = field(default=None, metadata={"label": "NMI"})
    vi: float = field(default=None, metadata={"label": "VI"})

    onmi: float = field(default=None, metadata={"label": "ONMI"})
    omega: float = field(default=None, metadata={"label": "Omega"})


@dataclass
class CandidateThreshold(CsvDataclass):
    family: str = field(metadata={"label": "Family"})
    network: str = field(metadata={"label": "Network"})

    name: CandidateThresholdName = field(metadata={"label": "Name"})
    value: float = field(metadata={"label": "Value"})

    intrinsic_evaluation: Optional["IntrinsicEvaluation"] = None
    stability_evaluation: Optional["StabilityEvaluation"] = None
    null_model_evaluation: Optional["NullModelEvaluation"] = None
    pareto_plus_parsimony_selection: Optional["ParetoPlusParsimonySelection"] = None
    extrinsic_evaluation: Optional["ExtrinsicEvaluation"] = None
