from db.crud.base_repository import BaseRepository
from db.models import ChatHistory, ChatMessage

class ChatHistoryRepository(BaseRepository):
    model = ChatHistory

class ChatMessageRepository(BaseRepository):
    model = ChatMessage