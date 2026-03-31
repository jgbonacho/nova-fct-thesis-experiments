"""
Entry point.
"""

from experiments.scripts.contributions_experiments_in_lfr_networks import \
    run_contributions_experiments_in_lfr_networks
from experiments.scripts.experiments_in_lfr_networks import \
    run_experiments_in_lfr_networks


def run_experience(apply_lapin, use_desired_k):
    print("\n###### Script 1")
    results_path = run_contributions_experiments_in_lfr_networks(apply_lapin, use_desired_k)
    print("\n###### Script 2")
    run_experiments_in_lfr_networks(results_path, apply_lapin)


def main():
    # Experience 1
    run_experience(apply_lapin=False, use_desired_k=True)

    # Experience 2
    run_experience(apply_lapin=False, use_desired_k=False)

    # Experience 3
    run_experience(apply_lapin=True, use_desired_k=True)

    # Experience 4
    run_experience(apply_lapin=True, use_desired_k=False)


if __name__ == "__main__":
    main()
