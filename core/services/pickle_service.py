from pandas import DataFrame
from xgboost import XGBClassifier
from core.schemes.pickled_data import DatasetModelMonoObject
from core.validators import DatasetValidator, ModelValidator
from core.services.pickle_writer import PickleWriter
from core.services.pickle_reader import PickleReader
from app.constants import MODEL_LOAD_ERROR, DATASET_LOAD_ERROR_MESSAGE


class PickleService:
    def __init__(self):
        self.__reader = PickleReader()
        self.__writer = PickleWriter()

        self.__model_validator = ModelValidator()
        self.__dataset_validator = DatasetValidator()

    def get_dataset(self, path: str) -> DataFrame:
        obj = self.__reader.read_pickled(path)

        if not self.__dataset_validator.is_valid(obj):
            raise Exception(DATASET_LOAD_ERROR_MESSAGE)

        return obj

    def get_model(self, path: str) -> XGBClassifier:
        obj: XGBClassifier = self.__reader.read_pickled(path)

        if not self.__model_validator.is_valid(obj):
            raise Exception(MODEL_LOAD_ERROR)

        return obj  # type: ignore

    def get_dataset_and_model(self, path: str) -> DatasetModelMonoObject:
        obj: tuple[XGBClassifier, DataFrame] = self.__reader.read_pickled(path)

        if not self.__dataset_validator.is_valid(obj[1]):
            raise Exception(DATASET_LOAD_ERROR_MESSAGE)

        if not self.__model_validator.is_valid(obj[0]):
            raise Exception(DATASET_LOAD_ERROR_MESSAGE)

        return DatasetModelMonoObject(dataset=obj[1], model=obj[0])

    def save_dataset_and_model(
        self, dataset_and_model: DatasetModelMonoObject, path: str
    ) -> None:
        self.__writer.write_pickled(
            [dataset_and_model.model, dataset_and_model.dataset], path
        )
