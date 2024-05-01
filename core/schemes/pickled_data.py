from pydantic import BaseModel
from pandas import DataFrame
from xgboost import XGBClassifier


class DatasetModelMonoObject(BaseModel):
    dataset: DataFrame
    model: XGBClassifier

    class Config:
        arbitrary_types_allowed = True
