import sys
from PyQt5 import QtWidgets

from app.components.main_app import MainApp


def dalex_test():
    import dalex as dx
    from core.debug_starter import DebugStarter
    starter = DebugStarter('forest')
    df, model = starter.get_dataset_and_model()
    X = df.drop('survived', axis=1)
    y = df['survived']

    titanic_rf_exp = dx.Explainer(model, X, y, label="Titanic RF Pipeline")

    test = X.iloc[0]
    bd_henry = titanic_rf_exp.predict_parts(test, type='break_down')
    print('ts')


def get_GP_plots():
    from libs.XAI.src.xai import GP
    from core.debug_starter import DebugStarter
    import pathlib
    import os

    if sys.platform == 'win32':
        path = pathlib.Path(r'C:\Program Files\Graphviz\bin')
        if path.is_dir() and str(path) not in os.environ['PATH']:
            os.environ['PATH'] += f';{path}'

    starter = DebugStarter('forest')
    df, model = starter.get_dataset_and_model()
    X = df.drop('survived', axis=1)
    # Train and predict with blackbox
    predictions = [[x] for x in model.predict(X.values)]

    # Use GP to make an approximation of the blackbox predictions
    explainer = GP(max_trees=100, num_generations=1)
    explainer.fit(X.values, predictions)

    # Save our approximations
    explainer.plot("./model.png")
    explainer.plot_pareto("./frontier.png")

def get_extree_plots():
    from lrmatrix.treevis import nodelink
    from core.debug_starter import DebugStarter

    from core.services.simple_tree_model_fitter import SimpleTreeModelFitter
    from core.services.model_rules_aggregator import ModelRulesAggregator
    from exmatrix import ExplainableMatrix



    starter = DebugStarter('forest')
    df, model = starter.get_dataset_and_model()
    feature_names = df.drop('survived', axis=1).columns

    fitter = SimpleTreeModelFitter(model, df, None)
    X = fitter.get_X()
    y = fitter.get_y()
    tree = fitter.get_simple_tree()


    exm = ExplainableMatrix(n_features=len(feature_names), n_classes=len(target_names),
                            feature_names=np.array(feature_names), class_names=np.array(target_names))
    exm.rules_extration([clf], X, y, clf.feature_importances_, n_jobs=1)
    print('n_rules DT', exm.n_rules_)


    tree = nodelink(tree, out_file=None, max_depth=None, feature_names=feature_names, class_names=[0, 1],
                    label='all', filled=True, leaves_parallel=False, impurity=False, node_ids=True, proportion=True,
                    rotate=False, rounded=True, special_characters=False, precision=2)
    tree.write_jpeg('DT.jpeg')


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    app.exec_()
    # get_extree_plots()


if __name__ == "__main__":
    main()


