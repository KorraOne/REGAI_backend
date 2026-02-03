"""Tests for ChatHistoryRepository and ChatMessageRepository."""
import pytest


class TestChatHistoryRepository:
    """ChatHistoryRepository."""

    def test_create(self, chat_history_repo, stakeholders_repo, sample_scenario):
        st = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="Stakeholder",
            role="Role",
            prompt="Prompt",
        )
        h = chat_history_repo.create(stakeholder_id=st.id)
        assert h.id is not None
        assert h.stakeholder_id == st.id

    def test_list_by_stakeholder(
        self, chat_history_repo, stakeholders_repo, sample_scenario
    ):
        st = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="S",
            role="R",
            prompt="P",
        )
        chat_history_repo.create(stakeholder_id=st.id)
        histories = chat_history_repo.list(stakeholder_id=st.id)
        assert len(histories) == 1


class TestChatMessageRepository:
    """ChatMessageRepository."""

    def test_create(
        self,
        chat_message_repo,
        chat_history_repo,
        stakeholders_repo,
        sample_scenario,
    ):
        st = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="S",
            role="R",
            prompt="P",
        )
        h = chat_history_repo.create(stakeholder_id=st.id)
        msg = chat_message_repo.create(
            chat_history_id=h.id,
            sent_by="User",
            message="Hello",
        )
        assert msg.id is not None
        assert msg.chat_history_id == h.id
        assert msg.sent_by == "User"
        assert msg.message == "Hello"

    def test_list_by_history(
        self,
        chat_message_repo,
        chat_history_repo,
        stakeholders_repo,
        sample_scenario,
    ):
        st = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="S",
            role="R",
            prompt="P",
        )
        h = chat_history_repo.create(stakeholder_id=st.id)
        chat_message_repo.create(
            chat_history_id=h.id,
            sent_by="User",
            message="Hi",
        )
        msgs = chat_message_repo.list(chat_history_id=h.id)
        assert len(msgs) == 1
