from typing import Any
from pandas import DataFrame


class DatasetValidator:
    @staticmethod
    def is_valid(dataset: Any) -> bool:
        return isinstance(dataset, DataFrame)
