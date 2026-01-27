from pydantic import BaseModel
from typing import Optional, List
from ..domain.category import Category
from ..dto.summary import StakeholderSummary

class EditScenarioRequest(BaseModel):
    title: Optional[str] = None
    short_desc: Optional[str] = None
    long_desc: Optional[str] = None
    categories: Optional[List[Category]] = None
    stakeholders: Optional[List[StakeholderSummary]]