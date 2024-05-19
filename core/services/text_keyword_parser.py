from typing import Callable
from enum import Enum
import re


def explain_one(**kwargs):
    dataset = kwargs["dataset"]
    value = kwargs["value"]

    result = "Что будет с записью, у которой следующие параметры? В какое из правил она может попасть и почему\n"

    instance = dataset[value : value + 1]
    for column in dataset.columns:
        result += f"{column}: {list(getattr(instance, column))[0]}\n"

    return result


def get_stats(**kwargs):
    dataset = kwargs["dataset"]

    result = "Оформи в текстовом виде вот эту таблицу:\n"
    result += str(dataset.describe())

    return result


def get_n_first(**kwargs):
    dataset = kwargs["dataset"]
    value = kwargs["value"]

    result = "Отправь пользователю вот эту таблицу без редактирования:\n"
    result += str(dataset.head(value))

    return result


def get_n_last(**kwargs):
    dataset = kwargs["dataset"]
    value = kwargs["value"]

    result = "Оформи в текстовом виде вот эту таблицу:\n"
    result += str(dataset.tail(value))

    return result


class KeywordHandler:
    def __init__(self, reg, func):
        self.reg = reg
        self.func = func


class Keywords(Enum):
    EXPLAIN_ONE = KeywordHandler(re.compile("Объясни .*?(\d+)"), explain_one)
    STATS = KeywordHandler(re.compile("Приведи статистику"), get_stats)
    SHOW_N_FIRST = KeywordHandler(
        re.compile("Покажи первые (\d+) записей"), get_n_first
    )
    SHOW_N_LAST = KeywordHandler(
        re.compile("Покажи последние (\d+) записей"), get_n_last
    )


class TextKeywordParser:
    def __init__(self, params):
        self.params = params

    def fill_text_with_additional_info(self, text: str) -> str:
        for keyword in Keywords:
            res = keyword.value.reg.findall(text)
            if res:
                value = int(res[0]) if res[0].isdigit() else res[0]
                return keyword.value.func(**self.params, value=value)

        return text
