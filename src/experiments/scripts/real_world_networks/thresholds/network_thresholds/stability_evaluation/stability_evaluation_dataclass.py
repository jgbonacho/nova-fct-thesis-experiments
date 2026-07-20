from dataclasses import dataclass, field

from experiments.scripts.real_world_networks.utils.csv_dataclass import CsvDataclass


@dataclass
class StabilityEvaluation(CsvDataclass):
    """
    Dataclass for perturbation stability evaluation results.

    Attributes:
        number_of_perturbed_graphs : (int)
            Number of perturbed graphs generated for the stability evaluation.
        number_of_valid_similarities : (int)
            Number of valid similarity values obtained from the perturbed graphs.
        similarities : (list[float])
            Similarity values between the original and perturbed community structures.
        stability : (float)
            Average similarity across the valid perturbed community structures.
        acceptable_stability : (bool | None)
            Whether the stability satisfies the acceptability criterion.
            None if not yet evaluated.
    """

    number_of_perturbed_graphs: int = field(metadata={"label": "#Perturbed Graphs"})
    number_of_valid_similarities: int = field(metadata={"label": "#Valid Similarities"})
    similarities: list[float] = field(metadata={"label": "Similarities"})
    stability: float = field(metadata={"label": "Stability"})
    acceptable_stability: bool = field(metadata={"label": "Acceptable Stability?"}, default=None)
