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