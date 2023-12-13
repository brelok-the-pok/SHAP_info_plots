import os
import shutil
import tempfile
from pathlib import Path

import matplotlib.pyplot as plt
from app.constants import stylesheet
from app.functions import (
    find_categorical,
    getMinMax,
    plot_ice_plot,
    plot_top5_centered_importance,
)
from app.services.pickle_service import PickleService
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from app.schemes.pickled_data import DatasetModelMonoObject
from app.services.qt_helper import QtHelper
from PlotData import PlotDataDialog
from app.components.plot_container import PlotContainer


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__()

        self.__qt_helper = QtHelper()
        self.__pickle_service = PickleService()

        uic.loadUi("../ui/main.ui", self)

        self.open_file_action.setStatusTip("Открыть файл проекта")
        self.open_file_action.triggered.connect(self.OpenSavedFile)

        self.save_file_action.setStatusTip("Сохранить файл модели и выборки")
        self.save_file_action.triggered.connect(self.save_file)

        self.load_model_action.setStatusTip("Открыть файл модели")
        self.load_model_action.triggered.connect(self.OpenModel)

        self.load_dataset_action.setStatusTip("Открыть файл выборки")
        self.load_dataset_action.triggered.connect(self.open_dataset)

        self.save_plot_action.triggered.connect(self.save_plots)

        self.push_button_plot.clicked.connect(self.make_plots)

        self.plots_combo_box.currentIndexChanged.connect(self.changeGrath)

        self.statusBar().showMessage("Ожидается загрузка модели и датасета")

        self.is_model_loaded = False
        self.is_dataset_loaded = False

        self.model = None
        self.data = None
        self.clear_data = None

        self.temp = tempfile.TemporaryDirectory()

        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.debug_start()
        self.show()

    def closeEvent(self, event):
        self.temp.cleanup()

    def debug_start(self):
        fname = "../data/obj_v2"
        mono_object = self.__pickle_service.get_dataset_and_model(fname)
        self.model = mono_object.model
        self.data = mono_object.dataset
        self.clear_data = self.data

        self.create_columns(self.data)
        self.create_rows(self.data)

        self.is_model_loaded = True
        self.is_dataset_loaded = True

        self.statusBar().showMessage("Загрузка датасета и модели произведена")

    def OpenSavedFile(self):
        home_dir = str(Path.cwd())
        fname = QFileDialog.getOpenFileName(self, "Открыть файл", home_dir)
        if fname[0]:
            modelNdata = self.__pickle_service.get_dataset_and_model(fname[0])

            if modelNdata is not None:
                try:
                    modelNdata[1].columns
                except:
                    self.statusBar().showMessage(
                        "Загруженный объект не является сохранённым"
                    )
                    return

                try:
                    modelNdata[0].classes_
                except:
                    self.statusBar().showMessage(
                        "Загруженный объект не является сохранённым"
                    )
                    return

                self.model = modelNdata[0]
                self.data = modelNdata[1]

                self.create_columns(self.data)
                self.create_rows(self.data)

                self.is_model_loaded = True
                self.is_dataset_loaded = True

                self.statusBar().showMessage("Загрузка датасета и модели произведена")
            else:
                self.statusBar().showMessage("Ошибка загрузки, неверный файл")

    def save_file(self):
        if self.is_model_loaded and self.is_dataset_loaded:
            fname = QFileDialog.getSaveFileName(self, "Сохранить файл", str(Path.cwd()))

            if path := fname[0]:
                mono = DatasetModelMonoObject(dataset=self.data, model=self.model)
                self.__pickle_service.save_dataset_and_model(mono, path)

                self.statusBar().showMessage("Сохранение модели и датасета произведено")
        else:
            self.statusBar().showMessage("Не загружена модель или датасет")

    def open_dataset(self):
        path = self.__qt_helper.get_path_to_file(self)

        if not path:
            return None

        data = self.__pickle_service.get_dataset(path)

        self.data = data
        self.clear_data = data

        self.create_columns(self.data)
        self.create_rows(self.data)

        self.is_dataset_loaded = True

        if self.is_model_loaded:
            self.statusBar().showMessage("Загрузка выборки произведена.")
        else:
            self.statusBar().showMessage(
                "Загрузка выборки произведена. Ожидается загрузка модели"
            )

    def create_columns(self, data):
        vertLayout = QtWidgets.QVBoxLayout()
        groupBox = QtWidgets.QGroupBox()
        shape = data.shape

        temp = tempfile.TemporaryDirectory()

        for i in range(0, shape[1]):
            groupBox1 = QtWidgets.QGroupBox()
            groupBox1.setStyleSheet(stylesheet)

            minLabel = QtWidgets.QLabel(f"min: {round(data[data.columns[i]].min(), 2)}")
            meanLabel = QtWidgets.QLabel(
                f"mean: {round(data[data.columns[i]].mean(), 2)}"
            )
            maxLabel = QtWidgets.QLabel(f"max: {round(data[data.columns[i]].max(), 2)}")

            vbox = QtWidgets.QVBoxLayout()
            vbox.addWidget(minLabel)
            vbox.addWidget(meanLabel)
            vbox.addWidget(maxLabel)

            label = QtWidgets.QLabel()
            plt.clf()
            plot = plt.axes()
            plot.hist(x=data[data.columns[i]], label=data.columns[i])
            # plot.set_title(data.columns[i])
            plot.get_xaxis().set_ticklabels([])
            plot.get_yaxis().set_ticklabels([])
            plot.get_figure().savefig(temp.name + f"/img{i}.svg")

            pixmap = QtGui.QPixmap(temp.name + f"/img{i}.svg")
            pixmap = pixmap.scaledToHeight(200).scaledToWidth(200)
            label.setPixmap(pixmap)

            hbox = QtWidgets.QHBoxLayout()
            hbox.addWidget(label)
            hbox.addLayout(vbox)

            # vertLayout.addLayout(hbox)
            hbox.setContentsMargins(0, 12, 0, 0)
            hbox.setStretch(0, 4)
            hbox.setStretch(1, 1)
            groupBox1.setLayout(hbox)
            groupBox1.setTitle(data.columns[i])
            vertLayout.addWidget(groupBox1)

        groupBox.setLayout(vertLayout)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidget(groupBox)
        scroll.setWidgetResizable(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(scroll)

        vvlayout = QtWidgets.QVBoxLayout()
        vvlayout.addLayout(layout)

        self.tabCollumns.setLayout(vvlayout)

    def create_rows(self, data):
        vLayout = QtWidgets.QVBoxLayout()

        tableWidget = QtWidgets.QTableWidget()
        tableWidget.setSortingEnabled(True)

        shape = data.shape

        tableWidget.setColumnCount(shape[1])
        tableWidget.setRowCount(shape[0])

        columns = list(data.columns)
        tableWidget.setHorizontalHeaderLabels(columns)

        color_white = QtGui.QColor(255, 255, 255)
        color_beige = QtGui.QColor(235, 204, 153)
        cur_color = color_white

        for i in range(0, shape[0]):
            if cur_color == color_beige:
                cur_color = color_white
            else:
                cur_color = color_beige

            for j in range(0, shape[1]):
                item = QtWidgets.QTableWidgetItem(f"{data.loc[i][j]}")
                item.setFlags(QtCore.Qt.ItemIsEnabled)
                tableWidget.setItem(i, j, item)
                tableWidget.item(i, j).setBackground(cur_color)

        tableWidget.setFont(QtGui.QFont("Arial", 12))
        tableWidget.resizeColumnsToContents()

        vLayout.addWidget(tableWidget)
        self.tabData.setLayout(vLayout)

    def OpenModel(self):
        home_dir = str(Path.cwd())
        fname = QFileDialog.getOpenFileName(self, "Open file", home_dir)
        if fname[0]:
            model = self.__pickle_service.get_model(fname[0])

            if model is not None:
                try:
                    model.classes_
                except:
                    self.statusBar().showMessage(
                        "Загруженный объект не является моделью"
                    )
                    return

                self.model = model
                self.is_model_loaded = True
                self.statusBar().showMessage("Загрузка модели произведена")

                if self.is_dataset_loaded:
                    self.statusBar().showMessage("Загрузка модели произведена.")
                else:
                    self.statusBar().showMessage(
                        "Загрузка модели произведена. Ожидается загрузка выборки"
                    )
            else:
                self.statusBar().showMessage("Ошибка загрузки, неверный файл")

    def save_plots(self):
        if self.plots_combo_box.count() != 0:
            home_dir = str(Path.cwd())
            dir_name = QFileDialog.getExistingDirectory(
                self, "Сохранить файл", home_dir
            )
            if dir_name:
                files = os.listdir(self.temp.name)
                for file in files:
                    if ".png" in file:
                        shutil.copy2(f"{self.temp.name}\\{file}", f"{dir_name}\\{file}")
        else:
            self.statusBar().showMessage(
                "Сохранение графиков невозможно, графики не были построены"
            )

    def changeGrath(self):
        if not self.is_plots_in_progress:
            text = self.plots_combo_box.currentText()
            print(text)

            self.show_grath(text.replace(":", ""))

    def make_plots(self):
        if self.is_dataset_loaded and self.is_model_loaded:
            self.dialog = QtWidgets.QDialog()
            self.ui = PlotDataDialog()
            minMax = getMinMax(self.clear_data)
            categorical = find_categorical(self.clear_data)
            self.ui.setupUi(
                self.dialog, list(self.clear_data.columns), categorical, minMax, self
            )
            self.dialog.show()
        else:
            self.statusBar().showMessage(
                "Для постройки графиков загрузите модель и выборку"
            )

    def createPlots(self, colName, minVal, maxVal, categorcal_col=""):
        categorical = categorcal_col != ""

        cond1 = self.clear_data[colName] >= minVal
        cond2 = self.clear_data[colName] <= maxVal

        cur_data = self.clear_data[cond1 & cond2].reset_index(drop=True)

        h = 6
        w = 12
        plt.figure(1, figsize=(1000, 1000), dpi=1)

        temp = self.temp

        self.is_plots_in_progress = True

        if categorical:
            categories = sorted(list(self.clear_data[categorcal_col].unique()))
            categories_items = [f"{colName}:{categorcal_col}:{x}" for x in categories]
            self.plots_combo_box.addItems(categories_items)
            self.plots_combo_box.setEnabled(True)
            self.plots_combo_box.setCurrentIndex(
                self.plots_combo_box.count() - len(categories)
            )

            for i in range(len(categories)):
                plt.clf()

                cond3 = self.clear_data[categorcal_col] == categories[i]

                cur_data = self.clear_data[cond1 & cond2 & cond3].reset_index(drop=True)

                name = categories_items[i].replace(":", "")

                plot_lt = plot_top5_centered_importance(
                    self.model, cur_data, colName, True
                )
                fig_lt = plot_lt.get_figure()
                fig_lt.set_size_inches(w, h)
                fig_lt.savefig(temp.name + f"\\img1{name}.svg", bbox_inches="tight")
                fig_lt.savefig(
                    temp.name + f"\\img1{name}.png", bbox_inches="tight", format="png"
                )
                plt.clf()
                #
                if colName == categorcal_col:
                    plot_lb = plot_ice_plot(
                        self.model,
                        self.clear_data[cond1 & cond2].reset_index(drop=True),
                        colName,
                        True,
                    )
                else:
                    plot_lb = plot_ice_plot(self.model, cur_data, colName, True)
                fig_lb = plot_lb.get_figure()
                fig_lb.set_size_inches(w, h)
                fig_lb.savefig(temp.name + f"\\img2{name}.svg", bbox_inches="tight")
                fig_lb.savefig(
                    temp.name + f"\\img2{name}.png", bbox_inches="tight", format="png"
                )
                plt.clf()

                plot_rt = plot_top5_centered_importance(self.model, cur_data, colName)
                fig_rt = plot_rt.get_figure().figure
                fig_rt.set_size_inches(w, h)
                fig_rt.savefig(temp.name + f"\\img0{name}.svg", bbox_inches="tight")
                fig_rt.savefig(
                    temp.name + f"\\img0{name}.png", bbox_inches="tight", format="png"
                )
                plt.clf()
                #
                if colName == categorcal_col:
                    plot_rb = plot_ice_plot(
                        self.model,
                        self.clear_data[cond1 & cond2].reset_index(drop=True),
                        colName,
                    )
                else:
                    plot_rb = plot_ice_plot(self.model, cur_data, colName)
                fig_rb = plot_rb.get_figure().figure
                fig_rb.set_size_inches(w, h)
                fig_rb.savefig(temp.name + f"\\img3{name}.svg", bbox_inches="tight")
                fig_rb.savefig(
                    temp.name + f"\\img3{name}.png", bbox_inches="tight", format="png"
                )
                plt.clf()

            self.show_grath(
                self.plots_combo_box.itemText(
                    self.plots_combo_box.count() - len(categories)
                ).replace(":", "")
            )

        else:
            self.plots_combo_box.addItems([colName])
            self.plots_combo_box.setEnabled(True)
            self.plots_combo_box.setCurrentIndex(self.plots_combo_box.count() - 1)

            plt.clf()
            plot_lt = plot_top5_centered_importance(self.model, cur_data, colName, True)
            fig_lt = plot_lt.get_figure()
            fig_lt.set_size_inches(w, h)
            fig_lt.savefig(temp.name + f"\\img1{colName}.svg", bbox_inches="tight")
            fig_lt.savefig(
                temp.name + f"\\img1{colName}.png", bbox_inches="tight", format="png"
            )
            plt.clf()

            self.statusBar().showMessage("1")
            print("1")

            plot_lb = plot_ice_plot(self.model, cur_data, colName, True)
            fig_lb = plot_lb.get_figure()
            fig_lb.set_size_inches(w, h)
            fig_lb.savefig(temp.name + f"\\img2{colName}.svg", bbox_inches="tight")
            fig_lb.savefig(
                temp.name + f"\\img2{colName}.png", bbox_inches="tight", format="png"
            )
            plt.clf()
            self.statusBar().showMessage("2")
            print("2")

            plot_rt = plot_top5_centered_importance(self.model, cur_data, colName)
            fig_rt = plot_rt.get_figure().figure
            fig_rt.set_size_inches(w, h)
            fig_rt.savefig(temp.name + f"\\img0{colName}.svg", bbox_inches="tight")
            fig_rt.savefig(
                temp.name + f"\\img0{colName}.png", bbox_inches="tight", format="png"
            )
            plt.clf()
            self.statusBar().showMessage("3")
            print("3")

            plot_rb = plot_ice_plot(self.model, cur_data, colName)
            fig_rb = plot_rb.get_figure().figure
            fig_rb.set_size_inches(w, h)
            fig_rb.savefig(temp.name + f"\\img3{colName}.svg", bbox_inches="tight")
            fig_rb.savefig(
                temp.name + f"\\img3{colName}.png", bbox_inches="tight", format="png"
            )
            plt.clf()
            self.statusBar().showMessage("5")
            print("4")

            self.show_grath(colName)

        self.is_plots_in_progress = False

    def show_grath_by_name(self, i, j, name):
        temp = self.temp
        pixmap = PlotContainer(temp.name + f"/img{2 * i + j}{name}.svg")
        pixmap.setMaximumSize(800, 600)
        pixmap.setStyleSheet(stylesheet)
        pixmap.setSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        widget_to_replace = self.gridLayout.itemAtPosition(i, j)
        widget_to_replace.widget().setParent(None)
        self.gridLayout.addWidget(pixmap, i, j)

    def show_grath(self, name):
        temp = self.temp
        for i in range(0, 2):
            for j in range(0, 2):
                pixmap = PlotContainer(temp.name + f"/img{2 * i + j}{name}.svg")
                pixmap.setMaximumSize(800, 600)
                pixmap.setStyleSheet(stylesheet)
                pixmap.setSizePolicy(
                    QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
                )
                widget_to_replace = self.gridLayout.itemAtPosition(i, j)
                widget_to_replace.widget().setParent(None)
                self.gridLayout.addWidget(pixmap, i, j)
