"""
Entry point.
"""

from experiments.scripts.contributions_in_lfr_networks import run_contributions_experiments_in_lfr_networks
from experiments.scripts.executions_in_lfr_networks import run_executions_experiments_in_lfr_networks


def main():
    run_contributions_experiments_in_lfr_networks(desired_k=True, apply_lapin=False)
    run_executions_experiments_in_lfr_networks(apply_lapin=False)

    run_contributions_experiments_in_lfr_networks(desired_k=True, apply_lapin=True)
    run_executions_experiments_in_lfr_networks(apply_lapin=True)

    run_contributions_experiments_in_lfr_networks(desired_k=False, apply_lapin=False)
    run_executions_experiments_in_lfr_networks(apply_lapin=False)

    run_contributions_experiments_in_lfr_networks(desired_k=False, apply_lapin=True)
    run_executions_experiments_in_lfr_networks(apply_lapin=True)


if __name__ == "__main__":
    main()
