from typing import Any
from pandas import DataFrame
from app.services.validators.base_validator import BaseValidator


class DatasetValidator(BaseValidator):
    def is_valid(self, obj: Any) -> bool:
        return isinstance(obj, DataFrame)
