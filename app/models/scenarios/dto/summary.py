from pydantic import BaseModel
from typing import List, Dict
from app.models.scenarios.domain.scenario import Stakeholder, SeniorDev
from app.models.scenarios.domain.category import Category

class StakeholderSummary(Stakeholder):
    chats: None = None

class SeniorDevSummary(SeniorDev):
    chats: None = None

class ScenarioSummary(BaseModel):
    id: int
    title: str
    short_desc: str
    categories: List[Category]
    stakeholders: List[StakeholderSummary]
    seniordev: SeniorDevSummary