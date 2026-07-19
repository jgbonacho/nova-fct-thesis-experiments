from experiments.scripts.real_world_networks.thresholds.network_thresholds.intrinsic_evaluation.intrinsic_evaluation_dataclass import \
    IntrinsicEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold
from experiments.scripts.real_world_networks.thresholds.network_thresholds.null_model_evaluation.null_model_evaluation_dataclass import \
    NullModelEvaluation
from experiments.scripts.real_world_networks.thresholds.network_thresholds.pareto_filtering_and_parsimony_selection.pareto_plus_parsimony_selection_dataclass import \
    ParetoPlusParsimonySelection
from experiments.scripts.real_world_networks.thresholds.network_thresholds.stability_evaluation.stability_evaluation_dataclass import \
    StabilityEvaluation

RAW_CONTRIBUTIONS_FILENAME = "01_raw_contributions.csv"
RAW_CONTRIBUTIONS_FILENAMES = [
    "Network", "K", "Stop Condition"
]
K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAME = "k_boundary_thresholds_by_network.csv"
K_BOUNDARY_THRESHOLDS_BY_NETWORK_FILENAMES = [
    "Network", "#Contributions", "K", "c_K", "c_K+1", "Valid Threshold?", "Threshold"
]
K_BOUNDARY_THRESHOLDS_BY_FAMILY_FILENAME = "k_boundary_thresholds_by_family.csv"
K_BOUNDARY_THRESHOLDS_BY_FAMIL_FIELDNAMES = [
    "Network Family", "#Networks", "#Valid Thresholds", "Valid Thresholds", "e_family", "e_global"
]
CANDIDATE_THRESHOLDS_FILENAME = "02_candidate_thresholds.csv"
CANDIDATE_THRESHOLDS_FIELDNAMES = (
    CandidateThreshold.fieldnames()
)
INTRINSIC_EVALUATION_FILENAME = "03_intrinsic_evaluation.csv"
INTRINSIC_EVALUATION_FIELDNAMES = (
        CandidateThreshold.fieldnames()
        + IntrinsicEvaluation.fieldnames()
)
STABILITY_EVALUATION_FILENAME = "04_stability_evaluation.csv"
STABILITY_EVALUATION_FIELDNAMES = (
        CandidateThreshold.fieldnames()
        + IntrinsicEvaluation.fieldnames()
        + StabilityEvaluation.fieldnames()
)
NULL_MODEL_EVALUATION_FILENAME = "05_null_model_evaluation.csv"
NULL_MODEL_EVALUATION_FIELDNAMES = (
        CandidateThreshold.fieldnames()
        + IntrinsicEvaluation.fieldnames()
        + StabilityEvaluation.fieldnames()
        + NullModelEvaluation.fieldnames()
)
FINAL_THRESHOLDS_FILENAME = "06_final_thresholds_evaluation.csv"
THRESHOLD_FILENAME = "07_threshold.csv"
FINAL_THRESHOLDS_FIELDNAMES = (
        CandidateThreshold.fieldnames()
        + IntrinsicEvaluation.fieldnames()
        + StabilityEvaluation.fieldnames()
        + NullModelEvaluation.fieldnames()
        + ParetoPlusParsimonySelection.fieldnames()
)
EXTRINSIC_EVALUATION_FILENAME = "08_extrinsic_evaluation.csv"
REPORT_FILENAME = "report.json"
