from enum import Enum

import numpy as np

from experiments.scripts.real_world_networks.utils.affinity_designs.binary_set_similarities import compute_kul, \
    compute_dice, compute_ochiai
from experiments.scripts.real_world_networks.utils.affinity_designs.weighted_inner_product_similarities import \
    compute_ip, compute_cosip


class AffinityDesign(str, Enum):
    """
    Enumeration of the supported affinity-matrix designs.

    Attributes:
        DEFAULT : (str)
            Use the original adjacency matrix as the affinity matrix.
        KUL : (str)
            Use the Kulczynski binary-set similarity.
        DICE : (str)
            Use the Dice binary-set similarity.
        OCHIAI : (str)
            Use the Ochiai binary-set similarity.
        IP_B0 : (str)
            Use the weighted inner-product similarity with beta equal to 0.
        IP_B0_5 : (str)
            Use the weighted inner-product similarity with beta equal to 0.5.
        IP_B1 : (str)
            Use the weighted inner-product similarity with beta equal to 1.
        COSIP_B0 : (str)
            Use the cosine-weighted inner-product similarity with beta equal to 0.
        COSIP_B0_5 : (str)
            Use the cosine-weighted inner-product similarity with beta equal to 0.5.
        COSIP_B1 : (str)
            Use the cosine-weighted inner-product similarity with beta equal to 1.
    """

    DEFAULT = "Default"
    KUL = "Kul"
    DICE = "Dice"
    OCHIAI = "Ochiai"
    IP_B0 = "Ip_b0"
    IP_B0_5 = "Ip_b0.5"
    IP_B1 = "Ip_b1"
    COSIP_B0 = "CosIp_b0"
    COSIP_B0_5 = "CosIp_b0.5"
    COSIP_B1 = "CosIp_b1"

    def apply_affinity_design(self, A: np.ndarray) -> np.ndarray:
        """
        Apply the selected affinity design to an adjacency matrix.

        Parameters:
            A : (np.ndarray, shape[n,n])
                Adjacency matrix of the network.

        Returns:
            W : (np.ndarray, shape[n,n])
                Affinity matrix obtained using the selected affinity design.

        Raises:
            ValueError
                If the selected affinity design is unknown.
        """

        if self == AffinityDesign.DEFAULT:
            return A.copy()
        elif self == AffinityDesign.KUL:
            return compute_kul(A)
        elif self == AffinityDesign.DICE:
            return compute_dice(A)
        elif self == AffinityDesign.OCHIAI:
            return compute_ochiai(A)
        elif self == AffinityDesign.IP_B0:
            return compute_ip(A, beta=0)
        elif self == AffinityDesign.IP_B0_5:
            return compute_ip(A, beta=0.5)
        elif self == AffinityDesign.IP_B1:
            return compute_ip(A, beta=1)
        elif self == AffinityDesign.COSIP_B0:
            return compute_cosip(A, beta=0)
        elif self == AffinityDesign.COSIP_B0_5:
            return compute_cosip(A, beta=0.5)
        elif self == AffinityDesign.COSIP_B1:
            return compute_cosip(A, beta=1)
        else:
            raise ValueError(f"[ERROR] Unknown affinity design: {self.value}.")
