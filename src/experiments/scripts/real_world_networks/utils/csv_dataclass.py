from dataclasses import fields, is_dataclass
from enum import Enum


class CsvDataclass:
    """
    Base class for dataclasses that can be converted to CSV-compatible field names and dictionaries.
    """

    @classmethod
    def fieldnames(cls) -> list[str]:
        """
        Return the CSV field names defined in the dataclass field metadata.

        Returns:
            fieldnames : (list[str])
                Labels of all dataclass fields containing a "label" metadata entry.
        """

        return [
            dataclass_field.metadata["label"]
            for dataclass_field in fields(cls)
            if "label" in dataclass_field.metadata
        ]

    def to_dict(self) -> dict:
        """
        Convert the dataclass and its nested dataclasses into a flat dictionary.

        Returns:
            output : (dict)
                Dictionary mapping CSV field labels to their corresponding values. Nested dataclasses
                are flattened, and enumeration values are converted to their underlying values.
        """

        output = {}

        for dataclass_field in fields(self):
            value = getattr(self, dataclass_field.name)

            if is_dataclass(value):
                output.update(value.to_dict())

            elif "label" in dataclass_field.metadata:
                if isinstance(value, Enum):
                    value = value.value

                output[dataclass_field.metadata["label"]] = value

        return output
