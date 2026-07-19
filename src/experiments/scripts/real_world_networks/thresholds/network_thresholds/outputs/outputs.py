import csv
import os

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

from experiments.scripts.real_world_networks.thresholds.network_thresholds.network_candidate_thresholds.candidate_threshold_dataclass import \
    CandidateThreshold, CandidateThresholdName
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig

THRESHOLD_PLOT_STYLES = {
    "e_family": {"label": r"$\epsilon_{\mathrm{family}}$", "color": "tab:red", "marker": "o"},
    "e_global": {"label": r"$\epsilon_{\mathrm{global}}$", "color": "tab:grey", "marker": "s"},
    "e_below": {"label": r"$\epsilon_{\mathrm{below}}$", "color": "tab:brown", "marker": "^"},
    "e_above": {"label": r"$\epsilon_{\mathrm{above}}$", "color": "tab:green", "marker": "D"},
    "e_elbow": {"label": r"$\epsilon_{\mathrm{elbow}}$", "color": "tab:purple", "marker": "*"}
}


def generate_final_outputs(
        results_dir: str,
        raw_contributions_filename: str,
        raw_contributions_fieldnames: list,
        candidate_thresholds_filename: str,
        intrinsic_evaluation_filename: str,
        stability_evaluation_filename: str,
        null_model_evaluation_filename: str,
        final_threshold: CandidateThreshold,
        config: RealWorldThresholdEstimationConfig
) -> None:
    """
    Generate the summary CSV and evaluation plots for the selected threshold.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        raw_contributions_filename : (str)
            Name of the CSV file containing the raw contributions.
        raw_contributions_fieldnames : (list)
            Base field names of the raw contributions CSV file.
        candidate_thresholds_filename : (str)
            Name of the candidate thresholds CSV file.
        intrinsic_evaluation_filename : (str)
            Name of the intrinsic evaluation CSV file.
        stability_evaluation_filename : (str)
            Name of the stability evaluation CSV file.
        null_model_evaluation_filename : (str)
            Name of the null-model evaluation CSV file.
        final_threshold : (CandidateThreshold)
            Selected candidate threshold.
        config : (RealWorldThresholdEstimationConfig)
            Configuration of the threshold estimation.

    Returns:
        None
    """

    candidate_thresholds = _load_csv_rows(os.path.join(results_dir, candidate_thresholds_filename))
    intrinsic_results = _load_csv_rows(os.path.join(results_dir, intrinsic_evaluation_filename))
    stability_results = _load_csv_rows(os.path.join(results_dir, stability_evaluation_filename))
    null_model_results = _load_csv_rows(os.path.join(results_dir, null_model_evaluation_filename))

    e_family_candidate = next(
        (row for row in candidate_thresholds if row["Name"] == CandidateThresholdName.E_FAMILY.value),
        None
    )
    e_global_candidate = next(
        (row for row in candidate_thresholds if row["Name"] == CandidateThresholdName.E_GLOBAL.value),
        None
    )

    e_family_intrinsic = next(
        (row for row in intrinsic_results if row["Name"] == CandidateThresholdName.E_FAMILY.value),
        None
    )

    summary = {
        "Family": final_threshold.family,
        "Network": final_threshold.network,
        "e_family": (e_family_candidate["Value"] if e_family_candidate is not None else None),
        "e_global": (e_global_candidate["Value"] if e_global_candidate is not None else None),
        "e* (Name)": final_threshold.name,
        "e*": final_threshold.value,
        "K'(e_family)": (e_family_intrinsic["K'"] if e_family_intrinsic is not None else None),
        "K'(e*)": final_threshold.intrinsic_evaluation.k_predicted,
        "Modularity": final_threshold.intrinsic_evaluation.modularity,
        "Conductance": final_threshold.intrinsic_evaluation.conductance,
        "Singleton/Near-Singleton Fraction": final_threshold.intrinsic_evaluation.singleton_or_near_singleton_fraction,
        "Largest-Community Fraction": final_threshold.intrinsic_evaluation.largest_community_fraction,
        "Runtime": final_threshold.intrinsic_evaluation.runtime,
        "Stability": final_threshold.stability_evaluation.stability,
        "Z Modularity": final_threshold.null_model_evaluation.modularity_z_score,
        "Modularity Empirical p-value": final_threshold.null_model_evaluation.modularity_empirical_p_value,
        "Modularity Rank": final_threshold.null_model_evaluation.modularity_rank,
        "Z Conductance": final_threshold.null_model_evaluation.conductance_z_score,
        "Conductance Empirical p-value": final_threshold.null_model_evaluation.conductance_empirical_p_value,
        "Conductance Rank": final_threshold.null_model_evaluation.conductance_rank,
        "Acceptable Modularity?": final_threshold.intrinsic_evaluation.acceptable_modularity,
        "Acceptable Conductance?": final_threshold.intrinsic_evaluation.acceptable_conductance,
        "Acceptable Non-Degenerate?": final_threshold.intrinsic_evaluation.acceptable_non_degenerate,
        "Acceptable Stability?": final_threshold.stability_evaluation.acceptable_stability,
        "Acceptable Null Model?": final_threshold.null_model_evaluation.acceptable_null_model,
        "Acceptable?": final_threshold.pareto_plus_parsimony_selection.acceptable
    }

    summary_file = os.path.join(results_dir, "_summary.csv")
    with open(file=summary_file, mode="w", newline="", encoding="utf-8") as out_file:
        writer = csv.DictWriter(out_file, fieldnames=list(summary.keys()))
        writer.writeheader()
        writer.writerow(summary)

    _plot_candidate_thresholds(
        results_dir=results_dir,
        raw_contributions_filename=raw_contributions_filename,
        raw_contributions_fieldnames=raw_contributions_fieldnames,
        candidate_thresholds=candidate_thresholds,
        final_threshold=final_threshold
    )

    _plot_k_line_by_threshold(results_dir, intrinsic_results)
    _plot_intrinsic_evaluation(results_dir, intrinsic_results)
    _plot_stability_evaluation(results_dir, stability_results)
    _plot_null_model_z_scores(results_dir, null_model_results)
    _plot_null_model_empirical_p_values(results_dir, null_model_results, config.pareto_null_model_p_value_boundary)
    _plot_null_model_empirical_ranks(results_dir, null_model_results)


def _load_csv_rows(input_file: str) -> list[dict]:
    """
    Load all rows from a CSV file.

    Parameters:
        input_file : (str)
            Path to the input CSV file.

    Returns:
        rows : (list[dict])
            CSV rows represented as dictionaries.
    """

    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
        return list(csv.DictReader(in_file))


def _plot_candidate_thresholds(
        results_dir: str,
        raw_contributions_filename: str,
        raw_contributions_fieldnames: list,
        candidate_thresholds: list[dict],
        final_threshold: CandidateThreshold
) -> None:
    """
    Plot the raw contributions and candidate thresholds.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        raw_contributions_filename : (str)
            Name of the CSV file containing the raw contributions.
        raw_contributions_fieldnames : (list)
            Base field names of the raw contributions CSV file.
        candidate_thresholds : (list[dict])
            Candidate threshold rows loaded from the corresponding CSV file.
        final_threshold : (CandidateThreshold)
            Selected candidate threshold.

    Returns:
        None
    """

    input_file = os.path.join(results_dir, raw_contributions_filename)
    with open(file=input_file, mode="r", newline="", encoding="utf-8") as in_file:
        reader = csv.reader(in_file)
        next(reader, None)
        network = next(reader, None)

    contributions = [float(value) for value in network[len(raw_contributions_fieldnames):] if value != ""]
    extraction_numbers = list(range(1, len(contributions) + 1))

    plt.figure()
    plt.plot(extraction_numbers, contributions, marker="o", markersize=4, linewidth=1.5)
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for candidate in candidate_thresholds:
        if candidate["Value"] in [None, ""]:
            continue

        candidate_name = candidate["Name"]
        candidate_value = float(candidate["Value"])
        style = THRESHOLD_PLOT_STYLES.get(candidate_name, {"label": candidate_name, "color": "black"})

        if candidate_name == final_threshold.name.value:
            plt.axhline(
                final_threshold.value,
                color=style["color"],
                linewidth=2,
                label=f'{style["label"]} = {round(final_threshold.value, 6)}'
            )
        else:
            plt.axhline(
                candidate_value,
                color=style["color"],
                linestyle="--",
                label=f'{style["label"]} = {round(candidate_value, 6)}'
            )

    plt.xlabel("Extraction Number")
    plt.ylabel("Contribution")

    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend(handles=handles, labels=labels, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_candidate_thresholds_plot.pdf"))
    plt.close()


def _plot_k_line_by_threshold(
        results_dir: str,
        intrinsic_results: list[dict]
) -> None:
    """
    Plot the predicted number of communities as a function of the candidate threshold.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        intrinsic_results : (list[dict])
            Intrinsic evaluation results for the candidate thresholds.

    Returns:
        None
    """

    points = sorted(
        [
            (np.log(float(row["Value"])), int(row["K'"]), row["Name"])
            for row in intrinsic_results if row["Value"] not in [None, ""]
        ],
        key=lambda point: point[0]
    )

    if not points:
        return

    log_thresholds = [point[0] for point in points]
    k_values = [point[1] for point in points]

    plt.figure()
    plt.plot(log_thresholds, k_values, linestyle="--")
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for log_threshold, k_value, name in points:
        style = THRESHOLD_PLOT_STYLES.get(name, {"label": name, "color": "black", "marker": "o"})
        plt.plot(
            log_threshold,
            k_value,
            marker=style["marker"],
            color=style["color"],
            linestyle="None",
            markersize=5,
            label=style["label"]
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel(r"$K'(\epsilon)$")

    handles, labels = plt.gca().get_legend_handles_labels()
    if handles:
        plt.legend(handles=handles, labels=labels, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_k_line_by_threshold_plot.pdf"))
    plt.close()


def _plot_intrinsic_evaluation(
        results_dir: str,
        intrinsic_results: list[dict]
) -> None:
    """
    Plot modularity and conductance as functions of the candidate threshold.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        intrinsic_results : (list[dict])
            Intrinsic evaluation results for the candidate thresholds.

    Returns:
        None
    """

    points = sorted(
        [
            (row["Name"], np.log(float(row["Value"])), float(row["Modularity"]), float(row["Conductance"]))
            for row in intrinsic_results if row["Value"] not in [None, ""]
        ],
        key=lambda point: point[1]
    )

    if not points:
        return

    threshold_names = [point[0] for point in points]
    log_thresholds = [point[1] for point in points]
    modularities = [point[2] for point in points]
    conductances = [point[3] for point in points]

    plt.figure()
    plt.plot(log_thresholds, modularities, linestyle="--", color="tab:blue", label="Modularity")
    plt.plot(log_thresholds, conductances, linestyle=":", color="tab:orange", label="Conductance")
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for threshold_name, log_threshold, modularity, conductance in zip(
            threshold_names,
            log_thresholds,
            modularities,
            conductances
    ):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        plt.plot(log_threshold, modularity, marker=style["marker"], color="tab:blue", linestyle="None")
        plt.plot(log_threshold, conductance, marker=style["marker"], color="tab:orange", linestyle="None")

    legend_handles = [
        Line2D([0], [0], color="tab:blue", linestyle="--", label="Modularity"),
        Line2D([0], [0], color="tab:orange", linestyle=":", label="Conductance")
    ]

    for threshold_name in dict.fromkeys(threshold_names):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        legend_handles.append(
            Line2D([0], [0], color="black", marker=style["marker"], linestyle="None", label=style["label"])
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel("Intrinsic Metric")

    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_intrinsic_evaluation_plot.pdf"))
    plt.close()


def _plot_stability_evaluation(
        results_dir: str,
        stability_results: list[dict]
) -> None:
    """
    Plot the stability of each candidate threshold.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        stability_results : (list[dict])
            Stability evaluation results for the candidate thresholds.

    Returns:
        None
    """

    if not stability_results:
        return

    names = [row["Name"] for row in stability_results]
    labels = [THRESHOLD_PLOT_STYLES.get(name, {"label": name})["label"] for name in names]
    colors = [THRESHOLD_PLOT_STYLES.get(name, {"color": "black"})["color"] for name in names]
    stabilities = [float(row["Stability"]) for row in stability_results]

    plt.figure()
    plt.bar(labels, stabilities, color=colors)
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    plt.xlabel(r"$\epsilon$")
    plt.ylabel("Stability")
    plt.tight_layout()

    plt.savefig(os.path.join(results_dir, "_stability_evaluation_plot.pdf"))
    plt.close()


def _plot_null_model_z_scores(
        results_dir: str,
        null_model_results: list[dict]
) -> None:
    """
    Plot the null-model modularity and conductance z-scores.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        null_model_results : (list[dict])
            Null-model evaluation results for the candidate thresholds.

    Returns:
        None
    """

    points = sorted(
        [
            (
                row["Name"],
                np.log(float(row["Value"])),
                float(row["Z Modularity"]),
                float(row["Z Conductance"])
            )
            for row in null_model_results
            if (
                row["Value"] not in [None, ""]
                and row["Z Modularity"] not in [None, ""]
                and row["Z Conductance"] not in [None, ""]
        )
        ],
        key=lambda point: point[1]
    )

    if not points:
        return

    threshold_names = [point[0] for point in points]
    log_thresholds = [point[1] for point in points]
    modularity_z_scores = [point[2] for point in points]
    conductance_z_scores = [point[3] for point in points]

    plt.figure()

    plt.plot(log_thresholds, modularity_z_scores, linestyle="--", color="tab:blue", label="Z Modularity")
    plt.plot(log_thresholds, conductance_z_scores, linestyle=":", color="tab:orange", label="Z Conductance")
    plt.axhline(y=0, color="black", linewidth=1, linestyle="-")
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for threshold_name, log_threshold, modularity_z_score, conductance_z_score in zip(
            threshold_names,
            log_thresholds,
            modularity_z_scores,
            conductance_z_scores
    ):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        plt.plot(log_threshold, modularity_z_score, marker=style["marker"], color="tab:blue", linestyle="None")
        plt.plot(log_threshold, conductance_z_score, marker=style["marker"], color="tab:orange", linestyle="None")

    legend_handles = [
        Line2D([0], [0], color="tab:blue", linestyle="--", label="Z Modularity"),
        Line2D([0], [0], color="tab:orange", linestyle=":", label="Z Conductance")
    ]

    for threshold_name in dict.fromkeys(threshold_names):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        legend_handles.append(
            Line2D([0], [0], color="black", marker=style["marker"], linestyle="None", label=style["label"])
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel("Null-Model Z-Score")

    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_null_model_z_scores_plot.pdf"))
    plt.close()


def _plot_null_model_empirical_p_values(
        results_dir: str,
        null_model_results: list[dict],
        p_value_boundary: float
) -> None:
    """
    Plot the null-model empirical p-values and their acceptability boundary.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        null_model_results : (list[dict])
            Null-model evaluation results for the candidate thresholds.
        p_value_boundary : (float)
            Upper acceptability boundary for the empirical p-values.

    Returns:
        None
    """

    points = sorted(
        [
            (
                row["Name"],
                np.log(float(row["Value"])),
                float(row["Modularity Empirical p-value"]),
                float(row["Conductance Empirical p-value"])
            )
            for row in null_model_results
            if (
                row["Value"] not in [None, ""]
                and row["Modularity Empirical p-value"] not in [None, ""]
                and row["Conductance Empirical p-value"] not in [None, ""]
        )
        ],
        key=lambda point: point[1]
    )

    if not points:
        return

    threshold_names = [point[0] for point in points]
    log_thresholds = [point[1] for point in points]
    modularity_p_values = [point[2] for point in points]
    conductance_p_values = [point[3] for point in points]

    plt.figure()

    plt.plot(log_thresholds, modularity_p_values, linestyle="--", color="tab:blue")
    plt.plot(log_thresholds, conductance_p_values, linestyle=":", color="tab:orange")

    plt.axhline(y=p_value_boundary, color="black", linestyle="-.", linewidth=1)
    plt.grid(axis="both", linestyle=":", alpha=0.5)

    for threshold_name, log_threshold, modularity_p_value, conductance_p_value in zip(
            threshold_names,
            log_thresholds,
            modularity_p_values,
            conductance_p_values
    ):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        plt.plot(log_threshold, modularity_p_value, marker=style["marker"], color="tab:blue", linestyle="None")
        plt.plot(log_threshold, conductance_p_value, marker=style["marker"], color="tab:orange", linestyle="None")

    legend_handles = [
        Line2D([0], [0], color="tab:blue", linestyle="--", label="Modularity empirical p-value"),
        Line2D([0], [0], color="tab:orange", linestyle=":", label="Conductance empirical p-value"),
        Line2D([0], [0], color="black", linestyle="-.", label=f"Boundary = {p_value_boundary:g}")
    ]

    for threshold_name in dict.fromkeys(threshold_names):
        style = THRESHOLD_PLOT_STYLES.get(threshold_name, {"label": threshold_name, "marker": "o"})

        legend_handles.append(
            Line2D([0], [0], color="black", marker=style["marker"], linestyle="None", label=style["label"])
        )

    plt.xlabel(r"$\log(\epsilon)$")
    plt.ylabel("Empirical p-value")
    plt.ylim(0.0, 1.0)
    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_null_model_empirical_p_values_plot.pdf"))
    plt.close()


def _plot_null_model_empirical_ranks(
        results_dir: str,
        null_model_results: list[dict]
) -> None:
    """
    Plot the null-model empirical modularity and conductance ranks.

    Parameters:
        results_dir : (str)
            Path to the network results directory.
        null_model_results : (list[dict])
            Null-model evaluation results for the candidate thresholds.

    Returns:
        None
    """

    valid_results = [
        row
        for row in null_model_results
        if (
                row["Modularity Rank"] not in [None, ""]
                and row["Conductance Rank"] not in [None, ""]
        )
    ]

    if not valid_results:
        return

    names = [row["Name"] for row in valid_results]
    labels = [THRESHOLD_PLOT_STYLES.get(name, {"label": name})["label"] for name in names]
    colors = [THRESHOLD_PLOT_STYLES.get(name, {"color": "black"})["color"] for name in names]

    modularity_ranks = [int(row["Modularity Rank"]) for row in valid_results]
    conductance_ranks = [int(row["Conductance Rank"]) for row in valid_results]

    x = np.arange(len(labels))
    width = 0.35

    plt.figure()
    plt.bar(x - width / 2, modularity_ranks, width, color=colors, edgecolor="black", hatch="//")
    plt.bar(x + width / 2, conductance_ranks, width, color=colors, edgecolor="black", hatch="\\")

    legend_handles = [
        Patch(facecolor="white", edgecolor="black", hatch="//", label="Modularity rank"),
        Patch(facecolor="white", edgecolor="black", hatch="\\", label="Conductance rank")
    ]

    for name in dict.fromkeys(names):
        style = THRESHOLD_PLOT_STYLES.get(name, {"label": name, "color": "black"})

        legend_handles.append(
            Patch(facecolor=style["color"], label=style["label"])
        )

    plt.xticks(x, labels)
    plt.ylabel("Empirical Rank")
    plt.xlabel(r"$\epsilon$")
    plt.yticks(np.arange(0, max(modularity_ranks + conductance_ranks) + 1, 1))

    plt.grid(axis="y", linestyle=":", alpha=0.5)
    plt.legend(handles=legend_handles, fontsize=8)

    plt.tight_layout()
    plt.savefig(os.path.join(results_dir, "_null_model_empirical_ranks_plot.pdf"))
    plt.close()
