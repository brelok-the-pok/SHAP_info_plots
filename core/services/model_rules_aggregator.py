import numpy as np

from sklearn.tree import DecisionTreeRegressor, _tree


class ModelRulesAggregator:
    def __init__(self, tree: DecisionTreeRegressor, columns):
        self.tree = tree
        self.columns = columns

    def get_formatted_rules(self) -> str:
        rules = self._get_rules()
        return self._format_rules(rules)

    def _get_rules(self, res_name="Вероятность"):
        tree_ = self.tree.tree_

        feature_name = []
        for i in tree_.feature:
            feature_name.append(self.columns[i])

        paths = []
        path = []

        def recursive_descent(node, path, paths):
            if tree_.feature[node] != _tree.TREE_UNDEFINED:
                name = feature_name[node]
                threshold = tree_.threshold[node]
                p1, p2 = list(path), list(path)
                p1 += [f"({name} <= {np.round(threshold, 3)})"]
                recursive_descent(tree_.children_left[node], p1, paths)
                p2 += [f"({name} > {np.round(threshold, 3)})"]
                recursive_descent(tree_.children_right[node], p2, paths)
            else:
                path += [(tree_.value[node], tree_.n_node_samples[node])]
                paths += [path]

        recursive_descent(0, path, paths)

        samples_count = [p[-1][1] for p in paths]
        ii = list(np.argsort(samples_count))
        paths = [paths[i] for i in reversed(ii)]

        rules = {}
        for path in paths:
            rule = "Если "

            for p in path[:-1]:
                if rule != "Если ":
                    rule += " И "
                rule += f"{p}"
            val = int(np.round(path[-1][0][0][0] * 100, 0))
            rule = f"{res_name}={val} ({rule})"

            rules[rule] = val

        sorted_rules = list(sorted(rules, key=lambda x: rules[x], reverse=True))

        return sorted_rules

    @staticmethod
    def _format_rules(rules: list[str]) -> str:

        rules = [f"{i}. {x}" for i, x in enumerate(rules, start=1)]
        formatted_rules = ";\n".join(rules) + ";"
        replace_rules = {
            "sex > 0.5": "sex = M",
            "sex <= 0.5": "sex = F",
            "class > 2.5": "class = High",
            "class <= 2.5": "class = Low",
            "Вероятность_0": "Вероятность",
            "Вероятность_1": "Вероятность",
            "Вероятность_2": "Вероятность",
            "Вероятность_3": "Вероятность",
            "Вероятность_4": "Вероятность",
        }
        for from_, to in replace_rules.items():
            formatted_rules = formatted_rules.replace(from_, to)

        return formatted_rules
