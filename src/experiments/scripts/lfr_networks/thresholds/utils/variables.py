RAW_CONTRIBUTIONS_FILENAME = "raw_contributions.csv"
RAW_CONTRIBUTIONS_FIELDNAMES = [
    "Network", "K"
]
NORMALIZED_CONTRIBUTIONS_FILENAME = "normalized_contributions.csv"
NORMALIZED_CONTRIBUTIONS_FIELDNAMES = [
    "Network", "K"
]
STATISTICS_FILENAME = "statistics.csv"
STATISTICS_FIELDNAMES = [
    "Network Family", "#Networks", "Mean", "Std", "Median", "75%", "90%", "95%", "Min", "Max"
]
HISTOGRAM_FILENAME = "histogram.pdf"
BOXPLOT_FILENAME = "boxplot.pdf"
LINE_PLOT_FILENAME = "line_plot.pdf"
CANDIDATE_THRESHOLDS_FILENAME = "candidate_thresholds.csv"
CANDIDATE_THRESHOLDS_FIELDNAMES = [
    "Network Family", "Mean", "Median", "75%", "90%", "95%"
]
BOOTSTRAP_STATISTICS_FILENAME = "bootstrap_statistics.csv"
BOOTSTRAP_STATISTICS_FIELDNAMES = [
    "Network Family", "#Networks", "Subsample Size", "#Bootstraps", "Metric", "Candidate Threshold", "MSE"
]
SELECTED_THRESHOLDS_FILENAME = "thresholds.csv"
SELECTED_THRESHOLDS_FIELDNAMES = [
    "Network Family", "Selected Metric", "Threshold"
]
REPORT_FILENAME = "report.json"
