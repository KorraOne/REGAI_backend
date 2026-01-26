from typing import List, Literal
from pydantic import BaseModel

class ChatMessage(BaseModel):
    id: int
    sender: Literal["User", "LLM"]
    timestamp: float
    message: str

class ChatHistory(BaseModel):
    id: int
    messages: List[ChatMessage]