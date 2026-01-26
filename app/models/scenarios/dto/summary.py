from pydantic import BaseModel
from typing import List, Dict

class ScenarioSummary(BaseModel):
    id: int
    title: str
    short_desc: str
    categories: List[str]
    stakeholders: List[Dict]
    seniordev: Dict