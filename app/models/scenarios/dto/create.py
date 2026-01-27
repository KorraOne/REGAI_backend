from pydantic import BaseModel
from typing import List
from ..domain.category import Category
from ..dto.summary import StakeholderSummary

class CreateScenarioRequest(BaseModel):
    title: str
    short_desc: str
    long_desc: str
    categories: List[Category]
    stakeholders: List[StakeholderSummary]

class ChatMessageRequest(BaseModel):
    message: str