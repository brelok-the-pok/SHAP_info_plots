from pandas import DataFrame
from PyQt5 import QtGui, QtWidgets, QtCore
from app.constants import stylesheet, qt_color_beige, qt_color_white
import tempfile
import matplotlib.pyplot as plt


class DatasetRendered:
    def __init__(self, dataset: DataFrame) -> None:
        self.__dataset = dataset
        self.__term_dir = tempfile.TemporaryDirectory()

    def get_rendered_data_layout(self) -> QtWidgets.QVBoxLayout:
        vLayout = QtWidgets.QVBoxLayout()

        tableWidget = QtWidgets.QTableWidget()
        tableWidget.setSortingEnabled(True)

        tableWidget.setColumnCount(self.__dataset.shape[1])
        tableWidget.setRowCount(self.__dataset.shape[0])

        tableWidget.setHorizontalHeaderLabels(list(self.__dataset.columns))

        cur_color = qt_color_white

        for i in range(0, self.__dataset.shape[0]):
            if cur_color == qt_color_beige:
                cur_color = qt_color_white
            else:
                cur_color = qt_color_beige

            for j in range(0, self.__dataset.shape[1]):
                item = QtWidgets.QTableWidgetItem(f"{self.__dataset.loc[i][j]}")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(i, j, item)
                tableWidget.item(i, j).setBackground(cur_color)

        tableWidget.setFont(QtGui.QFont("Arial", 12))
        tableWidget.resizeColumnsToContents()

        vLayout.addWidget(tableWidget)

        return vLayout

    def get_rendered_info_plots_layout(self) -> QtWidgets.QVBoxLayout:
        vertLayout = QtWidgets.QVBoxLayout()
        groupBox = QtWidgets.QGroupBox()
        shape = self.__dataset.shape

        for i in range(0, shape[1]):
            groupBox1 = QtWidgets.QGroupBox()
            groupBox1.setStyleSheet(stylesheet)

            minLabel = QtWidgets.QLabel(
                f"min: {round(self.__dataset[self.__dataset.columns[i]].min(), 2)}"
            )
            meanLabel = QtWidgets.QLabel(
                f"mean: {round(self.__dataset[self.__dataset.columns[i]].mean(), 2)}"
            )
            maxLabel = QtWidgets.QLabel(
                f"max: {round(self.__dataset[self.__dataset.columns[i]].max(), 2)}"
            )

            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(minLabel)
            vbox.addWidget(meanLabel)
            vbox.addWidget(maxLabel)

            label = QtWidgets.QLabel()
            plt.clf()
            plot = plt.axes()
            plot.hist(
                x=self.__dataset[self.__dataset.columns[i]],
                label=self.__dataset.columns[i],
            )
            plot.get_xaxis().set_ticklabels([])
            plot.get_yaxis().set_ticklabels([])
            plot.get_figure().savefig(self.__term_dir.name + f"/img{i}.svg")

            pixmap = QtGui.QPixmap(self.__term_dir.name + f"/img{i}.svg")
            pixmap = pixmap.scaledToHeight(200).scaledToWidth(200)
            label.setPixmap(pixmap)

            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(label)
            hbox.addLayout(vbox)

            hbox.setContentsMargins(0, 12, 0, 0)
            hbox.setStretch(0, 4)
            hbox.setStretch(1, 1)
            groupBox1.setLayout(hbox)
            groupBox1.setTitle(self.__dataset.columns[i])
            vertLayout.addWidget(groupBox1)

        groupBox.setLayout(vertLayout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll)

        vvlayout = QtWidgets.QVBoxLayout()
        vvlayout.addLayout(layout)

        return vvlayout
