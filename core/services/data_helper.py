import numpy as np
from pandas import DataFrame


class DataHelper:
    @staticmethod
    def get_dataset_min_max(dataset: DataFrame):
        array = np.array(dataset)
        return [np.amin(array, axis=0), np.amax(array, axis=0)]

    @staticmethod
    def find_category_columns(dataset: DataFrame):
        categorical = []

        for col in dataset.columns:
            if len(dataset[col].unique()) < 10:
                categorical.append(col)

        return categorical
