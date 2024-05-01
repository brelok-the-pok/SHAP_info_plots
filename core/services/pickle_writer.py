import pickle
from typing import Any


class PickleWriter:
    @staticmethod
    def write_pickled(obj: Any, path: str) -> None:
        pickle.dump(obj, open(path, "wb"))
