import pickle
from typing import Any


class PickleReader:
    @staticmethod
    def read_pickled(path: str) -> Any:
        try:
            file = pickle.load(open(path, "rb"))
        except Exception:
            raise Exception("Объект по указаному пути не найден")

        return file
