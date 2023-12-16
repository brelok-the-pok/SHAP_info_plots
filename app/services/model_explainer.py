from xgboost import XGBClassifier
import shap
from pandas import DataFrame, Series
import numpy as np
from app.schemes.model_explainer import MostImportantColumns


class ModelExplainer:
    def __init__(self, model: XGBClassifier) -> None:
        self.__explainer = shap.TreeExplainer(model)

    def get_n_most_important_columns(
        self, dataset: DataFrame, n: int
    ) -> list[MostImportantColumns]:
        shap_values = self.__explainer.shap_values(
            dataset.drop("Survived", axis=1), y=dataset["Survived"]
        )

        columns = []
        mean_importance = list(np.mean(np.absolute(shap_values), axis=0))

        for importance in sorted(mean_importance)[-n:]:
            index = mean_importance.index(importance)
            columns.append(
                MostImportantColumns(index=index, name=dataset.columns[index])
            )

        return columns

    def get_column_centered_importance(self, dataset: DataFrame, column: str):
        dataset_copy = dataset.copy()

        column_values = self.create_variable_list(dataset_copy[column])
        res_vals = []

        for value in column_values:
            dataset_copy[column] = len(dataset_copy[column]) * [value]
            shap_values = self.get_shap_values(dataset_copy)
            res_vals.append(shap_values)

        return res_vals, column_values

    def get_shap_values(self, dataset: DataFrame):
        return self.__explainer.shap_values(
            dataset.drop("Survived", axis=1), y=dataset["Survived"]
        )

    def create_variable_list(self, column: Series):
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

        return col_vals

    def __ice_plot_data_importance(self, explainer, data, col_name):
        data_copy = data.copy()

        col_vals = self.create_variable_list(data[col_name])
        res_vals = []

        for val in col_vals:
            new_col = len(data_copy[col_name]) * [val]
            data_copy[col_name] = new_col

            shap_values = explainer.shap_values(
                data_copy.drop("Survived", axis=1), y=data_copy["Survived"]
            )
            shap_values = np.array(shap_values)

            res_vals.append(shap_values[:, list(data.columns).index(col_name)])

        return res_vals, col_vals

    def __ice_plot_data_y(self, model, data, col_name):
        data_copy = data.copy()

        col_vals = self.create_variable_list(data[col_name])
        res_vals = []

        for val in col_vals:
            new_col = len(data_copy[col_name]) * [val]
            data_copy[col_name] = new_col
            predict = model.predict_proba(data_copy.drop("Survived", axis=1))[:, 1]
            res_vals.append(predict)

        return res_vals, col_vals
