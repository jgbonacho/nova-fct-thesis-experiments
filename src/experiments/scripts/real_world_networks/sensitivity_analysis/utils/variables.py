from experiments.scripts.real_world_networks.utils.ground_truth_properties.ground_truth_properties_dataclass import \
    GroundTruthProperties
from experiments.scripts.real_world_networks.utils.network_properties.network_properties_dataclass import \
    NetworkProperties

RAW_CONTRIBUTIONS_FILENAME = "raw_contributions.csv"
RAW_CONTRIBUTIONS_FIELDNAMES = [
    "Network", "K", "Stop Condition"
]
NETWORK_PROPERTIES_FILENAME = "network_properties.csv"
NETWORK_PROPERTIES_FIELDNAMES = NetworkProperties.headers()
GROUND_TRUTH_PROPERTIES_FILENAME = "ground_truth_properties.csv"
GROUND_TRUTH_PROPERTIES_FIELDNAMES = GroundTruthProperties.headers()
FADDIS_SENSITIVITY_ANALYSIS_FILENAME = "faddis_sensitivity_analysis.csv"
FADDIS_SENSITIVITY_ANALYSIS_FIELDNAMES = [
    "Ground-Truth Type",
    "Network Property",
    "FADDIS Property",
    "#Networks",
    "Spearman Correlation",
    "Spearman 95% CI Lower",
    "Spearman 95% CI Upper",
    "Pearson Correlation",
    "Pearson 95% CI Lower",
    "Pearson 95% CI Upper"
]
REPORT_FILENAME = "report.json"
