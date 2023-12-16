import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap

from constants import COLORS


def find_category_columns(data):
    data_copy = data.copy()
    categorical = []

    for col in data_copy.columns:
        if len(data_copy[col].unique()) < 10:
            categorical.append(col)
    return categorical


def getMinMax(data):
    data_copy = data.copy()
    ar = np.array(data_copy)
    minMax = [np.amin(ar, axis=0), np.amax(ar, axis=0)]
    return minMax


def top5_centered_importance(explainer, data, col_name):
    data_copy = data.copy()

    col_vals = create_variable_list(data[col_name])
    res_vals = []

    for val in col_vals:
        new_col = len(data_copy[col_name]) * [val]
        data_copy[col_name] = new_col
        shap_values = explainer.shap_values(
            data_copy.drop("Survived", axis=1), y=data_copy["Survived"]
        )
        res_vals.append(shap_values)

    return res_vals, col_vals


def top5_find_by_importance(explainer, data):
    shap_values = explainer.shap_values(
        data.drop("Survived", axis=1), y=data["Survived"]
    )

    col_names = []
    indexes = []
    mean_importance = list(np.mean(np.absolute(shap_values), axis=0))

    max_list = sorted(mean_importance)[-5:]
    for max_val in max_list:
        indexes.append(mean_importance.index(max_val))
        col_names.append(data.columns[mean_importance.index(max_val)])

    return col_names, indexes


def plot_top5_centered_importance(model, data, col_name, absolute=False):
    plot = plt.axes()
    plot.figure.set_size_inches(16, 8)

    if absolute:
        title = "Центрированный график изменения абсолютной важности переменных"
    else:
        title = "Центрированный график изменения важности переменных"
    plot.set_title(title, fontsize=18)

    explainer = shap.TreeExplainer(model)

    data_copy = data.copy()

    cols, indexes = top5_find_by_importance(explainer, data_copy)

    res_vals, col_vals = top5_centered_importance(explainer, data_copy, col_name)

    res_vals = np.array(res_vals)

    for i in range(0, len(indexes)):
        res = []

        for j in range(0, len(res_vals)):
            val = res_vals[j, :, indexes[i]]
            if absolute:
                val = np.absolute(val)
            res.append(val.mean())

        plot.plot(col_vals, res, color=COLORS[i], linewidth=4, label=cols[i])

    plot.grid()
    plot.set_xlabel(col_name, fontsize=16)
    plot.set_ylabel("Важность переменных", fontsize=16)
    plot.legend()

    return plot


def ice_plot_data_y(model, data, col_name):
    data_copy = data.copy()

    col_vals = create_variable_list(data[col_name])
    res_vals = []

    for val in col_vals:
        new_col = len(data_copy[col_name]) * [val]
        data_copy[col_name] = new_col
        predict = model.predict_proba(data_copy.drop("Survived", axis=1))[:, 1]
        res_vals.append(predict)

    return res_vals, col_vals


def create_variable_list(col):
    min_val = col.min()
    max_val = col.max()

    unique = col.unique()

    if len(unique) < 50:
        col_vals = sorted(list(unique))
    else:
        delta = (max_val - min_val) / 100
        col_vals = []
        while min_val <= max_val:
            col_vals.append(min_val)
            min_val += delta
    return col_vals


def ice_plot_data_importance(explainer, data, col_name):
    data_copy = data.copy()

    col_vals = create_variable_list(data[col_name])
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


def plot_ice_plot(model, data, col_name, importance=False):
    plot = plt.axes()

    if importance:
        explainer = shap.TreeExplainer(model)
        res_vals, col_vals = ice_plot_data_importance(explainer, data, col_name)
        y_label = f"Важность переменной {col_name}"
        title = f"с-ICE график изменения важности переменной {col_name}"
    else:
        res_vals, col_vals = ice_plot_data_y(model, data, col_name)
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

    return plot
