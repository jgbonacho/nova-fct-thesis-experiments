import unittest
from dataclasses import dataclass, field
from enum import Enum

from experiments.scripts.real_world_networks.utils.csv_dataclass import CsvDataclass


class ExampleStatus(str, Enum):
    READY = "ready"
    FAILED = "failed"


@dataclass
class NestedResults(CsvDataclass):
    score: float = field(metadata={"label": "Score"})
    accepted: bool = field(metadata={"label": "Accepted?"})
    internal_note: str = ""


@dataclass
class ExampleRecord(CsvDataclass):
    name: str = field(metadata={"label": "Name"})
    status: ExampleStatus = field(metadata={"label": "Status"})
    nested_results: NestedResults = None
    ignored_value: int = 0


class TestCsvDataclass(unittest.TestCase):

    def test_fieldnames_returns_labeled_fields_in_definition_order(self):
        self.assertEqual(
            ExampleRecord.fieldnames(),
            ["Name", "Status"]
        )

    def test_fieldnames_ignores_fields_without_label_metadata(self):
        self.assertEqual(
            NestedResults.fieldnames(),
            ["Score", "Accepted?"]
        )

    def test_to_dict_converts_labeled_fields(self):
        record = ExampleRecord(
            name="network_a",
            status=ExampleStatus.READY
        )

        self.assertEqual(
            record.to_dict(),
            {
                "Name": "network_a",
                "Status": "ready"
            }
        )

    def test_to_dict_flattens_nested_csv_dataclass(self):
        record = ExampleRecord(
            name="network_a",
            status=ExampleStatus.READY,
            nested_results=NestedResults(
                score=0.85,
                accepted=True,
                internal_note="not exported"
            )
        )

        self.assertEqual(
            record.to_dict(),
            {
                "Name": "network_a",
                "Status": "ready",
                "Score": 0.85,
                "Accepted?": True
            }
        )

    def test_to_dict_ignores_unlabeled_fields(self):
        nested_results = NestedResults(
            score=0.5,
            accepted=False,
            internal_note="private"
        )

        self.assertNotIn("internal_note", nested_results.to_dict())
        self.assertNotIn("private", nested_results.to_dict().values())

    def test_to_dict_omits_none_nested_field_without_label(self):
        record = ExampleRecord(
            name="network_a",
            status=ExampleStatus.FAILED,
            nested_results=None
        )

        self.assertEqual(
            record.to_dict(),
            {
                "Name": "network_a",
                "Status": "failed"
            }
        )


if __name__ == "__main__":
    unittest.main()
