"""
Entry point.
"""

from experiments.scripts.contributions_experiments_in_lfr_networks import run_contributions_experiments_in_lfr_networks
from experiments.scripts.contributions_experiments_in_real_world_networks import \
    run_contributions_experiments_in_real_world_networks
from experiments.scripts.sensitivity_experiments_in_real_world_networks import \
    run_sensitivity_experiments_in_real_world_networks
from experiments.utils.dataclasses.real_world_threshold_estimation_config import RealWorldThresholdEstimationConfig


def main(estimate_lfr_network_thresholds=True, estimate_real_world_network_thresholds=True):
    """
    Entry point.

    Parameters:
        estimate_lfr_network_thresholds : (bool, optional)
            Whether to estimate thresholds in LFR networks.
            Defaults to True.
        estimate_real_world_network_thresholds : (bool, optional)
            Whether to estimate thresholds in real-world networks.
            Defaults to True.
    """

    if estimate_lfr_network_thresholds:
        ## LFR experience with 'LAPIN-off + Extraction of K desired clusters'
        run_contributions_experiments_in_lfr_networks(apply_lapin=False, use_desired_k=True)

        ## LFR experience with 'LAPIN-off + Extraction of clusters until the end'
        # run_contributions_experiments_in_lfr_networks(apply_lapin=False, use_desired_k=False)

        ## LFR experience with 'LAPIN-on + Extraction of K desired clusters'
        # run_contributions_experiments_in_lfr_networks(apply_lapin=True, use_desired_k=True)

        ## LFR experience with 'LAPIN-on + Extraction of clusters until the end'
        # run_contributions_experiments_in_lfr_networks(apply_lapin=True, use_desired_k=False)

    if estimate_real_world_network_thresholds:
        run_sensitivity_experiments_in_real_world_networks(apply_lapin=True)

        run_contributions_experiments_in_real_world_networks(config=RealWorldThresholdEstimationConfig(
            apply_lapin=True,
            overlapping_communities=False
        ))
        run_contributions_experiments_in_real_world_networks(config=RealWorldThresholdEstimationConfig(
            apply_lapin=True,
            overlapping_communities=True
        ))
        run_contributions_experiments_in_real_world_networks(config=RealWorldThresholdEstimationConfig(
            apply_lapin=True,
            overlapping_communities=False,
            pareto_tolerance_fraction_modularity=0.10,
            pareto_tolerance_fraction_conductance=0.10,
            pareto_tolerance_fraction_stability=0.10
        ))
        run_contributions_experiments_in_real_world_networks(config=RealWorldThresholdEstimationConfig(
            apply_lapin=True,
            overlapping_communities=True,
            pareto_tolerance_fraction_modularity=0.10,
            pareto_tolerance_fraction_conductance=0.10,
            pareto_tolerance_fraction_stability=0.10
        ))


if __name__ == "__main__":
    main(
        estimate_lfr_network_thresholds=False,
        estimate_real_world_network_thresholds=True,
    )
