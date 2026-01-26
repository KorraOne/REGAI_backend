from pydantic import BaseModel
from typing import Literal

class Requirement(BaseModel):
    id: int
    type: Literal["functional", "non-functional"]
    info: str