"""
Entry point.
"""

from experiments.scripts.contributions_in_lfr_networks import run_contributions_in_lfr_networks_experiments


def main():
    run_contributions_in_lfr_networks_experiments(desired_k=True, apply_lapin=False, threshold_metric="Median")
    # run_contributions_in_lfr_networks_experiments(desired_k=False, apply_lapin=False, threshold_metric="Median")
    # run_contributions_in_lfr_networks_experiments(desired_k=True, apply_lapin=True, threshold_metric="Median")
    # run_contributions_in_lfr_networks_experiments(desired_k=False, apply_lapin=True, threshold_metric="Median")


if __name__ == "__main__":
    main()
