from sklearn import tree
from app.constants import FONT_SIZE, FIG_SIZE, DPI, PLOT_HEIGHT, PLOT_WIDTH
from matplotlib import pyplot as plt


class TreeModelFigureBuilder:
    def __init__(self, model, columns, feature_name):
        self.model = model
        self.columns = columns
        self.feature_name = feature_name

    def get_model_figure(self):
        plot = self._get_empty_plot()
        fig = plot.get_figure()
        fig.set_size_inches(30, 15)
        tree.plot_tree(
            self.model,
            filled=True,
            feature_names=self.columns,
            ax=plot,
            impurity=False,
            proportion=True,
        )
        plot.get_figure().savefig(f"D:/AMI/tests/1.png", bbox_inches="tight")

        return plot.get_figure()

    def _get_empty_plot(self):
        plt.figure(1, figsize=(30, 15), dpi=DPI)
        plt.clf()
        plot = plt.axes()
        plot.set_title(f"{self.feature_name}", fontsize=FONT_SIZE)

        return plot
