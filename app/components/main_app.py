import tempfile

from app.constants import (
    STYLESHEET,
    DATASET_AND_MODEL_LOADED_MESSAGE,
    DATA_IS_AWAITED_MESSAGE,
    ONLY_DATASET_LOADED_MESSAGE,
    ONLY_MODEL_LOADED_MESSAGE,
    SAVE_COMPLETE_MESSAGE,
    NO_PLOTS_MESSAGE,
    FIG_WIDTH,
    FIG_HEIGHT,
    LLM_SYSTEM_PROMPT_FOR_USER_PREDICT,
    LLM_SYSTEM_PROMPT_FOR_USER_IMPORTANCE,
    LLM_SYSTEM_PROMPT_FOR_PREDICT,
    LLM_SYSTEM_PROMPT_FOR_IMPORTANCE,
    TREE_IMAGE_PATH,
)
from core.schemes import PlotSettings
from core.debug_starter import DebugStarter
from app.services.created_plots_saver import CreatedPlotsSaver
from core.services.data_helper import DataHelper
from pandas import DataFrame
from xgboost import XGBClassifier
from core.services.pickle_service import PickleService
from PyQt5 import QtCore, QtWidgets, uic, QtGui
from core.schemes.pickled_data import DatasetModelMonoObject
from app.services.qt_helper import QtHelper
from app.components.plot_settings_app import PlotDataDialog
from app.components.ai_settings_app import AISettingDialog
from app.components.tree_container import TreeContainer
from app.components.plot_container import PlotContainer
from app.services.dataset_renderer import DatasetRendered
from app.services.plot_creator import PlotCreator
from core.services.llm_controller import LLMController
from core.services.simple_tree_model_fitter import SimpleTreeModelFitter
from core.services.shap_tree_model_fitter import ShapTreeModelFitter
from core.services.model_rules_aggregator import ModelRulesAggregator
from core.services.tree_model_figure_builder import TreeModelFigureBuilder
from app.components.text_chat_scroll_widget import TextChatScrollArea
from core.services.text_keyword_parser import TextKeywordParser


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
        self.show_tree_figure_action.triggered.connect(self.show_tree_figure)

        self.push_button_plot.clicked.connect(self.make_plots)

        self.user_input_button.clicked.connect(self.send_chat_request)
        self.llm_init_button.clicked.connect(self.init_llm_button)

        self.init_scroll()

        self._widget.setLayout(self._layout)

        self.plots_combo_box.currentIndexChanged.connect(self.switch_plots)

        self.statusBar().showMessage("Ожидается загрузка модели и датасета")

        self.default_tree_image_path = TREE_IMAGE_PATH

        self.is_model_loaded = False
        self.is_dataset_loaded = False

        self.__model = None
        self.__dataset = None

        self.__paths: dict[str, list[str]] = {}

        self.temp_dir = tempfile.TemporaryDirectory()

        self.setWindowState(QtCore.Qt.WindowMaximized)
        # self.debug_start()
        self.show()

    @property
    def dataset(self) -> DataFrame:
        return self.__dataset

    @property
    def clean_dataset(self) -> DataFrame:
        return self.__dataset.drop("survived", axis=1)

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
        debug_starter = DebugStarter("boost")
        dataset, model = debug_starter.get_dataset_and_model()
        self.dataset = dataset
        self.model = model
        print('a')

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
        min_max = self.__data_helper.get_dataset_min_max(self.clean_dataset)
        category_columns = self.__data_helper.find_category_columns(self.clean_dataset)
        self.ui.setupUi(
            dialog,
            list(self.clean_dataset.columns),
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
            text_for_llm = TextKeywordParser(
                {"dataset": self.clean_dataset}
            ).fill_text_with_additional_info(text)

            self._scroll.add_text(text)

            response = self.llm_controller.get_answer(
                text_for_llm, text_for_llm == text
            )
            self._scroll.add_text(response)

            scroll_bar = self._scroll.verticalScrollBar()
            scroll_bar.setValue(scroll_bar.maximum() + 500)

    def init_llm_button(self):
        if not self.is_dataset_loaded and self.is_model_loaded:
            self.show_data_status()

        dialog = QtWidgets.QDialog()
        self.ui = AISettingDialog()

        columns = self.clean_dataset.columns
        category_columns = self.__data_helper.find_category_columns(self.clean_dataset)

        self.ui.setupUi(
            dialog, columns, category_columns, self._init_llm_button_callback
        )
        dialog.show()

    def show_tree_figure(self):
        TreeContainer(self.paths).exec_()

    def _init_llm_button_callback(
        self,
        temperature,
        depth,
        importance_tree,
        feature_name="age",
        category_feature_name=None,
    ):
        if importance_tree:
            fitter = ShapTreeModelFitter(self.model, self.dataset, depth, feature_name)
        else:
            fitter = SimpleTreeModelFitter(self.model, self.dataset, depth)

        if category_feature_name:
            trees = fitter.get_category_tree(category_feature_name)
        else:
            trees = [fitter.get_simple_tree()]

        columns = fitter.get_columns()

        paths = {}

        for index, tree in enumerate(trees):
            builder = TreeModelFigureBuilder(tree, columns, feature_name)
            plot = builder.get_model_figure()

            path_name = f"{feature_name}" if importance_tree else "Prediction"

            if category_feature_name:
                path_name += f" - {category_feature_name}_{index}"

            path = self.default_tree_image_path.format(index)
            paths[path_name] = path
            plot.savefig(path, bbox_inches="tight")

        self.paths = paths
        # self.show_tree_figure()

        res_name = "Важность" if importance_tree else "Вероятность"
        res_factor = 1 if importance_tree else 100

        self.init_scroll()
        for index, tree in enumerate(trees, start=1):
            aggregator = ModelRulesAggregator(tree, columns, res_name, res_factor)
            rules = aggregator.get_formatted_rules()

            prompt = (
                LLM_SYSTEM_PROMPT_FOR_IMPORTANCE
                if importance_tree
                else LLM_SYSTEM_PROMPT_FOR_PREDICT
            )

            self.llm_controller = LLMController(temperature, system_prompt=prompt)
            text_field = getattr(self, f"proba_text_{index}")
            if category_feature_name:
                rules = f"При значении {category_feature_name} == {index}\n{rules}"

            text_field.setText(rules)

            if importance_tree:
                self._scroll.add_text(LLM_SYSTEM_PROMPT_FOR_USER_IMPORTANCE)
            else:
                self._scroll.add_text(LLM_SYSTEM_PROMPT_FOR_USER_PREDICT)

            response = self.llm_controller.get_answer(rules)

            self._scroll.add_text(response)

    def init_scroll(self):
        if hasattr(self, "_layout"):
            self._layout.removeWidget(self._scroll)

        self._widget = QtWidgets.QWidget()
        self._layout = self.verticalLayout_2
        self._scroll = TextChatScrollArea()
        self._layout.addWidget(self._scroll)
        self._layout.addWidget(self._scroll)
