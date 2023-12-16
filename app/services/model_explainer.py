from xgboost import XGBClassifier
import shap
from pandas import DataFrame, Series
import numpy as np
from app.schemes.model_explainer import MostImportantColumns


class ModelExplainer:
    def __init__(self, model: XGBClassifier) -> None:
        self.__model = model
        self.__explainer = shap.TreeExplainer(model)
        self.__most_important_columns = []
        self.__importance = {}
        self.__predicts = {}

    def get_n_most_important_columns(self, n: int) -> list[MostImportantColumns]:
        return self.__most_important_columns[:n]

    def get_centered_importance(self):
        return self.__importance

    def get_ice_importance(self):
        column_index = list(self.__dataset.columns).index(self.__column_to_vary)

        return {
            key: shap_values[:, column_index]
            for key, shap_values in self.__importance.items()
        }

    def get_ice_predictions(self):
        return self.__predicts

    def calculate_for_dataset(self, dataset: DataFrame, column_to_vary: str) -> None:
        self.__dataset = dataset
        self.__column_to_vary = column_to_vary

        self.__calculate_most_important_columns()
        self.__calculate_importance()

    def __calculate_most_important_columns(self) -> None:
        shap_values = self.__get_shap_values(self.__dataset)

        columns = []
        mean_importance = list(np.mean(np.absolute(shap_values), axis=0))

        for importance in sorted(mean_importance, reverse=True):
            index = mean_importance.index(importance)
            columns.append(
                MostImportantColumns(index=index, name=self.__dataset.columns[index])
            )

        self.__most_important_columns = columns

    def __calculate_importance(self) -> None:
        dataset_copy = self.__dataset.copy()
        column_to_vary = self.__column_to_vary

        importance = {}
        predicts = {}

        dataset_len = dataset_copy[column_to_vary].count()

        for value in self.__get_variables_to_vary(dataset_copy[column_to_vary]):
            dataset_copy[column_to_vary] = dataset_len * [value]

            shap_values = self.__get_shap_values(dataset_copy)
            predict_values = self.__get_predict_values(dataset_copy)

            importance[value] = shap_values
            predicts[value] = predict_values

        self.__importance = importance
        self.__predicts = predicts

    def __get_variables_to_vary(self, column: Series) -> list[float]:
        min_val = column.min()
        max_val = column.max()

        unique = column.unique()

        if len(unique) < 50:
            col_vals = sorted(list(unique))
        else:
            delta = (max_val - min_val) / 100
            col_vals = []

            while min_val <= max_val:
                col_vals.append(min_val)
                min_val += delta

        return list(col_vals)

    def __get_shap_values(self, dataset: DataFrame):
        return np.array(
            self.__explainer.shap_values(
                dataset.drop("Survived", axis=1), y=dataset["Survived"]
            )
        )

    def __get_predict_values(self, dataset: DataFrame):
        return np.array(
            self.__model.predict_proba(dataset.drop("Survived", axis=1))[:, 1]
        )
