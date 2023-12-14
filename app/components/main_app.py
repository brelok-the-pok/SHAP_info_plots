import tempfile

import matplotlib.pyplot as plt
from app.constants import (
    stylesheet,
    debug_file_path,
    dataset_and_model_loaded_message,
    data_is_awaited_message,
    only_dataset_loaded_message,
    only_model_loaded_message,
    save_complete_message,
    no_plots_message,
)
from app.services.created_plots_saver import CreatedPlotsSaver
from app.functions import (
    find_categorical,
    getMinMax,
    plot_ice_plot,
    plot_top5_centered_importance,
)
from pandas import DataFrame
from xgboost import XGBClassifier
from app.services.pickle_service import PickleService
from PyQt5 import QtCore, QtWidgets, uic
from app.schemes.pickled_data import DatasetModelMonoObject
from app.services.qt_helper import QtHelper
from app.components.plot_settings_app import PlotDataDialog
from app.components.plot_container import PlotContainer
from app.services.dataset_renderer import DatasetRendered


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__()

        self.__qt_helper = QtHelper()
        self.__pickle_service = PickleService()

        uic.loadUi("../ui/main.ui", self)

        self.open_file_action.setStatusTip("Открыть файл проекта")
        self.open_file_action.triggered.connect(self.open_saved_file)

        self.save_file_action.setStatusTip("Сохранить файл модели и выборки")
        self.save_file_action.triggered.connect(self.save_file)

        self.load_model_action.setStatusTip("Открыть файл модели")
        self.load_model_action.triggered.connect(self.open_model)

        self.load_dataset_action.setStatusTip("Открыть файл выборки")
        self.load_dataset_action.triggered.connect(self.open_dataset)

        self.save_plot_action.triggered.connect(self.save_plots)

        self.push_button_plot.clicked.connect(self.make_plots)

        self.plots_combo_box.currentIndexChanged.connect(self.switch_plots)

        self.statusBar().showMessage("Ожидается загрузка модели и датасета")

        self.is_model_loaded = False
        self.is_dataset_loaded = False

        self.__model = None
        self.__dataset = None

        self.temp_dir = tempfile.TemporaryDirectory()

        self.setWindowState(QtCore.Qt.WindowMaximized)
        self.debug_start()
        self.show()

    @property
    def dataset(self) -> DataFrame:
        return self.__dataset

    @dataset.setter
    def dataset(self, dataset) -> None:
        self.is_dataset_loaded = True
        self.__dataset = dataset

        self.create_columns()
        self.create_rows()
        self.show_data_status()

    @property
    def model(self) -> XGBClassifier:
        return self.__model

    @model.setter
    def model(self, model) -> None:
        self.is_model_loaded = True
        self.__model = model
        self.show_data_status()

    def closeEvent(self, event):
        self.temp_dir.cleanup()

    def debug_start(self):
        self.open_saved_file(debug_file_path)

    def show_data_status(self) -> None:
        if self.is_dataset_loaded and self.is_model_loaded:
            self.statusBar().showMessage(dataset_and_model_loaded_message)
        elif self.is_dataset_loaded:
            self.statusBar().showMessage(only_dataset_loaded_message)
        elif self.is_model_loaded:
            self.statusBar().showMessage(only_model_loaded_message)
        else:
            self.statusBar().showMessage(data_is_awaited_message)

    def open_saved_file(self, path: str = ""):
        if not path:
            file_name = self.__qt_helper.get_path_to_open_file(self)
        else:
            file_name = path

        if not file_name:
            return

        mono_object = self.__pickle_service.get_dataset_and_model(file_name)

        self.model = mono_object.model
        self.dataset = mono_object.dataset

    def save_file(self):
        if not all([self.is_dataset_loaded, self.is_model_loaded]):
            self.show_data_status()
            return

        file_name = self.__qt_helper.get_path_to_save_file(self)

        if not file_name:
            return

        mono = DatasetModelMonoObject(dataset=self.__dataset, model=self.model)
        self.__pickle_service.save_dataset_and_model(mono, file_name)

        self.statusBar().showMessage(save_complete_message)

    def open_dataset(self):
        path = self.__qt_helper.get_path_to_open_file(self)

        if not path:
            return None

        self.dataset = self.__pickle_service.get_dataset(path)

    def create_columns(self):
        layout = DatasetRendered(self.dataset).get_rendered_info_plots_layout()
        self.tabCollumns.setLayout(layout)

    def create_rows(self):
        layout = DatasetRendered(self.dataset).get_rendered_data_layout()
        self.tabData.setLayout(layout)

    def open_model(self):
        file_name = self.__qt_helper.get_path_to_open_file(self)

        if not file_name:
            return

        self.model = self.__pickle_service.get_model(file_name)

    def save_plots(self):
        if self.plots_combo_box.count() == 0:
            self.statusBar().showMessage(no_plots_message)
            return

        path = self.__qt_helper.get_existing_dir_path(self)

        if not path:
            return

        CreatedPlotsSaver.save_plots(self.temp_dir.name, path)

    def switch_plots(self):
        if not self.is_plots_in_progress:
            text = self.plots_combo_box.currentText()
            self.show_grath(text.replace(":", ""))

    def make_plots(self):
        if not self.is_dataset_loaded and self.is_model_loaded:
            self.show_data_status()

        self.dialog = QtWidgets.QDialog()
        self.ui = PlotDataDialog()
        minMax = getMinMax(self.dataset)
        categorical = find_categorical(self.dataset)
        self.ui.setupUi(
            self.dialog, list(self.dataset.columns), categorical, minMax, self
        )
        self.dialog.show()

    def createPlots(self, colName, minVal, maxVal, categorcal_col=""):
        categorical = categorcal_col != ""

        cond1 = self.dataset[colName] >= minVal
        cond2 = self.dataset[colName] <= maxVal

        cur_data = self.dataset[cond1 & cond2].reset_index(drop=True)

        h = 6
        w = 12
        plt.figure(1, figsize=(1000, 1000), dpi=1)

        temp = self.temp_dir

        self.is_plots_in_progress = True

        if categorical:
            categories = sorted(list(self.dataset[categorcal_col].unique()))
            categories_items = [f"{colName}:{categorcal_col}:{x}" for x in categories]
            self.plots_combo_box.addItems(categories_items)
            self.plots_combo_box.setEnabled(True)
            self.plots_combo_box.setCurrentIndex(
                self.plots_combo_box.count() - len(categories)
            )

            for i in range(len(categories)):
                plt.clf()

                cond3 = self.dataset[categorcal_col] == categories[i]

                cur_data = self.dataset[cond1 & cond2 & cond3].reset_index(drop=True)

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
                        self.dataset[cond1 & cond2].reset_index(drop=True),
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
                        self.dataset[cond1 & cond2].reset_index(drop=True),
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
        temp = self.temp_dir
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
        temp = self.temp_dir
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
