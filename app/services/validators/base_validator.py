from abc import ABC, abstractmethod
from typing import Any


class BaseValidator(ABC):
    @staticmethod
    @abstractmethod
    def is_valid(obj: Any) -> bool:
        ...
