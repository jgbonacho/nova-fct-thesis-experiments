"""
Entry point.
"""

from experiments.scripts.lfr_networks.thresholds.estimate_lfr_network_family_thresholds import \
    estimate_lfr_network_family_thresholds
from experiments.scripts.lfr_networks.thresholds.lfr_threshold_estimation_config import LFRThresholdEstimationConfig
from experiments.scripts.real_world_networks.networks_characterization.real_world_networks_characterization import \
    characterization_of_real_world_networks
from experiments.scripts.real_world_networks.sensitivity_analysis.sensitivity_analysis_in_real_world_networks import \
    sensitivity_analysis_in_real_world_networks
from experiments.scripts.real_world_networks.thresholds.estimate_real_world_network_thresholds import \
    estimate_real_world_network_thresholds
from experiments.scripts.real_world_networks.thresholds.real_world_threshold_estimation_config import \
    RealWorldThresholdEstimationConfig
from experiments.scripts.real_world_networks.utils.affinity_designs.affinity_design_dataclass import AffinityDesign


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
        # Configuration 1.
        estimate_lfr_network_family_thresholds(
            config=LFRThresholdEstimationConfig(apply_lapin=False, use_desired_k=True)
        )

        # Configuration 2.
        estimate_lfr_network_family_thresholds(
            config=LFRThresholdEstimationConfig(apply_lapin=False, use_desired_k=False)
        )

        # Configuration 3.
        estimate_lfr_network_family_thresholds(
            config=LFRThresholdEstimationConfig(apply_lapin=True, use_desired_k=True)
        )

        # Configuration 4.
        estimate_lfr_network_family_thresholds(
            config=LFRThresholdEstimationConfig(apply_lapin=True, use_desired_k=False)
        )

    if run_real_world_networks_scripts:
        # Networks characterization.
        characterization_of_real_world_networks()

        # Sensitivity analysis.
        sensitivity_analysis_in_real_world_networks(apply_lapin=True)
        sensitivity_analysis_in_real_world_networks(apply_lapin=False)

        # Thresholds estimation.
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.DEFAULT, apply_lapin=True, overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.DEFAULT, apply_lapin=False, overlapping_communities=False
            )
        )

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.IP_B0, apply_lapin=True, overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.IP_B0, apply_lapin=False, overlapping_communities=False
            )
        )

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.COSIP_B0, apply_lapin=True, overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.COSIP_B0, apply_lapin=False, overlapping_communities=False
            )
        )

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.KUL, apply_lapin=True, overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.KUL, apply_lapin=False, overlapping_communities=False
            )
        )

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.DICE, apply_lapin=True, overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.DICE, apply_lapin=False, overlapping_communities=False
            )
        )

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.OCHIAI, apply_lapin=True, overlapping_communities=False
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.OCHIAI, apply_lapin=False, overlapping_communities=False
            )
        )

        # ---

        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.DEFAULT, apply_lapin=True, overlapping_communities=True
            )
        )
        estimate_real_world_network_thresholds(
            config=RealWorldThresholdEstimationConfig(
                affinity_design=AffinityDesign.DEFAULT, apply_lapin=False, overlapping_communities=True
            )
        )


if __name__ == "__main__":
    main(
        run_lfr_networks_scripts=False,
        run_real_world_networks_scripts=True,
    )
