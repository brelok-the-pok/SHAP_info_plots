import tempfile
from typing import Any

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from pandas import DataFrame
from app.constants import PLOT_HEIGHT, PLOT_WIDTH, TOP5_CENTERED_IMPORTANCE_TITLE
from xgboost import XGBClassifier
import shap
from app.services.model_explainer import ModelExplainer


class PlotCreator:
    def __init__(
        self,
        model: XGBClassifier,
        dataset: DataFrame,
        column: str,
        min_value: float,
        max_value: float,
    ):
        cond1 = dataset[column] >= min_value
        cond2 = dataset[column] <= max_value

        self.__model = model
        self.__dataset = dataset[cond1 & cond2].reset_index(drop=True)
        self.__column = column
        self.__temp_dir = tempfile.TemporaryDirectory()

        self.__default_height = PLOT_HEIGHT
        self.__default_width = PLOT_WIDTH

    def plot_category_plots(self, category_column: str) -> list[list[str]]:
        categories = sorted(list(self.__dataset[category_column].unique()))

        if not categories:
            raise Exception("Категории не найдены")

        fig_paths: list[list[str]] = []

        for category in categories:
            dataset = self.__get_category_dataset(category_column, category)

            paths = self.__make_plots_for_dataset(
                dataset, f"{self.__column} - {category_column} - {category}"
            )
            fig_paths.append(paths)

        return fig_paths

    def plot_regular_plots(self) -> list[str]:
        return self.__make_plots_for_dataset(self.__dataset, f"{self.__column}")

    def __make_plots_for_dataset(self, dataset: DataFrame, fig_name: str) -> list[str]:
        fig_lt = self.__get_top5_centered_importance_plot(dataset, True)
        self.__set_fig_settings(fig_lt)
        lt_path = self.__save_fig(fig_lt, f"lt-{fig_name}")

        fig_lb = self.__get_ice_plot(self.__model, dataset, True)
        self.__set_fig_settings(fig_lb)
        lb_path = self.__save_fig(fig_lb, f"lb-{fig_name}")

        fig_rt = self.__get_top5_centered_importance_plot(dataset, False)
        self.__set_fig_settings(fig_rt)
        rt_path = self.__save_fig(fig_rt, f"rt-{fig_name}")

        fig_rb = self.__get_ice_plot(self.__model, dataset, False)
        self.__set_fig_settings(fig_rb)
        rb_path = self.__save_fig(fig_rb, f"rb-{fig_name}")

        return [lt_path, lb_path, rt_path, rb_path]

    def __set_fig_settings(self, fig: Any) -> None:
        fig.set_size_inches(self.__default_width, self.__default_height)

    def __save_fig(self, fig: Any, fig_name: str) -> str:
        path = self.__temp_dir.name + f"\\{fig_name}.svg"

        fig.savefig(f"{path}.svg", bbox_inches="tight")
        fig.savefig(
            f"{path}.png",
            bbox_inches="tight",
            format="png",
        )

        return f"{path}.svg"

    def __get_category_dataset(self, category_column: str, category: str) -> DataFrame:
        cond = self.__dataset[category_column] == category

        return self.__dataset[cond].reset_index(drop=True)

    def __get_top5_centered_importance_plot(self, dataset, absolute=False):
        column = self.__column

        plt.figure(1, figsize=(1000, 1000), dpi=1)
        plt.clf()
        plot = plt.axes()
        plot.figure.set_size_inches(PLOT_WIDTH, PLOT_HEIGHT)
        plot.set_title(TOP5_CENTERED_IMPORTANCE_TITLE, fontsize=18)

        explainer = ModelExplainer(self.__model)
        columns = explainer.get_n_most_important_columns(dataset, 5)
        res_vals, col_vals = explainer.get_column_centered_importance(dataset, column)

        res_vals = np.array(res_vals)

        for i in range(0, len(indexes)):
            res = []

            for j in range(0, len(res_vals)):
                val = res_vals[j, :, indexes[i]]
                if absolute:
                    val = np.absolute(val)
                res.append(val.mean())

            plot.plot(col_vals, res, color=colors[i], linewidth=4, label=cols[i])

        plot.grid()
        plot.set_xlabel(col_name, fontsize=16)
        plot.set_ylabel("Важность переменных", fontsize=16)
        plot.legend()

        return plot.get_figure()

    def __get_ice_plot(self, model, data, importance=False):
        col_name = self.__column

        plt.figure(1, figsize=(1000, 1000), dpi=1)
        plt.clf()
        plot = plt.axes()

        if importance:
            explainer = shap.TreeExplainer(model)
            res_vals, col_vals = __ice_plot_data_importance(explainer, data, col_name)
            y_label = f"Важность переменной {col_name}"
            title = f"с-ICE график изменения важности переменной {col_name}"
        else:
            res_vals, col_vals = self.__ice_plot_data_y(model, data, col_name)
            y_label = "Вероятность удачного исхода"
            title = f"с-ICE график вероятности удачного исхода при изменении переменной {col_name}"

        df = pd.DataFrame(np.array(res_vals))
        df = df.T
        mean = df.mean()

        plot.figure.set_size_inches(16, 8)
        plot.set_title(title, fontsize=18)

        for i in df.index:
            plot.plot(col_vals, df.loc[i], color="black", linewidth=0.1)

        plot.plot(col_vals, mean, color="lime", linewidth=6)

        plot.grid()
        plot.set_xlabel(col_name, fontsize=16)
        plot.set_ylabel(y_label, fontsize=16)

        return plot.get_figure()
