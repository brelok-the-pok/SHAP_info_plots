from typing import Any
from xgboost import XGBClassifier
from core.validators.base_validator import BaseValidator


class ModelValidator(BaseValidator):
    @staticmethod
    def is_valid(obj: Any) -> bool:
        return isinstance(obj, XGBClassifier)
