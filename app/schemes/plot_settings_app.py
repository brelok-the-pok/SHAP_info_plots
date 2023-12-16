from typing import Optional

from pydantic import BaseModel


class PlotSettings(BaseModel):
    min_value: float
    max_value: float
    column: str
    catrgory_column: Optional[str] = None
