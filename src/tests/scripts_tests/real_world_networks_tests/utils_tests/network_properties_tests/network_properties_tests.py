import math
import unittest

import networkx as nx

from experiments.scripts.real_world_networks.utils.network_properties.network_properties import \
    compute_network_properties
from experiments.scripts.real_world_networks.utils.network_properties.network_properties_dataclass import \
    NetworkProperties


class TestNetworkProperties(unittest.TestCase):

    def test_compute_network_properties_for_path_graph(self):
        graph = nx.path_graph(4)

        properties = compute_network_properties(
            network_name="path",
            graph=graph,
            ground_truth=True,
            overlapping_ground_truth=False
        )

        self.assertEqual(properties.network, "path")
        self.assertEqual(properties.nodes_lcc, 4)
        self.assertEqual(properties.edges_lcc, 3)
        self.assertEqual(properties.min_degree, 1.0)
        self.assertEqual(properties.max_degree, 2.0)
        self.assertAlmostEqual(properties.average_degree, 1.5)
        self.assertAlmostEqual(properties.degree_std, math.sqrt(1.0 / 3.0))
        self.assertAlmostEqual(
            properties.degree_cv,
            math.sqrt(1.0 / 3.0) / 1.5
        )
        self.assertAlmostEqual(properties.degree_hub_ratio, 2.0 / 1.5)
        self.assertAlmostEqual(properties.degree_assortativity, -0.5)
        self.assertAlmostEqual(properties.density, 0.5)
        self.assertAlmostEqual(properties.sparsity, 0.5)
        self.assertEqual(properties.global_clustering_coefficient, 0.0)
        self.assertEqual(properties.average_clustering, 0.0)
        self.assertTrue(properties.ground_truth)
        self.assertFalse(properties.overlapping_ground_truth)

    def test_compute_network_properties_for_triangle_graph(self):
        graph = nx.complete_graph(3)

        properties = compute_network_properties(
            network_name="triangle",
            graph=graph,
            ground_truth=False,
            overlapping_ground_truth=False
        )

        self.assertEqual(properties.nodes_lcc, 3)
        self.assertEqual(properties.edges_lcc, 3)
        self.assertEqual(properties.min_degree, 2.0)
        self.assertEqual(properties.max_degree, 2.0)
        self.assertEqual(properties.average_degree, 2.0)
        self.assertEqual(properties.degree_std, 0.0)
        self.assertEqual(properties.degree_cv, 0.0)
        self.assertEqual(properties.degree_hub_ratio, 1.0)
        self.assertAlmostEqual(properties.density, 1.0)
        self.assertAlmostEqual(properties.sparsity, 0.0)
        self.assertAlmostEqual(properties.global_clustering_coefficient, 1.0)
        self.assertAlmostEqual(properties.average_clustering, 1.0)

    def test_compute_network_properties_for_empty_graph(self):
        properties = compute_network_properties(
            network_name="empty",
            graph=nx.Graph(),
            ground_truth=False,
            overlapping_ground_truth=False
        )

        self.assertEqual(properties.nodes_lcc, 0)
        self.assertEqual(properties.edges_lcc, 0)
        self.assertIsNone(properties.min_degree)
        self.assertIsNone(properties.max_degree)
        self.assertIsNone(properties.average_degree)
        self.assertEqual(properties.degree_std, 0.0)
        self.assertIsNone(properties.degree_cv)
        self.assertIsNone(properties.degree_hub_ratio)
        self.assertIsNone(properties.degree_assortativity)
        self.assertEqual(properties.density, 0.0)
        self.assertEqual(properties.sparsity, 1.0)
        self.assertIsNone(properties.global_clustering_coefficient)
        self.assertIsNone(properties.average_clustering)

    def test_compute_network_properties_does_not_modify_graph(self):
        graph = nx.Graph()
        graph.add_nodes_from([10, 20, 30])
        graph.add_edges_from([(10, 20), (20, 30)])
        original_nodes = list(graph.nodes(data=True))
        original_edges = list(graph.edges(data=True))

        compute_network_properties(
            network_name="network",
            graph=graph,
            ground_truth=True,
            overlapping_ground_truth=True
        )

        self.assertEqual(list(graph.nodes(data=True)), original_nodes)
        self.assertEqual(list(graph.edges(data=True)), original_edges)

    def test_headers(self):
        self.assertEqual(
            NetworkProperties.headers(),
            [
                "Network",
                "Nodes LCC",
                "Edges LCC",
                "Min Degree",
                "Max Degree",
                "Average Degree",
                "Degree Std",
                "Degree CV",
                "Degree Hub Ratio",
                "Degree Assortativity",
                "Density",
                "Sparsity",
                "Global Clustering Coefficient",
                "Average Clustering",
                "Ground-Truth?",
                "Overlapping Ground-Truth?"
            ]
        )

    def test_to_dict(self):
        properties = NetworkProperties(
            network="network",
            nodes_lcc=4,
            edges_lcc=3,
            min_degree=1.0,
            max_degree=2.0,
            average_degree=1.5,
            degree_std=0.5,
            degree_cv=1.0 / 3.0,
            degree_hub_ratio=4.0 / 3.0,
            degree_assortativity=-0.5,
            density=0.5,
            sparsity=0.5,
            global_clustering_coefficient=0.0,
            average_clustering=0.0,
            ground_truth=True,
            overlapping_ground_truth=False
        )

        self.assertEqual(
            properties.to_dict(),
            {
                "Network": "network",
                "Nodes LCC": 4,
                "Edges LCC": 3,
                "Min Degree": 1.0,
                "Max Degree": 2.0,
                "Average Degree": 1.5,
                "Degree Std": 0.5,
                "Degree CV": 1.0 / 3.0,
                "Degree Hub Ratio": 4.0 / 3.0,
                "Degree Assortativity": -0.5,
                "Density": 0.5,
                "Sparsity": 0.5,
                "Global Clustering Coefficient": 0.0,
                "Average Clustering": 0.0,
                "Ground-Truth?": True,
                "Overlapping Ground-Truth?": False
            }
        )

    def test_headers_match_to_dict_keys(self):
        properties = compute_network_properties(
            network_name="path",
            graph=nx.path_graph(4),
            ground_truth=True,
            overlapping_ground_truth=False
        )

        self.assertEqual(
            list(properties.to_dict().keys()),
            NetworkProperties.headers()
        )


if __name__ == "__main__":
    unittest.main()
