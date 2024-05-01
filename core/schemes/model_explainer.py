from pydantic import BaseModel


class MostImportantColumns(BaseModel):
    name: str
    index: int
