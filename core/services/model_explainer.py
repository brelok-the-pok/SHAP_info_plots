from xgboost import XGBClassifier
import shap
from pandas import DataFrame, Series
import numpy as np

from core.schemes.model_explainer import MostImportantColumns


class ModelExplainer:
    def __init__(self, model: XGBClassifier) -> None:
        self._model = model
        self._explainer = shap.TreeExplainer(model)
        self._most_important_columns = []
        self._importance = {}
        self._predicts = {}

    def get_n_most_important_columns(self, n: int) -> list[MostImportantColumns]:
        return self._most_important_columns[:n]

    def get_centered_importance(self):
        return self._importance

    def get_ice_importance(self):
        column_index = list(self._dataset.columns).index(self._column_to_vary)

        return {
            key: shap_values[:, column_index]
            for key, shap_values in self._importance.items()
        }

    def get_ice_predictions(self):
        return self._predicts

    def calculate_for_dataset(self, dataset: DataFrame, column_to_vary: str) -> None:
        self._dataset = dataset
        self._column_to_vary = column_to_vary

        self._calculate_most_important_columns()
        self._calculate_importance()

    def _calculate_most_important_columns(self) -> None:
        shap_values = self._get_shap_values(self._dataset)

        columns = []
        mean_importance = list(np.mean(np.absolute(shap_values), axis=0))

        for importance in sorted(mean_importance, reverse=True):
            index = mean_importance.index(importance)
            columns.append(
                MostImportantColumns(index=index, name=self._dataset.columns[index])
            )

        self._most_important_columns = columns

    def _calculate_importance(self) -> None:
        dataset_copy = self._dataset.copy()
        column_to_vary = self._column_to_vary

        importance = {}
        predicts = {}

        dataset_len = dataset_copy[column_to_vary].count()

        for value in self._get_variables_to_vary(dataset_copy[column_to_vary]):
            dataset_copy[column_to_vary] = dataset_len * [value]

            shap_values = self._get_shap_values(dataset_copy)
            predict_values = self._get_predict_values(dataset_copy)

            importance[value] = shap_values
            predicts[value] = predict_values

        self._importance = importance
        self._predicts = predicts

    def _get_variables_to_vary(self, column: Series) -> list[float]:
        min_val = column.min()
        max_val = column.max()

        unique = column.unique()

        if len(unique) < 50:
            col_vals = sorted(list(unique))
        else:
            delta = (max_val - min_val) / 200
            col_vals = []

            while min_val <= max_val:
                col_vals.append(min_val)
                min_val += delta

        return list(col_vals)

    def _get_shap_values(self, dataset: DataFrame):
        X = dataset.drop("survived", axis=1)
        y = dataset["survived"]
        shap_values = self._explainer.shap_values(X, y=y)
        arr = np.array(shap_values)
        return arr

    def _get_predict_values(self, dataset: DataFrame):
        return np.array(
            self._model.predict_proba(dataset.drop("survived", axis=1))[:, 1]
        )
