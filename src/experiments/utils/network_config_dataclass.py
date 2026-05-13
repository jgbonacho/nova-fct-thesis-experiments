from dataclasses import dataclass


@dataclass
class NetworkConfig:
    """
    Dataclass for real-world network configurations.

    Attributes:
        name : (str)
            The name of the network.
        gml_filename : (str)
            The name of the GML file associated with the network.
        ground_truth : (bool)
            Whether the network has ground-truth community labels.
        overlapping_ground_truth : (bool)
            Whether the ground-truth communities are overlapping.
        ground_truth_attr : (str)
            The node attribute containing the ground-truth community label.
    """

    name: str
    gml_filename: str
    ground_truth: bool
    overlapping_ground_truth: bool
    ground_truth_attr: str

    @staticmethod
    def from_dict(data):
        """
        Create a NetworkConfig object from a dictionary.

        Parameters:
            data : (dict)
                The dictionary containing the network configuration.

        Returns:
            network : (NetworkConfig)
                The created NetworkConfig object.
        """

        return NetworkConfig(
            name=data["name"],
            gml_filename=data['gml_filename'],
            ground_truth=data['ground_truth'],
            overlapping_ground_truth=data['overlapping_ground_truth'],
            ground_truth_attr=data['ground_truth_attr'],
        )
