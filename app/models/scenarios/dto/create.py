from pydantic import BaseModel
from typing import List
from ..domain.category import Category

class CreateScenarioRequest(BaseModel):
    title: str
    short_desc: str
    long_desc: str
    categories: List[Category]