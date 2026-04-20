"""
Entry point.
"""

from experiments.scripts.contributions_experiments_in_lfr_networks import \
    run_contributions_experiments_in_lfr_networks


def run_experience(apply_lapin: bool, use_desired_k: bool) -> None:
    """
    Run an experience.

    Parameters:
        apply_lapin : (bool)
            Whether to apply the Lapin transformation.
        use_desired_k : (bool)
            Whether to use the desired number of communities.
    """

    run_contributions_experiments_in_lfr_networks(apply_lapin, use_desired_k)


def main():
    # Experience with 'LAPIN-off + Extraction of K desired clusters'
    run_experience(apply_lapin=False, use_desired_k=True)

    # Experience with 'LAPIN-off + Extraction of clusters until the end'
    # run_experience(apply_lapin=False, use_desired_k=False)

    # Experience with 'LAPIN-on + Extraction of K desired clusters'
    # run_experience(apply_lapin=True, use_desired_k=True)

    # Experience with 'LAPIN-on + Extraction of clusters until the end'
    # run_experience(apply_lapin=True, use_desired_k=False)


if __name__ == "__main__":
    main()
