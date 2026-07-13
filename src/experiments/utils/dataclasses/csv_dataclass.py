from dataclasses import fields, is_dataclass
from enum import Enum


class CsvDataclass:

    @classmethod
    def fieldnames(cls) -> list[str]:
        return [
            dataclass_field.metadata["label"]
            for dataclass_field in fields(cls)
            if "label" in dataclass_field.metadata
        ]

    def to_dict(self) -> dict:
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
