import tempfile

from app.constants import (
    STYLESHEET,
    DEBUG_FILE_PATH,
    DATASET_AND_MODEL_LOADED_MESSAGE,
    DATA_IS_AWAITED_MESSAGE,
    ONLY_DATASET_LOADED_MESSAGE,
    ONLY_MODEL_LOADED_MESSAGE,
    SAVE_COMPLETE_MESSAGE,
    NO_PLOTS_MESSAGE,
    FIG_WIDTH,
    FIG_HEIGHT,
    LLM_SYSTEM_PROMPT_FOR_USER
)
from app.schemes.plot_settings_app import PlotSettings
from app.services.created_plots_saver import CreatedPlotsSaver
from app.services.data_helper import DataHelper
from pandas import DataFrame
from xgboost import XGBClassifier
from app.services.pickle_service import PickleService
from PyQt5 import QtCore, QtWidgets, uic
from app.schemes.pickled_data import DatasetModelMonoObject
from app.services.qt_helper import QtHelper
from app.components.plot_settings_app import PlotDataDialog
from app.components.ai_settings_app import AISettingDialog
from app.components.plot_container import PlotContainer
from app.services.dataset_renderer import DatasetRendered
from app.services.plot_creator import PlotCreator
from app.services.llm_controller import LLMController
from app.services.simple_tree_model_fitter import SimpleTreeModelFitter
from app.services.model_rules_aggregator import ModelRulesAggregator
from app.components.text_chat_scroll_widget import TextChatScrollArea


class MainApp(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainApp, self).__init__()

        self.__qt_helper = QtHelper()
        self.__pickle_service = PickleService()
        self.__data_helper = DataHelper()

        uic.loadUi("../ui/main2.ui", self)

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

        self.user_input_button.clicked.connect(self.send_chat_request)
        self.llm_init_button.clicked.connect(self.init_llm_button)

        self._widget = QtWidgets.QWidget()
        self._layout = self.horizontalLayout_8
        self._scroll = TextChatScrollArea()
        self._layout.addWidget(self._scroll)

        self._widget.setLayout(self._layout)

        self.plots_combo_box.currentIndexChanged.connect(self.switch_plots)

        self.statusBar().showMessage("Ожидается загрузка модели и датасета")

        self.is_model_loaded = False
        self.is_dataset_loaded = False

        self.__model = None
        self.__dataset = None

        self.__paths: dict[str, list[str]] = {}

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
        self.open_saved_file(DEBUG_FILE_PATH)

    def show_data_status(self) -> None:
        if self.is_dataset_loaded and self.is_model_loaded:
            self.statusBar().showMessage(DATASET_AND_MODEL_LOADED_MESSAGE)
        elif self.is_dataset_loaded:
            self.statusBar().showMessage(ONLY_DATASET_LOADED_MESSAGE)
        elif self.is_model_loaded:
            self.statusBar().showMessage(ONLY_MODEL_LOADED_MESSAGE)
        else:
            self.statusBar().showMessage(DATA_IS_AWAITED_MESSAGE)

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

        self.statusBar().showMessage(SAVE_COMPLETE_MESSAGE)

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
            self.statusBar().showMessage(NO_PLOTS_MESSAGE)
            return

        path = self.__qt_helper.get_existing_dir_path(self)

        if not path:
            return

        CreatedPlotsSaver.save_plots(self.temp_dir.name, path)

    def switch_plots(self):
        if not self.is_plots_in_progress:
            text = self.plots_combo_box.currentText()
            if text:
                self.show_plots(text)

    def make_plots(self):
        if not self.is_dataset_loaded and self.is_model_loaded:
            self.show_data_status()

        dialog = QtWidgets.QDialog()
        self.ui = PlotDataDialog()
        min_max = self.__data_helper.get_dataset_min_max(self.__dataset)
        category_columns = self.__data_helper.find_category_columns(self.dataset)
        self.ui.setupUi(
            dialog,
            list(self.dataset.columns),
            category_columns,
            min_max,
            self.retrieve_data_from_child,
        )
        dialog.show()

    def retrieve_data_from_child(self, settings: PlotSettings):
        self.is_plots_in_progress = True

        plot_creator = PlotCreator(
            self.model,
            self.dataset,
            settings.column,
            settings.min_value,
            settings.max_value,
            self.temp_dir,
        )

        if settings.category_column:
            full_paths = plot_creator.plot_category_plots(settings.category_column)
            self.__save_category_paths(full_paths, settings)
        else:
            paths = plot_creator.plot_regular_plots()
            self.__save_regular_paths(paths, settings)

        self.is_plots_in_progress = False

        self.__update_plot_names_in_combo_box()
        self.switch_plots()

    def __save_category_paths(
        self, full_paths: list[[list[str]]], settings: PlotSettings
    ) -> None:
        name = self.__get_name_for_settings(settings)
        for index, path in enumerate(full_paths, start=1):
            self.__paths[f"{name} {index}"] = path

    def __save_regular_paths(self, paths: list[str], settings: PlotSettings) -> None:
        name = self.__get_name_for_settings(settings)
        self.__paths[name] = paths

    def __get_name_for_settings(self, settings: PlotSettings) -> str:
        name = f"Колонка {settings.column} от {settings.min_value} и до {settings.max_value}"

        if settings.category_column:
            name += f" по категории {settings.category_column}"

        return name

    def __update_plot_names_in_combo_box(self):
        plot_names = list(self.__paths.keys())

        self.plots_combo_box.clear()
        self.plots_combo_box.addItems(plot_names)
        self.plots_combo_box.setEnabled(True)
        self.plots_combo_box.setCurrentIndex(len(plot_names) - 1)

    def show_plots(self, plots_name: str):
        paths = self.__paths[plots_name]
        indexes = [(0, 0), (0, 1), (1, 0), (1, 1)]

        for path, position in zip(paths, indexes):
            pixmap = PlotContainer(path)
            pixmap.setMaximumSize(FIG_WIDTH, FIG_HEIGHT)
            pixmap.setStyleSheet(STYLESHEET)
            pixmap.setSizePolicy(
                QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum
            )
            widget_to_replace = self.gridLayout.itemAtPosition(*position)
            widget_to_replace.widget().setParent(None)
            self.gridLayout.addWidget(pixmap, *position)

    def send_chat_request(self):
        text = self.user_input_widget.document().toPlainText()
        if text:
            self._scroll.add_text(text)

            response = self.llm_controller.get_answer(text)
            self._scroll.add_text(response)

            scroll_bar = self._scroll.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum() + 500)

    def init_llm_button(self):
        if not self.is_dataset_loaded and self.is_model_loaded:
            self.show_data_status()

        dialog = QtWidgets.QDialog()
        self.ui = AISettingDialog()
        self.ui.setupUi(dialog, self._init_llm_button_callback)
        dialog.show()

    def _init_llm_button_callback(self, temperature, depth):
        fitter = SimpleTreeModelFitter(self.model, self.dataset, depth)
        tree = fitter.get_simple_tree()
        columns = fitter.get_X().columns

        aggregator = ModelRulesAggregator(tree, columns)
        rules = aggregator.get_formatted_rules()

        self.llm_controller = LLMController(temperature)
        self.proba_text.setText(rules)
        self._scroll.add_text(LLM_SYSTEM_PROMPT_FOR_USER)

        response = self.llm_controller.get_answer(rules)
        self._scroll.add_text(response)




