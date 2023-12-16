from pydantic import BaseModel
from pandas import DataFrame
from xgboost import XGBClassifier


class MostImportantColumns(BaseModel):
    name: str
    index: int
