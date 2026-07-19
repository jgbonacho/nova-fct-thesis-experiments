from dataclasses import dataclass, field


@dataclass
class LFRThresholdEstimationConfig:
    """
    Dataclass for the LFR threshold estimation configuration.

    Attributes:
        apply_lapin : (bool)
            Whether to apply the LAPIN transformation.
            Default is False.
        use_desired_k : (bool)
            Whether to use the desired number of communities as the FADDIS stopping criterion.
            Default is True.
        bootstrapping_maximum_number_of_repetitions : (int)
            Maximum number of bootstrap repetitions used for threshold selection.
            Default is 1000.
        bootstrapping_subsample_fraction : (float)
            Fraction of networks sampled in each bootstrap repetition.
            Default is 0.8.
    """

    apply_lapin: bool = field(default=False)
    use_desired_k: bool = field(default=True)
    bootstrapping_maximum_number_of_repetitions: int = field(default=1000)
    bootstrapping_subsample_fraction: float = field(default=0.8)
