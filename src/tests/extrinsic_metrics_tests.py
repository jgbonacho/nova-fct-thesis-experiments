import unittest

import networkx as nx

from experiments.evaluation_metrics.extrinsic.extrinsic_metrics_for_overlapping_ground_truth import \
    compute_extrinsic_metrics_for_overlapping_ground_truth


class Test(unittest.TestCase):

    def test_extrinsic_metrics_for_overlapping_ground_truth(self):
        graph = nx.Graph()
        graph.add_node(0)
        graph.add_node(1)
        graph.add_node(2)
        graph.add_node(3)

        results = compute_extrinsic_metrics_for_overlapping_ground_truth(
            graph=graph,
            ground_truth_labels=[[0], [0, 1], [1], [1]],
            predicted_labels=[[1], [1, 2], [2], [2]],
            k=2,
            k_predicted=2,
        )

        self.assertEqual(results.get("ONMI"), 1.0)
        self.assertEqual(results.get("Omega"), 1.0)
        self.assertEqual(results.get("|K'-K|/K"), 0.0)


if __name__ == "__main__":
    unittest.main()
