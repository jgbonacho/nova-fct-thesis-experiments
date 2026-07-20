from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from experiments.scripts.real_world_networks.thresholds.network_thresholds.extrinsic_evaluation.extrinsic_evaluation_dataclass import \
    ExtrinsicEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.intrinsic_evaluation_dataclass import \
    IntrinsicEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.null_model_evaluation.null_model_evaluation_dataclass import \
    NullModelEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_plus_parsimony_selection_dataclass import \
    ParetoPlusParsimonySelection
from experiments.scripts.real_world_networks.thresholds.network_thresholds.stability_evaluation.stability_evaluation_dataclass import \
    StabilityEvaluation
from experiments.scripts.real_world_networks.utils.csv_dataclass import CsvDataclass


class CandidateThresholdName(str, Enum):
    """
    Enumeration of candidate threshold names.

    Attributes:
        E_FAMILY : (str)
        E_GLOBAL : (str)
        E_BELOW : (str)
        E_ABOVE : (str)
        E_ELBOW : (str)
    """

    E_FAMILY = "e_family"
    E_GLOBAL = "e_global"
    E_BELOW = "e_below"
    E_ABOVE = "e_above"
    E_ELBOW = "e_elbow"


@dataclass
class CandidateThreshold(CsvDataclass):
    """
    Dataclass for a candidate threshold and its evaluation results.

    Attributes:
        family : (str)
            Name of the network family associated with the candidate threshold.
        network : (str)
            Name of the evaluated network.
        name : (CandidateThresholdName)
            Name identifying the candidate threshold.
        value : (float)
            Numerical value of the candidate threshold.
        intrinsic_evaluation : (IntrinsicEvaluation | None)
            Intrinsic evaluation results. None if not yet evaluated.
        stability_evaluation : (StabilityEvaluation | None)
            Perturbation stability evaluation results. None if not yet evaluated.
        null_model_evaluation : (NullModelEvaluation | None)
            Null-model evaluation results. None if not yet evaluated.
        pareto_plus_parsimony_selection : (ParetoPlusParsimonySelection | None)
            Pareto-plus-parsimony selection results. None if not yet evaluated.
        extrinsic_evaluation : (ExtrinsicEvaluation | None)
            Extrinsic evaluation results. None if not applicable or not yet evaluated.
    """

    family: str = field(metadata={"label": "Family"})
    network: str = field(metadata={"label": "Network"})
    name: CandidateThresholdName = field(metadata={"label": "Name"})
    value: float = field(metadata={"label": "Value"})
    intrinsic_evaluation: Optional["IntrinsicEvaluation"] = None
    stability_evaluation: Optional["StabilityEvaluation"] = None
    null_model_evaluation: Optional["NullModelEvaluation"] = None
    pareto_plus_parsimony_selection: Optional["ParetoPlusParsimonySelection"] = None
    extrinsic_evaluation: Optional["ExtrinsicEvaluation"] = None
