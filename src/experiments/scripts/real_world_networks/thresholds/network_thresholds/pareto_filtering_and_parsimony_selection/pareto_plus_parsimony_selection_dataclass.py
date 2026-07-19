from dataclasses import field, dataclass

from experiments.scripts.real_world_networks.thresholds.utils.csv_dataclass import CsvDataclass


@dataclass
class ParetoPlusParsimonySelection(CsvDataclass):
    """
    Dataclass for Pareto-plus-parsimony selection results.

    Attributes:
        acceptable : (bool)
            Whether the candidate threshold satisfies the combined acceptability criteria.
    """

    acceptable: bool = field(metadata={"label": "Acceptable?"})
