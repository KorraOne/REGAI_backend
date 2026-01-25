from typing import Literal
from pydantic import BaseModel

# -------------------------
# Shared lightweight models
# -------------------------

class StakeholderSummary(BaseModel):
    id: int
    name: str
    role: str

class SeniordevSummary(BaseModel):
    id: int
    name: str

class ScenarioSummary(BaseModel):
    id: int
    title: str
    short_desc: str
    categories: list[str]
    stakeholders: list[StakeholderSummary]
    seniordev: SeniordevSummary


# -------------------------
# Full detail models
# -------------------------

class ChatHistory(BaseModel):
    messages: list[str]

class Stakeholder(BaseModel):
    id: int
    name: str
    role: str
    chat_history: ChatHistory

class Seniordev(BaseModel):
    id: int
    name: str
    chat_history: ChatHistory

class Requirement(BaseModel):
    type: Literal["FR", "NFR"]
    info: str

class Requirements(BaseModel):
    items: list[Requirement]


class ScenarioDetail(BaseModel):
    id: int
    title: str
    short_desc: str
    long_desc: str
    categories: list[str]
    stakeholders: list[Stakeholder]
    seniordev: Seniordev
    requirements: Requirements


# -------------------------
# Shared base for create/edit
# -------------------------

class ScenarioBase(BaseModel):
    title: str | None = None
    short_desc: str | None = None
    long_desc: str | None = None
    categories: list[str] | None = None

    class Config:
        extra = "forbid"

class CreateScenarioRequest(ScenarioBase):
    title: str
    short_desc: str
    long_desc: str
    categories: list[str]

class EditScenarioRequest(ScenarioBase):
    pass