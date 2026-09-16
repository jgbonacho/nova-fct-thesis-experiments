import csv
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

BOOTSTRAP_SAMPLES = 10000
CONFIDENCE_LEVEL = 0.95
RANDOM_SEED = 42


def perform_faddis_sensitivity_analysis(
        results_dir: str,
        network_properties_input_filename: str,
        network_properties_input_fieldnames: list,
        raw_contributions_input_filename: str,
        raw_contributions_input_fieldnames: list,
        output_filename: str,
        output_fieldnames: list,
        apply_lapin: bool
) -> None:
    """
    Perform the FADDIS sensitivity analysis between network properties and valid
    contributions at K.

    The analysis is performed separately for non-overlapping networks,
    overlapping networks, and both ground-truth types combined. In addition to
    Pearson and Spearman correlation coefficients, bootstrap confidence
    intervals, scatter plots, and a leave-one-network-out influence analysis
    are produced.

    Parameters:
        results_dir : (str)
            Path to the results directory.
        network_properties_input_filename : (str)
            Name of the input CSV file containing the network properties.
        network_properties_input_fieldnames : (list)
            Field names of the network properties CSV file.
        raw_contributions_input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        raw_contributions_input_fieldnames : (list)
            Base field names of the raw contributions CSV file.
        output_filename : (str)
            Name of the output CSV file.
        output_fieldnames : (list)
            Field names of the output CSV file.
        apply_lapin : (bool)
            Whether LAPIN was applied before running FADDIS.

    Returns:
        None
    """

    network_properties = _load_network_properties(
        os.path.join(results_dir, network_properties_input_filename)
    )

    contributions_at_k = _load_valid_contributions_at_k(
        results_dir,
        raw_contributions_input_filename,
        raw_contributions_input_fieldnames,
        apply_lapin
    )

    ground_truth_groups = [
        (
            "Non-overlapping and Overlapping",
            network_properties
        ),
        (
            "Non-overlapping",
            {
                network_name: properties
                for network_name, properties in network_properties.items()
                if str(properties.get("Overlapping Ground-Truth?")).lower() == "false"
            }
        ),
        (
            "Overlapping",
            {
                network_name: properties
                for network_name, properties in network_properties.items()
                if str(properties.get("Overlapping Ground-Truth?")).lower() == "true"
            }
        )
    ]

    excluded_columns = {
        "Network",
        "Ground-Truth?",
        "Overlapping Ground-Truth?"
    }

    plots_dir = os.path.join(results_dir, "plots")
    os.makedirs(plots_dir, exist_ok=True)

    output_rows = []

    for ground_truth_type, group_network_properties in ground_truth_groups:

        group_plots_dir = os.path.join(
            plots_dir,
            _safe_filename(ground_truth_type).lower()
        )
        os.makedirs(group_plots_dir, exist_ok=True)

        for property_name in network_properties_input_fieldnames:

            if property_name in excluded_columns:
                continue

            network_names = []
            x_values = []
            y_values = []

            for network_name, properties in group_network_properties.items():

                if network_name not in contributions_at_k:
                    continue

                property_value = _parse_optional_float(
                    properties.get(property_name)
                )

                contribution_at_k = contributions_at_k[network_name]

                if property_value is None:
                    continue

                network_names.append(network_name)
                x_values.append(property_value)
                y_values.append(contribution_at_k)

            if len(x_values) < 3 or len(set(x_values)) <= 1:
                continue

            pearson_correlation = _pearson_correlation(
                x_values,
                y_values
            )

            spearman_correlation = _spearman_correlation(
                x_values,
                y_values
            )

            if (
                    pearson_correlation is None
                    or spearman_correlation is None
            ):
                continue

            # Bootstrap confidence intervals
            spearman_ci_lower, spearman_ci_upper = \
                _bootstrap_correlation_confidence_interval(
                    x_values=x_values,
                    y_values=y_values,
                    correlation_function=_spearman_correlation,
                    n_bootstrap=BOOTSTRAP_SAMPLES,
                    confidence_level=CONFIDENCE_LEVEL,
                    random_seed=RANDOM_SEED
                )

            pearson_ci_lower, pearson_ci_upper = \
                _bootstrap_correlation_confidence_interval(
                    x_values=x_values,
                    y_values=y_values,
                    correlation_function=_pearson_correlation,
                    n_bootstrap=BOOTSTRAP_SAMPLES,
                    confidence_level=CONFIDENCE_LEVEL,
                    random_seed=RANDOM_SEED
                )

            output_rows.append({
                "Ground-Truth Type": ground_truth_type,
                "Network Property": property_name,
                "FADDIS Property": "c_K",
                "#Networks": len(x_values),

                "Spearman Correlation": spearman_correlation,
                "Spearman 95% CI Lower": spearman_ci_lower,
                "Spearman 95% CI Upper": spearman_ci_upper,

                "Pearson Correlation": pearson_correlation,
                "Pearson 95% CI Lower": pearson_ci_lower,
                "Pearson 95% CI Upper": pearson_ci_upper,

                "Abs Spearman Correlation (Sort Criterion)":
                    abs(spearman_correlation)
            })

            # Scatter plot
            _plot_scatter(
                network_names=network_names,
                x_values=x_values,
                y_values=y_values,
                property_name=property_name,
                ground_truth_type=ground_truth_type,
                spearman_correlation=spearman_correlation,
                spearman_ci_lower=spearman_ci_lower,
                spearman_ci_upper=spearman_ci_upper,
                pearson_correlation=pearson_correlation,
                pearson_ci_lower=pearson_ci_lower,
                pearson_ci_upper=pearson_ci_upper,
                output_dir=group_plots_dir
            )

            # Leave-one-network-out influence analysis
            _plot_leave_one_out_influence(
                network_names=network_names,
                x_values=x_values,
                y_values=y_values,
                property_name=property_name,
                ground_truth_type=ground_truth_type,
                full_spearman=spearman_correlation,
                full_pearson=pearson_correlation,
                output_dir=group_plots_dir
            )

    ground_truth_type_order = {
        "Non-overlapping and Overlapping": 0,
        "Non-overlapping": 1,
        "Overlapping": 2
    }

    output_rows.sort(
        key=lambda r: (
            ground_truth_type_order[r["Ground-Truth Type"]],
            r["FADDIS Property"],
            -r["Abs Spearman Correlation (Sort Criterion)"]
        )
    )

    for row in output_rows:
        row.pop("Abs Spearman Correlation (Sort Criterion)")

    file = os.path.join(results_dir, output_filename)

    with open(
            file=file,
            mode="w",
            newline="",
            encoding="utf-8"
    ) as out_file:

        writer = csv.DictWriter(
            out_file,
            fieldnames=output_fieldnames
        )

        writer.writeheader()
        writer.writerows(output_rows)


def _plot_scatter(
        network_names: list[str],
        x_values: list[float],
        y_values: list[float],
        property_name: str,
        ground_truth_type: str,
        spearman_correlation: float,
        spearman_ci_lower: float,
        spearman_ci_upper: float,
        pearson_correlation: float,
        pearson_ci_lower: float,
        pearson_ci_upper: float,
        output_dir: str
) -> None:
    """
    Generate a scatter plot between a structural network property and the FADDIS
    contribution at K.

    Each point represents one network and is labelled with its network name. A
    linear least-squares trend line is included for visual interpretation.

    Parameters:
        network_names : (list[str])
            Names of the networks represented in the plot.
        x_values : (list[float])
            Structural network property values.
        y_values : (list[float])
            Corresponding FADDIS contribution values.
        property_name : (str)
            Name of the structural network property.
        ground_truth_type : (str)
            Ground-truth group represented in the plot.
        spearman_correlation : (float)
            Spearman correlation coefficient.
        spearman_ci_lower : (float)
            Lower bound of the Spearman confidence interval.
        spearman_ci_upper : (float)
            Upper bound of the Spearman confidence interval.
        pearson_correlation : (float)
            Pearson correlation coefficient.
        pearson_ci_lower : (float)
            Lower bound of the Pearson confidence interval.
        pearson_ci_upper : (float)
            Upper bound of the Pearson confidence interval.
        output_dir : (str)
            Directory in which the plot is saved.

    Returns:
        None
    """

    x = np.asarray(x_values, dtype=np.float64)
    y = np.asarray(y_values, dtype=np.float64)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.scatter(
        x,
        y,
        s=50
    )

    # Add a simple linear trend line.
    if len(x) >= 2 and np.std(x) > 0:
        slope, intercept = np.polyfit(x, y, 1)

        x_line = np.linspace(
            np.min(x),
            np.max(x),
            100
        )

        y_line = slope * x_line + intercept

        ax.plot(
            x_line,
            y_line,
            linestyle="--",
            linewidth=1.2
        )

    ax.set_xlabel(property_name)
    ax.set_ylabel("FADDIS contribution at K")

    # ax.set_title(
    #    f"{ground_truth_type}\n"
    #    f"{property_name} vs. FADDIS contribution at K"
    # )

    statistics_text = (
        f"Spearman = {spearman_correlation:.3f} "
        f"[95% CI: {_format_optional_float(spearman_ci_lower)}, "
        f"{_format_optional_float(spearman_ci_upper)}]\n"
        f"Pearson = {pearson_correlation:.3f} "
        f"[95% CI: {_format_optional_float(pearson_ci_lower)}, "
        f"{_format_optional_float(pearson_ci_upper)}]"
    )

    ax.text(
        0.02,
        0.98,
        statistics_text,
        transform=ax.transAxes,
        verticalalignment="top",
        fontsize=8,
        bbox={
            "boxstyle": "round",
            "alpha": 0.15
        }
    )

    ax.ticklabel_format(
        axis="y",
        style="sci",
        scilimits=(0, 0)
    )

    ax.grid(
        True,
        alpha=0.25
    )

    fig.tight_layout()

    output_base = os.path.join(
        output_dir,
        f"{_safe_filename(property_name).lower()}_s"
    )

    _save_figure(
        fig=fig,
        output_base=output_base
    )


def _plot_leave_one_out_influence(
        network_names: list[str],
        x_values: list[float],
        y_values: list[float],
        property_name: str,
        ground_truth_type: str,
        full_spearman: float,
        full_pearson: float,
        output_dir: str
) -> None:
    """
    Perform and plot a leave-one-network-out influence analysis.

    For each network, the Pearson and Spearman correlations are recomputed after
    excluding that network. This makes it possible to determine whether an
    observed correlation is strongly driven by a single network.

    Parameters:
        network_names : (list[str])
            Names of the networks included in the analysis.
        x_values : (list[float])
            Structural network property values.
        y_values : (list[float])
            Corresponding FADDIS contribution values.
        property_name : (str)
            Name of the structural network property.
        ground_truth_type : (str)
            Ground-truth group represented in the analysis.
        full_spearman : (float)
            Spearman correlation computed using the complete sample.
        full_pearson : (float)
            Pearson correlation computed using the complete sample.
        output_dir : (str)
            Directory in which the plot is saved.

    Returns:
        None
    """

    # At least three networks should remain after exclusion.
    if len(network_names) < 4:
        return

    excluded_networks = []
    spearman_values = []
    pearson_values = []

    for excluded_idx, excluded_network in enumerate(network_names):

        x_leave_one_out = [
            value
            for idx, value in enumerate(x_values)
            if idx != excluded_idx
        ]

        y_leave_one_out = [
            value
            for idx, value in enumerate(y_values)
            if idx != excluded_idx
        ]

        if (
                len(x_leave_one_out) < 3
                or len(set(x_leave_one_out)) <= 1
        ):
            continue

        spearman = _spearman_correlation(
            x_leave_one_out,
            y_leave_one_out
        )

        pearson = _pearson_correlation(
            x_leave_one_out,
            y_leave_one_out
        )

        if spearman is None or pearson is None:
            continue

        excluded_networks.append(excluded_network)
        spearman_values.append(spearman)
        pearson_values.append(pearson)

    if not excluded_networks:
        return

    positions = np.arange(len(excluded_networks))

    fig_width = max(
        8,
        len(excluded_networks) * 0.7
    )

    fig, ax = plt.subplots(
        figsize=(fig_width, 6)
    )

    spearman_line, = ax.plot(
        positions,
        spearman_values,
        marker="o",
        linewidth=1.5,
        label="Spearman after exclusion"
    )

    pearson_line, = ax.plot(
        positions,
        pearson_values,
        marker="s",
        linewidth=1.5,
        label="Pearson after exclusion"
    )

    # Full-sample correlations as reference lines.
    ax.axhline(
        full_spearman,
        color=spearman_line.get_color(),
        linestyle="--",
        linewidth=1.2,
        label=f"Full Spearman ({full_spearman:.3f})"
    )

    ax.axhline(
        full_pearson,
        color=pearson_line.get_color(),
        linestyle=":",
        linewidth=1.2,
        label=f"Full Pearson ({full_pearson:.3f})"
    )

    ax.axhline(
        0.0,
        linewidth=0.8,
        alpha=0.5
    )

    ax.set_xticks(positions)

    ax.set_xticklabels(
        excluded_networks,
        rotation=45,
        ha="right"
    )

    ax.set_ylim(
        -1.05,
        1.05
    )

    ax.set_xlabel("Excluded network")
    ax.set_ylabel("Correlation coefficient")

    # ax.set_title(
    #    f"{ground_truth_type}\n"
    #    f"Leave-one-network-out influence: {property_name}"
    # )

    ax.grid(
        True,
        axis="y",
        alpha=0.25
    )

    ax.legend(
        fontsize=8
    )

    fig.tight_layout()

    output_base = os.path.join(
        output_dir,
        f"{_safe_filename(property_name).lower()}_l"
    )

    _save_figure(
        fig=fig,
        output_base=output_base
    )


def _bootstrap_correlation_confidence_interval(
        x_values: list[float],
        y_values: list[float],
        correlation_function,
        n_bootstrap: int = 10000,
        confidence_level: float = 0.95,
        random_seed: int = 42
) -> tuple[float, float]:
    """
    Compute a percentile bootstrap confidence interval for a correlation
    coefficient.

    Paired observations are resampled together so that the association between
    each network property and its corresponding FADDIS contribution is
    preserved.

    Parameters:
        x_values : (list[float])
            Structural network property values.
        y_values : (list[float])
            Corresponding FADDIS contribution values.
        correlation_function :
            Function used to compute the correlation coefficient.
        n_bootstrap : (int)
            Number of bootstrap samples.
        confidence_level : (float)
            Confidence level.
        random_seed : (int)
            Random seed used for reproducibility.

    Returns:
        lower_bound, upper_bound : (tuple[float, float])
            Bootstrap confidence interval bounds.
    """

    x = np.asarray(
        x_values,
        dtype=np.float64
    )

    y = np.asarray(
        y_values,
        dtype=np.float64
    )

    n = len(x)

    if n < 3:
        return None, None

    rng = np.random.default_rng(
        random_seed
    )

    bootstrap_correlations = []

    for _ in range(n_bootstrap):

        sample_indices = rng.integers(
            low=0,
            high=n,
            size=n
        )

        x_sample = x[sample_indices]
        y_sample = y[sample_indices]

        correlation = correlation_function(
            x_sample.tolist(),
            y_sample.tolist()
        )

        if (
                correlation is not None
                and np.isfinite(correlation)
        ):
            bootstrap_correlations.append(
                correlation
            )

    if len(bootstrap_correlations) < 2:
        return None, None

    alpha = 1.0 - confidence_level

    lower_percentile = (
            100.0 * alpha / 2.0
    )

    upper_percentile = (
            100.0 * (1.0 - alpha / 2.0)
    )

    lower_bound, upper_bound = np.percentile(
        bootstrap_correlations,
        [
            lower_percentile,
            upper_percentile
        ]
    )

    return (
        float(lower_bound),
        float(upper_bound)
    )


def _save_figure(
        fig,
        output_base: str
) -> None:
    """
    Save a figure using the configured output format.

    Parameters:
        fig :
            Figure to save.
        output_base : (str)
            Base path used to construct the output filename.

    Returns:
        None
    """

    # fig.savefig(
    #    f"{output_base}.png",
    #    dpi=300,
    #    bbox_inches="tight"
    # )

    fig.savefig(
        f"{output_base}.pdf",
        bbox_inches="tight"
    )

    plt.close(fig)


def _safe_filename(value: str) -> str:
    """
    Convert a string into a filename-safe representation.

    Parameters:
        value : (str)
            String to convert.

    Returns:
        safe_value : (str)
            Filename-safe representation of the input string.
    """

    return "".join(
        character
        if character.isalnum() or character in ("-", "_")
        else "_"
        for character in value
    )


def _format_optional_float(
        value: float
) -> str:
    """
    Format an optional floating-point value.

    Parameters:
        value : (float)
            Floating-point value to format.

    Returns:
        formatted_value : (str)
            Value formatted to three decimal places, or "--" when unavailable.
    """

    if value is None:
        return "--"

    return f"{value:.3f}"


def _load_network_properties(
        input_path: str
) -> dict[str, dict]:
    """
    Load network properties from a CSV file.

    Parameters:
        input_path : (str)
            Path to the input CSV file.

    Returns:
        properties_by_network : (dict[str, dict])
            Network properties indexed by network name.
    """

    properties_by_network = {}

    with open(
            input_path,
            "r",
            newline="",
            encoding="utf-8"
    ) as in_file:
        reader = csv.DictReader(in_file)

        for row in reader:
            properties_by_network[
                row["Network"]
            ] = row

    return properties_by_network


def _load_valid_contributions_at_k(
        results_dir: str,
        raw_contributions_input_filename: str,
        raw_contributions_input_fieldnames: list,
        apply_lapin: bool
) -> dict[str, float]:
    """
    Load the valid FADDIS contributions corresponding to the ground-truth
    number of communities.

    Parameters:
        results_dir : (str)
            Path to the results directory containing the network-family
            subdirectories.
        raw_contributions_input_filename : (str)
            Name of the input CSV file containing the raw contributions.
        raw_contributions_input_fieldnames : (list)
            Base field names of the raw contributions CSV file.
        apply_lapin : (bool)
            Whether LAPIN was applied before running FADDIS.

    Returns:
        contributions_at_k : (dict[str, float])
            Valid contribution at K for each network.
    """

    contributions_at_k = {}

    network_family_dirs = sorted(
        [
            directory
            for directory in Path(results_dir).iterdir()
            if directory.is_dir()
        ],
        key=lambda path: path.name
    )

    for network_family_dir in network_family_dirs:

        input_path = os.path.join(
            network_family_dir,
            raw_contributions_input_filename
        )

        if not os.path.exists(input_path):
            continue

        with open(
                input_path,
                "r",
                newline="",
                encoding="utf-8"
        ) as in_file:

            reader = csv.reader(in_file)
            next(reader, None)

            for row in reader:

                network_name = row[0]
                k = int(row[1])

                contributions = [
                    float(value)
                    for value
                    in row[len(raw_contributions_input_fieldnames):]
                    if value != ""
                ]

                # Without LAPIN, the first extracted component is the
                # background component, so community K is K+1.
                contribution_idx = (
                    k - 1
                    if apply_lapin
                    else k
                )

                if contribution_idx >= len(contributions):
                    continue

                contribution_at_k = contributions[
                    contribution_idx
                ]

                contributions_at_k[
                    network_name
                ] = contribution_at_k

    return contributions_at_k


def _parse_optional_float(
        value: str
) -> float:
    """
    Parse an optional value as a finite floating-point number.

    Parameters:
        value : (str)
            Value to parse.

    Returns:
        parsed_value : (float | None)
            Parsed floating-point value, or None if the value is missing,
            invalid, or non-finite.
    """

    if value is None or value == "":
        return None

    try:

        parsed_value = float(value)

        if not np.isfinite(parsed_value):
            return None

        return parsed_value

    except (TypeError, ValueError):
        return None


def _pearson_correlation(
        x_values: list[float],
        y_values: list[float]
) -> float:
    """
    Compute the Pearson correlation coefficient between two sequences of values.

    Parameters:
        x_values : (list[float])
            Values of the first variable.
        y_values : (list[float])
            Values of the second variable.

    Returns:
        correlation : (float | None)
            Pearson correlation coefficient, or None if either variable has
            zero variance.
    """

    x = np.asarray(
        x_values,
        dtype=np.float64
    )

    y = np.asarray(
        y_values,
        dtype=np.float64
    )

    if (
            np.std(x) == 0
            or np.std(y) == 0
    ):
        return None

    return float(
        np.corrcoef(x, y)[0, 1]
    )


def _spearman_correlation(
        x_values: list[float],
        y_values: list[float]
) -> float:
    """
    Compute the Spearman rank correlation coefficient between two sequences of
    values.

    Parameters:
        x_values : (list[float])
            Values of the first variable.
        y_values : (list[float])
            Values of the second variable.

    Returns:
        correlation : (float | None)
            Spearman rank correlation coefficient, or None if either ranked
            variable has zero variance.
    """

    return _pearson_correlation(
        _rank_values(x_values),
        _rank_values(y_values)
    )


def _rank_values(
        values: list[float]
) -> list[float]:
    """
    Assign average ranks to a sequence of values.

    Tied values receive the average of their rank positions.

    Parameters:
        values : (list[float])
            Values to rank.

    Returns:
        ranks : (list[float])
            Rank assigned to each value in its original position.
    """

    sorted_indices = sorted(
        range(len(values)),
        key=lambda idx: values[idx]
    )

    ranks = [
        0.0
        for _ in values
    ]

    i = 0

    while i < len(values):

        j = i

        while (
                j + 1 < len(values)
                and values[sorted_indices[j + 1]]
                == values[sorted_indices[i]]
        ):
            j += 1

        average_rank = (
                               i + j + 2
                       ) / 2

        for rank_idx in range(
                i,
                j + 1
        ):
            ranks[
                sorted_indices[rank_idx]
            ] = average_rank

        i = j + 1

    return ranks
