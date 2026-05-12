"""
Entry point.
"""

from experiments.scripts.contributions_experiments_in_lfr_networks import run_contributions_experiments_in_lfr_networks
from experiments.scripts.contributions_experiments_in_real_world_networks import \
    run_contributions_experiments_in_real_world_networks


def main():
    # LFR experience with 'LAPIN-off + Extraction of K desired clusters'
    run_contributions_experiments_in_lfr_networks(apply_lapin=False, use_desired_k=True)

    # LFR experience with 'LAPIN-off + Extraction of clusters until the end'
    run_contributions_experiments_in_lfr_networks(apply_lapin=False, use_desired_k=False)

    # LFR experience with 'LAPIN-on + Extraction of K desired clusters'
    run_contributions_experiments_in_lfr_networks(apply_lapin=True, use_desired_k=True)

    # LFR experience with 'LAPIN-on + Extraction of clusters until the end'
    run_contributions_experiments_in_lfr_networks(apply_lapin=True, use_desired_k=False)

    # ---

    # Real-world experience with 'LAPIN-off + Extraction of K desired clusters'
    run_contributions_experiments_in_real_world_networks(apply_lapin=False, use_desired_k=True)

    # Real-world experience with 'LAPIN-off + Extraction of clusters until the end'
    run_contributions_experiments_in_real_world_networks(apply_lapin=False, use_desired_k=False)

    # Real-world experience with 'LAPIN-on + Extraction of K desired clusters'
    run_contributions_experiments_in_real_world_networks(apply_lapin=True, use_desired_k=True)

    # Real-world experience with 'LAPIN-on + Extraction of clusters until the end'
    run_contributions_experiments_in_real_world_networks(apply_lapin=True, use_desired_k=False)


if __name__ == "__main__":
    main()
