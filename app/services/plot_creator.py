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
from app.constants import (
    COLORS,
    FONT_SIZE,
    FIG_SIZE,
    DPI,
    FIG_COUNT,
    ICE_PREDICTIONS_TITLE,
    ICE_PREDICTIONS_Y_LABEL,
    ICE_IMPORTANCE_TITLE,
    ICE_IMPORTANCE_Y_LABEL,
)


class PlotCreator:
    def __init__(
        self,
        model: XGBClassifier,
        dataset: DataFrame,
        column: str,
        min_value: float,
        max_value: float,
        temp_dir: tempfile.TemporaryDirectory,
    ):
        cond1 = dataset[column] >= min_value
        cond2 = dataset[column] <= max_value

        self.__model = model
        self.__explainer = ModelExplainer(self.__model)
        self.__dataset = dataset[cond1 & cond2].reset_index(drop=True)
        self.__column = column
        self.__temp_dir = temp_dir

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
        self.__explainer.calculate_for_dataset(dataset, self.__column)

        fig_lt = self.__get_top5_centered_importance_plot(False)
        self.__set_fig_settings(fig_lt)
        lt_path = self.__save_fig(fig_lt, f"lt-{fig_name}")

        fig_lb = self.__get_ice_predictions_plot()
        self.__set_fig_settings(fig_lb)
        lb_path = self.__save_fig(fig_lb, f"lb-{fig_name}")

        fig_rt = self.__get_top5_centered_importance_plot(True)
        self.__set_fig_settings(fig_rt)
        rt_path = self.__save_fig(fig_rt, f"rt-{fig_name}")

        fig_rb = self.__get_ice_importance_plot()
        self.__set_fig_settings(fig_rb)
        rb_path = self.__save_fig(fig_rb, f"rb-{fig_name}")

        return [lt_path, lb_path, rt_path, rb_path]

    def __set_fig_settings(self, fig: Any) -> None:
        fig.set_size_inches(self.__default_width, self.__default_height)

    def __save_fig(self, fig: Any, fig_name: str) -> str:
        path = self.__temp_dir.name + f"\\{fig_name}"

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

    def __get_top5_centered_importance_plot(self, absolute=False):
        plot = self.__get_empty_plot(TOP5_CENTERED_IMPORTANCE_TITLE)

        columns = self.__explainer.get_n_most_important_columns(5)
        indexes = [column.index for column in columns]
        importances = self.__explainer.get_centered_importance()

        mean_values = []
        for importance in importances.values():
            values = importance[:, indexes]

            if absolute:
                values = np.absolute(values)

            mean_values.append(values.mean(axis=0))

        for index, column in enumerate(columns):
            plot.plot(
                list(importances.keys()),
                [x[index] for x in mean_values],
                color=COLORS[index],
                linewidth=4,
                label=column.name,
            )

        self.__set_plot_settings(plot, self.__column, "Важность переменных")
        plot.legend()

        return plot.get_figure()

    def __get_empty_plot(self, title: str):
        plt.figure(FIG_COUNT, figsize=FIG_SIZE, dpi=DPI)
        plt.clf()
        plot = plt.axes()
        plot.set_title(title, fontsize=FONT_SIZE)

        return plot

    def __set_plot_settings(self, plot: Any, x_label: str, y_label: str):
        plot.grid()
        plot.set_xlabel(x_label, fontsize=FONT_SIZE)
        plot.set_ylabel(y_label, fontsize=FONT_SIZE)

    def __get_ice_importance_plot(self):
        title = ICE_IMPORTANCE_TITLE.format(self.__column)
        y_label = ICE_IMPORTANCE_Y_LABEL.format(self.__column)
        importance = self.__explainer.get_ice_importance()

        return self.__plot_ice_plot(importance, title, y_label)

    def __get_ice_predictions_plot(self):
        title = ICE_PREDICTIONS_TITLE.format(self.__column)
        y_label = ICE_PREDICTIONS_TITLE.format(self.__column)
        predictions = self.__explainer.get_ice_predictions()

        return self.__plot_ice_plot(predictions, title, y_label)

    def __plot_ice_plot(self, data: DataFrame, title: str, y_label: str):
        plot = self.__get_empty_plot(title)

        df = pd.DataFrame(data)

        for i in df.index:
            plot.plot(df.columns, df.loc[i], color="black", linewidth=0.1)

        plot.plot(df.columns, df.mean(), color="lime", linewidth=6)

        self.__set_plot_settings(plot, self.__column, y_label)

        return plot.get_figure()
