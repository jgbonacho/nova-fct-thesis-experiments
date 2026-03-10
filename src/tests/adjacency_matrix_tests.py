import unittest

import networkx as nx
import numpy as np

from experiments.loaders.adjacency_matrix import compute_adjacency_matrix


class Test(unittest.TestCase):
    def test_adjacency_matrix(self):
        graph = nx.Graph()
        graph.add_edges_from([(0, 1), (1, 2), (2, 0), (2, 3)])
        A = compute_adjacency_matrix(graph)

        self.assertTrue(np.allclose(A, A.T), "Adjacency matrix is not symmetric.")
        self.assertTrue(np.all((A == 0) | (A == 1)), "Adjacency matrix is not binary.")
        self.assertTrue(np.all(np.diag(A) == 0), "Adjacency matrix diagonal is not zero.")


if __name__ == "__main__":
    unittest.main()
