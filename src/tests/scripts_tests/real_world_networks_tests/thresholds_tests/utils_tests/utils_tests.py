import csv
import json
import os
import unittest
from dataclasses import dataclass
from enum import Enum
from tempfile import TemporaryDirectory
from unittest.mock import Mock, patch

import networkx as nx
import numpy as np

from experiments.scripts.real_world_networks.thresholds.utils import utils as utils_module


class CandidateThresholdStub:

    def __init__(self, values: dict):
        self.values = values

    def to_dict(self) -> dict:
        return self.values.copy()


class AffinityDesignStub:

    def __init__(self, output: np.ndarray):
        self.output = output
        self.calls = []

    def apply_affinity_design(self, A: np.ndarray) -> np.ndarray:
        self.calls.append(A)
        return self.output


class DummyAffinityDesign(str, Enum):
    DICE = "Dice"


@dataclass
class DummyConfig:
    affinity_design: DummyAffinityDesign
    apply_lapin: bool
    tau: float
    number_of_perturbed_graphs: int


class TestThresholdUtils(unittest.TestCase):

    @staticmethod
    def _read_csv(path: str) -> list[list[str]]:
        with open(path, mode="r", newline="", encoding="utf-8") as file:
            return list(csv.reader(file))

    def test_write_candidate_thresholds_to_file(self):
        candidate_thresholds = [
            CandidateThresholdStub(
                {
                    "Family": "family_01",
                    "Network": "network_a",
                    "Name": "e_family",
                    "Value": 0.10
                }
            ),
            CandidateThresholdStub(
                {
                    "Family": "family_01",
                    "Network": "network_a",
                    "Name": "e_global",
                    "Value": 0.15
                }
            )
        ]

        with TemporaryDirectory() as temporary_dir:
            output_file = os.path.join(
                temporary_dir,
                "candidate_thresholds.csv"
            )

            result = utils_module.write_candidate_thresholds_to_file(
                candidate_thresholds=candidate_thresholds,
                output_file=output_file,
                output_fieldnames=[
                    "Family",
                    "Network",
                    "Name",
                    "Value"
                ]
            )

            rows = self._read_csv(output_file)

        self.assertIsNone(result)
        self.assertEqual(
            rows,
            [
                ["Family", "Network", "Name", "Value"],
                ["family_01", "network_a", "e_family", "0.1"],
                ["family_01", "network_a", "e_global", "0.15"]
            ]
        )

    def test_write_candidate_thresholds_to_file_with_empty_list(self):
        with TemporaryDirectory() as temporary_dir:
            output_file = os.path.join(
                temporary_dir,
                "candidate_thresholds.csv"
            )

            utils_module.write_candidate_thresholds_to_file(
                candidate_thresholds=[],
                output_file=output_file,
                output_fieldnames=["Name", "Value"]
            )

            rows = self._read_csv(output_file)

        self.assertEqual(rows, [["Name", "Value"]])

    def test_write_candidate_threshold_to_file_filters_and_orders_fields(self):
        candidate_threshold = CandidateThresholdStub(
            {
                "Value": 0.12,
                "Name": "e_family",
                "Network": "network_a",
                "Family": "family_01",
                "Ignored": "not written"
            }
        )

        with TemporaryDirectory() as temporary_dir:
            output_file = os.path.join(
                temporary_dir,
                "threshold.csv"
            )

            result = utils_module.write_candidate_threshold_to_file(
                candidate_threshold=candidate_threshold,
                output_file=output_file,
                output_fieldnames=["Network", "Name", "Value"]
            )

            rows = self._read_csv(output_file)

        self.assertIsNone(result)
        self.assertEqual(
            rows,
            [
                ["Network", "Name", "Value"],
                ["network_a", "e_family", "0.12"]
            ]
        )

    def test_write_candidate_threshold_to_file_writes_empty_missing_field(self):
        candidate_threshold = CandidateThresholdStub(
            {
                "Name": "e_family",
                "Value": 0.12
            }
        )

        with TemporaryDirectory() as temporary_dir:
            output_file = os.path.join(
                temporary_dir,
                "threshold.csv"
            )

            utils_module.write_candidate_threshold_to_file(
                candidate_threshold=candidate_threshold,
                output_file=output_file,
                output_fieldnames=["Network", "Name", "Value"]
            )

            rows = self._read_csv(output_file)

        self.assertEqual(
            rows,
            [
                ["Network", "Name", "Value"],
                ["", "e_family", "0.12"]
            ]
        )

    def test_generate_perturbed_graph_without_lapin(self):
        graph = nx.cycle_graph(4)
        original_edges = set(graph.edges())

        perturbed_A = np.array(
            [[0, 1, 0, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 0, 1, 0]],
            dtype=int
        )
        affinity_W = np.array(
            [[0, 0.5, 0, 0.5],
             [0.5, 0, 0.5, 0],
             [0, 0.5, 0, 0.5],
             [0.5, 0, 0.5, 0]],
            dtype=np.float32
        )
        affinity_design = AffinityDesignStub(affinity_W)

        with patch.object(
                utils_module,
                "connected_double_edge_swap",
                return_value=3
        ) as mocked_swap, patch.object(
            utils_module,
            "compute_adjacency_matrix",
            return_value=perturbed_A
        ) as mocked_compute_adjacency, patch.object(
            utils_module,
            "lapin"
        ) as mocked_lapin, patch(
            "builtins.print"
        ) as mocked_print:
            perturbed_graph, returned_A, returned_W = (
                utils_module.generate_a_perturbed_graph(
                    graph=graph,
                    number_of_swaps=5,
                    affinity_design=affinity_design,
                    apply_lapin=False,
                    seed=7
                )
            )

        self.assertIsNot(perturbed_graph, graph)
        self.assertEqual(set(graph.edges()), original_edges)

        swap_graph = mocked_swap.call_args.args[0]
        self.assertIs(swap_graph, perturbed_graph)
        mocked_swap.assert_called_once_with(
            perturbed_graph,
            nswap=5,
            seed=7
        )
        mocked_compute_adjacency.assert_called_once_with(
            perturbed_graph
        )
        self.assertEqual(len(affinity_design.calls), 1)
        self.assertIs(affinity_design.calls[0], perturbed_A)
        mocked_lapin.assert_not_called()
        mocked_print.assert_called_once_with(
            "[DEBUG] Successful swaps = 3/5"
        )

        self.assertIs(returned_A, perturbed_A)
        np.testing.assert_array_equal(returned_W, affinity_W)
        self.assertEqual(returned_W.dtype, np.float64)

    def test_generate_perturbed_graph_with_lapin(self):
        graph = nx.cycle_graph(4)
        perturbed_A = np.eye(4)
        affinity_W = np.full((4, 4), 0.25)
        lapin_W = np.full((4, 4), 0.75, dtype=np.float32)
        affinity_design = AffinityDesignStub(affinity_W)

        with patch.object(
                utils_module,
                "connected_double_edge_swap",
                return_value=2
        ), patch.object(
            utils_module,
            "compute_adjacency_matrix",
            return_value=perturbed_A
        ), patch.object(
            utils_module,
            "lapin",
            return_value=lapin_W
        ) as mocked_lapin, patch(
            "builtins.print"
        ):
            _, returned_A, returned_W = (
                utils_module.generate_a_perturbed_graph(
                    graph=graph,
                    number_of_swaps=2,
                    affinity_design=affinity_design,
                    apply_lapin=True,
                    seed=10
                )
            )

        mocked_lapin.assert_called_once_with(affinity_W)
        self.assertIs(returned_A, perturbed_A)
        np.testing.assert_array_equal(returned_W, lapin_W)
        self.assertEqual(returned_W.dtype, np.float64)

    def test_generate_perturbed_graph_uses_modified_graph_for_adjacency(self):
        graph = nx.Graph(
            [
                (0, 1),
                (1, 2),
                (2, 3),
                (3, 0)
            ]
        )

        def fake_swap(perturbed_graph, nswap, seed):
            perturbed_graph.remove_edge(0, 1)
            perturbed_graph.add_edge(0, 2)
            return 1

        def fake_compute_adjacency(perturbed_graph):
            self.assertIn((0, 2), perturbed_graph.edges())
            self.assertNotIn((0, 1), perturbed_graph.edges())
            return np.asarray(
                nx.to_numpy_array(
                    perturbed_graph,
                    nodelist=sorted(perturbed_graph.nodes())
                )
            )

        affinity_design = Mock()
        affinity_design.apply_affinity_design.side_effect = (
            lambda A: A.copy()
        )

        with patch.object(
                utils_module,
                "connected_double_edge_swap",
                side_effect=fake_swap
        ), patch.object(
            utils_module,
            "compute_adjacency_matrix",
            side_effect=fake_compute_adjacency
        ), patch(
            "builtins.print"
        ):
            perturbed_graph, _, _ = (
                utils_module.generate_a_perturbed_graph(
                    graph=graph,
                    number_of_swaps=1,
                    affinity_design=affinity_design,
                    apply_lapin=False,
                    seed=1
                )
            )

        self.assertIn((0, 2), perturbed_graph.edges())
        self.assertIn((0, 1), graph.edges())

    def test_save_contributions_experiment_report(self):
        config = DummyConfig(
            affinity_design=DummyAffinityDesign.DICE,
            apply_lapin=True,
            tau=0.05,
            number_of_perturbed_graphs=10
        )

        with TemporaryDirectory() as temporary_dir:
            output_file = os.path.join(
                temporary_dir,
                "report.json"
            )

            result = utils_module.save_contributions_experiment_report(
                results_dir=temporary_dir,
                output_filename="report.json",
                execution_elapsed_time=12.5,
                config=config
            )

            with open(
                    output_file,
                    mode="r",
                    encoding="utf-8"
            ) as file:
                report = json.load(file)

        self.assertIsNone(result)
        self.assertEqual(
            report,
            {
                "affinity_design": "Dice",
                "apply_lapin": True,
                "tau": 0.05,
                "number_of_perturbed_graphs": 10,
                "execution_elapsed_time_secs": 12.5
            }
        )

    def test_save_contributions_experiment_report_overwrites_file(self):
        config = DummyConfig(
            affinity_design=DummyAffinityDesign.DICE,
            apply_lapin=False,
            tau=0.1,
            number_of_perturbed_graphs=5
        )

        with TemporaryDirectory() as temporary_dir:
            output_file = os.path.join(
                temporary_dir,
                "report.json"
            )
            with open(
                    output_file,
                    mode="w",
                    encoding="utf-8"
            ) as file:
                json.dump({"old": "value"}, file)

            utils_module.save_contributions_experiment_report(
                results_dir=temporary_dir,
                output_filename="report.json",
                execution_elapsed_time=3.0,
                config=config
            )

            with open(
                    output_file,
                    mode="r",
                    encoding="utf-8"
            ) as file:
                report = json.load(file)

        self.assertNotIn("old", report)
        self.assertEqual(
            report["execution_elapsed_time_secs"],
            3.0
        )


if __name__ == "__main__":
    unittest.main()
