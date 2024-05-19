from pandas import DataFrame
from PyQt5 import QtGui, QtWidgets, QtCore
from app.constants import STYLESHEET, QT_COLOR_BEIGE, QT_COLOR_WHITE

import tempfile
import matplotlib.pyplot as plt


class DatasetRendered:
    def __init__(self, dataset: DataFrame) -> None:
        self.__dataset = dataset
        self.__term_dir = tempfile.TemporaryDirectory()

    def get_rendered_data_layout(self) -> QtWidgets.QVBoxLayout:
        vertical_layout = QtWidgets.QVBoxLayout()

        table_widget = QtWidgets.QTableWidget()
        table_widget.setSortingEnabled(True)

        table_widget.setColumnCount(self.__dataset.shape[1])
        table_widget.setRowCount(self.__dataset.shape[0])

        table_widget.setHorizontalHeaderLabels(list(self.__dataset.columns))

        cur_color = QT_COLOR_WHITE

        for i in range(0, self.__dataset.shape[0]):
            if cur_color == QT_COLOR_BEIGE:
                cur_color = QT_COLOR_WHITE
            else:
                cur_color = QT_COLOR_BEIGE

            for j in range(0, self.__dataset.shape[1]):
                item = QtWidgets.QTableWidgetItem(f"{self.__dataset.iloc[i, j]}")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                table_widget.setItem(i, j, item)
                table_widget.item(i, j).setBackground(cur_color)

        table_widget.setFont(QtGui.QFont("Arial", 12))
        table_widget.resizeColumnsToContents()

        vertical_layout.addWidget(table_widget)

        return vertical_layout

    def get_rendered_info_plots_layout(self) -> QtWidgets.QVBoxLayout:
        vertical_layout = QtWidgets.QVBoxLayout()
        main_group_box = QtWidgets.QGroupBox()
        shape = self.__dataset.shape

        for i in range(0, shape[1]):
            sub_group_box = QtWidgets.QGroupBox()
            sub_group_box.setStyleSheet(STYLESHEET)

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

            hbox.setContentsMargins(0, 20, 0, 0)
            hbox.setStretch(0, 0)
            hbox.setStretch(0, 0)
            sub_group_box.setLayout(hbox)
            sub_group_box.setTitle(self.__dataset.columns[i])
            vertical_layout.addWidget(sub_group_box)

        main_group_box.setLayout(vertical_layout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(main_group_box)
        scroll.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll)

        vvlayout = QtWidgets.QVBoxLayout()
        vvlayout.addLayout(layout)

        return vvlayout
