from PyQt5 import QtGui


stylesheet = """
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


save_complete_message = "Сохранение завершено"

dataset_load_error = "Загруженный объект не является выборкой"
model_load_error = "Загруженный объект не является выборкой"

data_is_awaited_message = "Ожидается загрузка датасета и модели"
only_model_loaded_message = "Загрузка модели произведена. Ожидается загрузка выборки"
only_dataset_loaded_message = "Загрузка датасета произведена. Ожидается загрузка модели"
dataset_and_model_loaded_message = "Датасет и модель загружены"

no_plots_message = "Для сохранения постройте графики"

debug_file_path = "../data/obj_v2"


qt_color_white = QtGui.QColor(255, 255, 255)
qt_color_beige = QtGui.QColor(235, 204, 153)


TOP5_CENTERED_IMPORTANCE_TITLE = "Центрированный график изменения важности переменных"

ICE_IMPORTANCE_Y_LABEL = "Важность переменной {}"
ICE_IMPORTANCE_TITLE = "с-ICE график изменения важности переменной {}"

ICE_PREDICTIONS_Y_LABEL = "Вероятность удачного исхода при изменении переменной {}"
ICE_PREDICTIONS_TITLE = (
    "с-ICE график вероятности удачного исхода при изменении переменной {}"
)
