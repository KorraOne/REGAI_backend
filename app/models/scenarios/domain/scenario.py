from pydantic import BaseModel
from typing import List
from .category import Category
from .stakeholder import Stakeholder, SeniorDev
from .requirement import Requirement

class Scenario(BaseModel):
    id: int
    owner_id: int
    title: str
    short_desc: str
    long_desc: str
    categories: List[Category]
    stakeholders: List[Stakeholder]
    seniordev: SeniorDev
    requirements: List[Requirement]