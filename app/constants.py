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

r_w, g_w, b_w = 255, 255, 255
r_b, g_b, b_b = 235, 204, 153

QT_COLOR_WHITE = QtGui.QColor(r_w, g_w, b_w)
QT_COLOR_BEIGE = QtGui.QColor(r_b, g_b, b_b)

CHAT_BASE_STYLESHEET = "border: 1px solid black; background-color: rgb({}, {}, {}); "
CHAT_USER_STYLESHEET = CHAT_BASE_STYLESHEET.format(r_w, g_w, b_w)
CHAT_LLM_STYLESHEET = CHAT_BASE_STYLESHEET.format(r_b, g_b, b_b)


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


TOKEN = "y0_AgAAAAAdy8SG3Xh2A"
TOKEN_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
LLM_FOLDER = "b1gqlhmqdst9ejbptsnp"
LLM_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

LLM_SYSTEM_PROMPT = """
Ты опытный аналитик, который профессионально умеет искать внутренние закономерности в данных. 
Тебе передали набор правил, которые описывают зависимость значений нескольких переменных от параметра PROBA. 
Чем выше значение параметра PROBA, тем выше вероятность отнесения конкретной записи к категории GOOD.
Необходимо проанализировать правила и сделать следующие действия:
1. Приведи пример двух записей с высокой вероятностью попадания в категорию GOOD
2. Приведи пример двух записей со средней вероятностью попадания в категорию GOOD
3. Приведи пример двух записей с низкой вероятностью попадания в категорию GOOD
4. Приведи пример записей с самой низкой вероятностью попадания в категорию GOOD и с самой высокой
Обязательно укажи вероятность в скобках у примеров
Пиши краткое и по существу, основываясь на переданных данных, 
не пиши о предварительных данных и что нужно больше информации. 
Сравнение проводи по строгим математическим правилам
"""

LLM_SYSTEM_PROMPT_FOR_USER = """
Проанализируй правила правила и приведи примеры:
1. Приведи пример двух записей с высокой вероятностью попадания в категорию GOOD
2. Приведи пример двух записей со средней вероятностью попадания в категорию GOOD
3. Приведи пример двух записей с низкой вероятностью попадания в категорию GOOD
4. Приведи пример записей с самой низкой вероятностью попадания в категорию GOOD и с самой высокой
"""