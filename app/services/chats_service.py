from __future__ import annotations

from typing import Iterable, Optional


class ChatsService:
    """
    Handles chat-related business logic:
    - create chat history
    - append messages
    - list messages
    """

    def __init__(self, chat_history_repo, chat_message_repo):
        self.history = chat_history_repo
        self.messages = chat_message_repo

    # ---------------------------------------------------------
    # CHAT HISTORIES
    # ---------------------------------------------------------
    def get_history(self, history_id: int):
        """Return a single active chat history."""
        return self.history.get(history_id)

    def get_history_for_stakeholder(self, stakeholder_id: int, *, create: bool = True):
        """
        Return (and optionally create) the chat history for a stakeholder.
        """
        histories = self.history.list(stakeholder_id=stakeholder_id)
        if histories:
            # Always return the most recently created active history.
            return max(histories, key=lambda h: getattr(h, "id", 0))

        if not create:
            return None

        return self.history.create(stakeholder_id=stakeholder_id)

    def list_histories(self, *, stakeholder_id: Optional[int] = None):
        """List chat histories, optionally filtered by stakeholder."""
        filters = {}
        if stakeholder_id is not None:
            filters["stakeholder_id"] = stakeholder_id
        return self.history.list(**filters)

    def delete_history(self, history_id: int):
        """Soft-delete a chat history and its messages."""
        history = self.get_history(history_id)
        if not history:
            return None

        for message in self.list_messages(history_id):
            self.delete_message(message.id)

        return self.history.delete(history_id)

    def restore_history(self, history_id: int):
        """Restore a previously deleted chat history."""
        return self.history.restore(history_id)

    # ---------------------------------------------------------
    # CHAT MESSAGES
    # ---------------------------------------------------------
    def append_message(self, history_id: int, *, sent_by: str, message: str):
        """
        Append a message to a chat history.
        Raises ValueError if the history does not exist.
        """
        history = self.get_history(history_id)
        if not history:
            raise ValueError(f"Chat history {history_id} not found")

        payload = {
            "chat_history_id": history_id,
            "sent_by": sent_by,
            "message": message,
        }
        return self.messages.create(**payload)

    def list_messages(self, history_id: int):
        """Return all active messages for a chat history."""
        history = self.get_history(history_id)
        if not history:
            return []

        return self.messages.list(chat_history_id=history_id)

    def get_last_message(self, history_id: int):
        """Return the newest active message in a history."""
        messages = self.list_messages(history_id)
        if not messages:
            return None

        return max(messages, key=lambda m: getattr(m, "id", 0))

    def delete_message(self, message_id: int):
        """Soft-delete a single chat message."""
        return self.messages.delete(message_id)

    def delete_messages(self, message_ids: Iterable[int]):
        """Soft-delete multiple chat messages."""
        results = []
        for message_id in message_ids:
            results.append(self.delete_message(message_id))
        return results

    def clear_history(self, history_id: int):
        """
        Soft-delete all messages in a chat history.
        Returns number of messages cleared.
        """
        messages = self.list_messages(history_id)
        for message in messages:
            self.delete_message(message.id)
        return len(messages)

    def restore_message(self, message_id: int):
        """Restore a soft-deleted chat message."""
        return self.messages.restore(message_id)