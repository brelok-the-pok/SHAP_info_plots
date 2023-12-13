from typing import Any
from xgboost import XGBClassifier


class ModelValidator:
    @staticmethod
    def is_valid(model: Any) -> bool:
        return isinstance(model, XGBClassifier)
