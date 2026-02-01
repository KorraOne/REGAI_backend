from pydantic import BaseModel
from typing import Optional, List, Literal
from ..domain.category import Category
from ..domain.stakeholder import Stakeholder

class EditScenarioRequest(BaseModel):
    title: Optional[str] = None
    short_desc: Optional[str] = None
    long_desc: Optional[str] = None
    categories: Optional[List[Category]] = None
    stakeholders: Optional[List[Stakeholder]] = None


class RequirementUpdateRequest(BaseModel):
    type: Optional[Literal["functional", "non-functional"]] = None
    info: Optional[str] = None