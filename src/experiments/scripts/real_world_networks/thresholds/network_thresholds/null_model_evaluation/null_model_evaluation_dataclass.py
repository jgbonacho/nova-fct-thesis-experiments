from dataclasses import field, dataclass

from experiments.scripts.real_world_networks.thresholds.utils.csv_dataclass import CsvDataclass


@dataclass
class NullModelEvaluation(CsvDataclass):
    """
    Dataclass for null-model evaluation results.

    Attributes:
        number_of_null_graphs : (int)
            Number of null-model graphs generated.
        number_of_valid_results : (int)
            Number of null-model graphs that produced valid modularity and conductance results.
        null_modularities : (list[float])
            Modularity values obtained from the valid null-model community structures.
        mean_null_modularity : (float)
            Mean modularity across the valid null-model results.
        std_null_modularity : (float)
            Sample standard deviation of the valid null-model modularities.
        modularity_z_score : (float)
            Standardized difference between the real modularity and the mean null modularity.
        modularity_empirical_p_value : (float)
            Empirical upper-tail p-value of the real modularity under the null model.
        modularity_rank : (int)
            Rank of the real modularity among the null-model modularities.
        null_conductances : (list[float])
            Conductance values obtained from the valid null-model community structures.
        mean_null_conductance : (float)
            Mean conductance across the valid null-model results.
        std_null_conductance : (float)
            Sample standard deviation of the valid null-model conductances.
        conductance_z_score : (float)
            Standardized difference between the mean null conductance and the real conductance.
        conductance_empirical_p_value : (float)
            Empirical lower-tail p-value of the real conductance under the null model.
        conductance_rank : (int)
            Rank of the real conductance among the null-model conductances.
        acceptable_null_model : (bool | None)
            Whether the modularity and conductance evidence satisfy the null-model acceptability criteria.
            None if not yet evaluated.
    """

    number_of_null_graphs: int = field(metadata={"label": "#Null Graphs"})
    number_of_valid_results: int = field(metadata={"label": "#Valid Null Modularities and Conductances"})
    null_modularities: list[float] = field(metadata={"label": "Null Modularities"})
    mean_null_modularity: float = field(metadata={"label": "Mean Null Modularity"})
    std_null_modularity: float = field(metadata={"label": "Std Null Modularity"})
    modularity_z_score: float = field(metadata={"label": "Z Modularity"})
    modularity_empirical_p_value: float = field(metadata={"label": "Modularity Empirical p-value"})
    modularity_rank: int = field(metadata={"label": "Modularity Rank"})
    null_conductances: list[float] = field(metadata={"label": "Null Conductances"})
    mean_null_conductance: float = field(metadata={"label": "Mean Null Conductance"})
    std_null_conductance: float = field(metadata={"label": "Std Null Conductance"})
    conductance_z_score: float = field(metadata={"label": "Z Conductance"})
    conductance_empirical_p_value: float = field(metadata={"label": "Conductance Empirical p-value"})
    conductance_rank: int = field(metadata={"label": "Conductance Rank"})
    acceptable_null_model: bool = field(metadata={"label": "Acceptable Null Model?"}, default=None)
