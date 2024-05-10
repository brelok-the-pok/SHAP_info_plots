import shap
from sklearn.tree import DecisionTreeRegressor


class ShapTreeModelFitter:
    def __init__(self, model, dataset, depth, feature_name):
        self.model = model
        self.dataset = dataset
        self.depth = depth
        self.feature_name = feature_name

    def get_simple_tree(self) -> DecisionTreeRegressor:
        feature_shap_values = self._get_y_for_tree()
        clf = self._fit_decision_tree(feature_shap_values)

        return clf

    def get_category_tree(self, category_name) -> list[DecisionTreeRegressor]:
        category_values = sorted(list(self.dataset[category_name].unique()))

        original_dataset = self.dataset
        clf_s = []
        for value in category_values:
            cond = original_dataset[category_name] == value
            self.dataset = original_dataset[cond].reset_index(drop=True)
            clf_s.append(self.get_simple_tree())

        self.dataset = original_dataset

        return clf_s

    def _get_y_for_tree(self) -> list[float]:
        return self._get_feature_shap_vals()

    def _get_X(self):
        return self.dataset.drop("survived", axis=1)

    def _get_y(self):
        return self.dataset["survived"]

    def _get_feature_shap_vals(self):
        shap_values = self._get_shap_vals()
        feature_index = self._get_feature_index()

        return shap_values[:, feature_index]

    def _get_shap_vals(self):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(self._get_X(), y=self._get_y())
        return shap_values

    def _get_feature_index(self):
        return list(self._get_X().columns).index(self.feature_name)

    def _fit_decision_tree(self, y) -> DecisionTreeRegressor:
        clf = DecisionTreeRegressor(max_depth=self.depth)
        clf = clf.fit(self._get_X(), y)

        return clf

    def get_columns(self) -> list[str]:
        return list(self._get_X().columns)

    # def plot_fig_for_tree(self, clf, feature_names):
    #     fig = plt.figure(figsize=(15, 5))
    #     _ = plot_tree(clf, filled=True, feature_names=feature_names)
    #
    # def get_decition_tree_for_feature(
    #     self, model, df, feature_name, depth, should_remove_original_feature=False
    # ):
    #     X, y = self.get_cleaned_data_for_shap(df)
    #     shap_values = self.get_shap_values_for_tree(model, X, y)
    #
    #     feature_index = self.get_feature_index(feature_name, X)
    #     feature_shap_vals = self.get_feature_shap_vals(shap_values, feature_index)
    #
    #     clf = self.fit_decision_tree(X, feature_shap_vals, depth)
    #
    #     self.plot_fig_for_tree(clf, X.columns)
    #
    # def get_decition_tree_text_for_feature(
    #     self, model, df, feature_name, depth, should_remove_original_feature=False
    # ):
    #     X, y = self.get_cleaned_data_for_shap(df)
    #     shap_values = self.get_shap_values_for_tree(model, X, y)
    #
    #     feature_index = self.get_feature_index(feature_name, X)
    #     feature_shap_vals = self.get_feature_shap_vals(shap_values, feature_index)
    #
    #     if should_remove_original_feature:
    #         X = X.drop(feature_name, axis=1)
    #
    #     clf = self.fit_decision_tree(X, feature_shap_vals, depth)
    #
    #     return clf, X
