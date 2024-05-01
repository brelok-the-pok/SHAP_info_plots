import seaborn as sns
from pandas import DataFrame


class DefaultDatasetCreator:
    def __init__(self) -> None:
        self.dataset = self._get_default_dataset()
        self.X = self.dataset.drop("survived", axis=1)
        self.y = self.dataset["survived"]

    def get_dataset(self) -> DataFrame:
        return self.dataset

    def get_X(self):
        return self.X

    def get_y(self):
        return self.y

    def _get_default_dataset(self):
        dataset = self._get_original_dataset()
        dataset = self._drop_extra_fields(dataset)
        dataset = self._fill_missing_values(dataset)
        dataset = self._map_not_numeric_feature(dataset)

        return dataset

    @staticmethod
    def _get_original_dataset():
        dataset = sns.load_dataset("titanic")

        return dataset

    @staticmethod
    def _drop_extra_fields(dataset):
        dataset = dataset.drop("embark_town", axis=1)
        dataset = dataset.drop("alive", axis=1)
        dataset = dataset.drop("who", axis=1)
        dataset = dataset.drop("pclass", axis=1)
        dataset = dataset.drop("deck", axis=1)
        dataset = dataset.drop("parch", axis=1)
        dataset = dataset.drop("adult_male", axis=1)

        return dataset

    @staticmethod
    def _fill_missing_values(dataset):
        dataset["age"] = dataset["age"].fillna(dataset["age"].mean())
        freq_port = dataset.embarked.dropna().mode()[0]
        dataset["embarked"] = dataset["embarked"].fillna(freq_port)

        return dataset

    @staticmethod
    def _map_not_numeric_feature(dataset):
        params = {
            "sex": {"female": 1, "male": 0},
            "class": {"Third": 3, "Second": 2, "First": 1},
            "alone": {True: 1, False: 0},
            # "adult_male": {True: 1, False: 0},
            "embarked": {"S": 0, "C": 1, "Q": 2},
        }
        dataset["sex"] = dataset["sex"].map(params["sex"]).astype(int)
        dataset["class"] = dataset["class"].map(params["class"]).astype(int)
        dataset["alone"] = dataset["alone"].map(params["alone"]).astype(int)
        # dataset["adult_male"] = (
        #     dataset["adult_male"].map(params["adult_male"]).astype(int)
        # )
        dataset["embarked"] = dataset["embarked"].map(params["embarked"]).astype(int)

        return dataset
