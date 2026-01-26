from pydantic import BaseModel
from .chat import ChatHistory

class Stakeholder(BaseModel):
    id: int
    name: str
    role: str
    desc: str
    chats: ChatHistory

class SeniorDev(Stakeholder):
    role: str = "Senior Developer"