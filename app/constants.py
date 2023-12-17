from PyQt5 import QtGui


STYLESHEET = """
    border-bottom-width: 1px;
    border-bottom-style: solid;
    border-top-width: 1px;
    border-top-style: solid;
    border-left-width: 1px;
    border-left-style: solid;
    border-right-width: 1px;
    border-right-style: solid;
    border-radius: 0px;
"""

COLORS = ["brown", "teal", "blue", "coral", "limegreen", "pink", "olive", "navy", "red"]
FONT_SIZE = 18
FIG_COUNT = 1

PLOT_WIDTH = 16
PLOT_HEIGHT = 10

FIG_WIDTH = PLOT_WIDTH * 100
FIG_HEIGHT = PLOT_HEIGHT * 100

FIG_SIZE = (FIG_WIDTH, FIG_HEIGHT)
DPI = 2


SAVE_COMPLETE_MESSAGE = "Сохранение завершено"

DATASET_LOAD_ERROR_MESSAGE = "Загруженный объект не является выборкой"
MODEL_LOAD_ERROR = "Загруженный объект не является выборкой"

DATA_IS_AWAITED_MESSAGE = "Ожидается загрузка датасета и модели"
ONLY_MODEL_LOADED_MESSAGE = "Загрузка модели произведена. Ожидается загрузка выборки"
ONLY_DATASET_LOADED_MESSAGE = "Загрузка датасета произведена. Ожидается загрузка модели"
DATASET_AND_MODEL_LOADED_MESSAGE = "Датасет и модель загружены"

NO_PLOTS_MESSAGE = "Для сохранения постройте графики"

DEBUG_FILE_PATH = "../data/obj_v2"


QT_COLOR_WHITE = QtGui.QColor(255, 255, 255)
QT_COLOR_BEIGE = QtGui.QColor(235, 204, 153)


TOP5_CENTERED_IMPORTANCE_TITLE = "Центрированный график изменения важности переменных"

ICE_IMPORTANCE_Y_LABEL = "Важность переменной {}"
ICE_IMPORTANCE_TITLE = "с-ICE график изменения важности переменной {}"

ICE_PREDICTIONS_Y_LABEL = "Вероятность удачного исхода при изменении переменной {}"
ICE_PREDICTIONS_TITLE = (
    "с-ICE график вероятности удачного исхода при изменении переменной {}"
)

PLOT_SETTINGS_ERROR_MESSAGE = (
    "Именна переменной варьирования и категориальной переменной не могут совпадать"
)
