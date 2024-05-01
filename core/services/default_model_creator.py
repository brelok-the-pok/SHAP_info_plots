from enum import Enum
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.neural_network import MLPClassifier
from typing import Union


class DefaultModelType(Enum):
    FOREST = (
        RandomForestClassifier,
        {
            "n_estimators": 40,
            "random_state": 42,
            "criterion": "gini",
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "min_weight_fraction_leaf": 0.0,
            "max_features": "sqrt",
        },
    )
    XGBOOST = (
        XGBClassifier,
        {
            "n_estimators": 100,
            "random_state": 42,
            "criterion": "gini",
            "max_depth": None,
            "min_samples_split": 2,
            "min_samples_leaf": 1,
            "min_weight_fraction_leaf": 0.0,
            "max_features": "sqrt",
        },
    )
    MLP = (
        MLPClassifier,
        {
            "hidden_layer_sizes": (100,),
            "activation": "relu",
            "solver": "lbfgs",
            "alpha": 1e-5,
            "batch_size": "auto",
        },
    )


class DefaultModelCreator:
    def __init__(
        self,
        model_type: DefaultModelType,
    ) -> None:
        self._model_class = model_type.value[0]
        self._model_params = model_type.value[1]

        self._model_fitted = False

    def fit_model(
        self, X: pd.DataFrame, y: pd.DataFrame
    ) -> Union[RandomForestClassifier, XGBClassifier, MLPClassifier]:
        model = self._init_model()
        fitted_model = self._fit_model(model, X, y)
        self._model = fitted_model
        return fitted_model

    def get_model_accuracy(self):
        if self._model_fitted:
            return {
                "train": self._model.score(self._X_train, self._y_train),
                "test": self._model.score(self._X_test, self._y_test),
            }

    def _init_model(self):
        model = self._model_class(**self._model_params)
        return model

    def _fit_model(self, model, X, y):
        self._X_train, self._X_test, self._y_train, self._y_test = (
            self._get_splited_dataset(X, y)
        )
        fitted_model = model.fit(self._X_train, self._y_train)
        self._model_fitted = True
        return fitted_model

    @staticmethod
    def _get_splited_dataset(X, y):
        return train_test_split(X, y, test_size=0.15, random_state=42)
