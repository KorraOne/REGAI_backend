from pydantic import BaseModel
from typing import List
from app.models.scenarios.domain.category import Category


class StakeholderSummary(BaseModel):
    id: int
    name: str
    role: str
    desc: str


class SeniorDevSummary(BaseModel):
    id: int
    name: str
    role: str
    desc: str


class ScenarioSummary(BaseModel):
    id: int
    title: str
    short_desc: str
    categories: List[Category] = []
    stakeholders: List[StakeholderSummary]
    seniordev: SeniorDevSummary