import shap
from sklearn.tree import DecisionTreeRegressor, plot_tree, _tree
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import xgboost
import numpy as np
from sklearn import preprocessing


class SimpleTreeModelFitter:
    def __init__(self, model, dataset, depth):
        self.model = model
        self.dataset = dataset
        self.depth = depth

    def get_simple_tree(self) -> DecisionTreeRegressor:
        y_proba = self.get_y_proba_for_tree()
        clf = self.fit_decision_tree(y_proba)

        return clf

    def get_y_proba_for_tree(self) -> list[float]:
        X = self.get_X()

        return self.model.predict_proba(X)[:, 1]

    def get_X(self):
        return self.dataset.drop("survived", axis=1)

    def get_y(self):
        return self.dataset["survived"]

    def fit_decision_tree(self, y) -> DecisionTreeRegressor:
        clf = DecisionTreeRegressor(max_depth=self.depth)
        X = self.get_X()
        clf = clf.fit(X, y)

        return clf
