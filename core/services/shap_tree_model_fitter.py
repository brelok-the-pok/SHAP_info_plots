import shap
from sklearn.tree import DecisionTreeRegressor, plot_tree, _tree
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import xgboost
import numpy as np
from sklearn import preprocessing


class ShapTreeModelFitter:
    def __init__(self, model, dataset, depth):
        self.model = model
        self.dataset = dataset
        self.depth = depth

    def get_simple_tree(self) -> DecisionTreeRegressor:
        y_proba = self.get_y_proba_for_tree()
        clf = self.fit_decision_tree(y_proba)

        return clf

    def get_y_proba_for_tree(self) -> list[float]:
        return self.model.predict_proba(self.get_X())[:, 1]

    def get_X(self):
        return self.dataset.drop("survived", axis=1)

    def get_y(self):
        return self.dataset["survived"]

    def fit_decision_tree(self, y) -> DecisionTreeRegressor:
        clf = DecisionTreeRegressor(max_depth=self.depth)
        clf = clf.fit(self.get_X(), y)

        return clf

    def get_shap_values_for_tree(model, X, y):
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X, y=y)
        return shap_values

    def get_feature_index(self, feature_name, X):
        return list(X.columns).index(feature_name)

    def get_feature_shap_vals(self, shap_values, feature_index):
        return shap_values[:, feature_index]

    def plot_fig_for_tree(self, clf, feature_names):
        fig = plt.figure(figsize=(15, 5))
        _ = plot_tree(clf, filled=True, feature_names=feature_names)

    def get_decition_tree_for_feature(
        self, model, df, feature_name, depth, should_remove_original_feature=False
    ):
        X, y = self.get_cleaned_data_for_shap(df)
        shap_values = self.get_shap_values_for_tree(model, X, y)

        feature_index = self.get_feature_index(feature_name, X)
        feature_shap_vals = self.get_feature_shap_vals(shap_values, feature_index)
        if should_remove_original_feature:
            X = X.drop(feature_name, axis=1)

        clf = self.fit_decision_tree(X, feature_shap_vals, depth)

        self.plot_fig_for_tree(clf, X.columns)

    def get_decition_tree_text_for_feature(
        self, model, df, feature_name, depth, should_remove_original_feature=False
    ):
        X, y = self.get_cleaned_data_for_shap(df)
        shap_values = self.get_shap_values_for_tree(model, X, y)

        feature_index = self.get_feature_index(feature_name, X)
        feature_shap_vals = self.get_feature_shap_vals(shap_values, feature_index)

        if should_remove_original_feature:
            X = X.drop(feature_name, axis=1)

        clf = self.fit_decision_tree(X, feature_shap_vals, depth)

        return clf, X
