"""
Entry point.
"""

from experiments.scripts.lfr_networks.thresholds.estimate_lfr_network_family_thresholds import \
    estimate_lfr_network_family_thresholds
from experiments.scripts.lfr_networks.thresholds.lfr_threshold_estimation_config import LFRThresholdEstimationConfig
from experiments.scripts.real_world_networks.sensitivity_analysis.sensitivity_analysis_in_real_world_networks import \
    sensitivity_analysis_in_real_world_networks
from experiments.scripts.real_world_networks.thresholds.estimate_real_world_network_thresholds import \
    estimate_real_world_network_thresholds
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig


def main(run_lfr_networks_scripts=True, run_real_world_networks_scripts=True):
    """
    Entry point.

    Parameters:
        run_lfr_networks_scripts : (bool, optional)
            Whether to estimate thresholds in LFR networks.
            Defaults to True.
        run_real_world_networks_scripts : (bool, optional)
            Whether to estimate thresholds in real-world networks.
            Defaults to True.
    """

    if run_lfr_networks_scripts:
        ## LFR experience with 'LAPIN-off + Extraction of K desired clusters'
        estimate_lfr_network_family_thresholds(
            config=LFRThresholdEstimationConfig(apply_lapin=False, use_desired_k=True)
        )

        ## LFR experience with 'LAPIN-off + Extraction of clusters until the end'
        # estimate_lfr_network_family_thresholds(
        #    config=LFRThresholdEstimationConfig(apply_lapin=False, use_desired_k=False)
        # )

        ## LFR experience with 'LAPIN-on + Extraction of K desired clusters'
        # estimate_lfr_network_family_thresholds(
        #    config=LFRThresholdEstimationConfig(apply_lapin=True, use_desired_k=True)
        # )

        ## LFR experience with 'LAPIN-on + Extraction of clusters until the end'
        # estimate_lfr_network_family_thresholds(
        #    config=LFRThresholdEstimationConfig(apply_lapin=True, use_desired_k=False)
        # )

    if run_real_world_networks_scripts:
        sensitivity_analysis_in_real_world_networks(apply_lapin=True)

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                overlapping_communities=True
            )
        )


if __name__ == "__main__":
    main(
        run_lfr_networks_scripts=False,
        run_real_world_networks_scripts=True,
    )
