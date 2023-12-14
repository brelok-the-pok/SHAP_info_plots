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
