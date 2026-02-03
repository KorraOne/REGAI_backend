"""Tests for ChatsService."""
import pytest


class TestChatsServiceHistory:
    """ChatsService chat history operations."""

    def test_get_history_for_stakeholder_creates_if_missing(
        self,
        chats_service,
        stakeholders_repo,
        sample_scenario,
    ):
        st = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="S",
            role="R",
            prompt="P",
        )
        h = chats_service.get_history_for_stakeholder(st.id, create=True)
        assert h is not None
        assert h.stakeholder_id == st.id

    def test_get_history_for_stakeholder_returns_none_if_not_create(
        self,
        chats_service,
        stakeholders_repo,
        sample_scenario,
    ):
        st = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="S",
            role="R",
            prompt="P",
        )
        h = chats_service.get_history_for_stakeholder(st.id, create=False)
        assert h is None

    def test_append_message(
        self,
        chats_service,
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
        msg = chats_service.append_message(
            h.id,
            sent_by="User",
            message="Hello",
        )
        assert msg.id is not None
        assert msg.message == "Hello"
        msgs = chats_service.list_messages(h.id)
        assert len(msgs) == 1

    def test_append_message_raises_for_invalid_history(
        self, chats_service
    ):
        with pytest.raises(ValueError, match="not found"):
            chats_service.append_message(
                99999,
                sent_by="User",
                message="Hi",
            )

    def test_list_messages(
        self,
        chats_service,
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
        chats_service.append_message(h.id, sent_by="U", message="M1")
        chats_service.append_message(h.id, sent_by="U", message="M2")
        msgs = chats_service.list_messages(h.id)
        assert len(msgs) == 2

    def test_get_last_message(
        self,
        chats_service,
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
        chats_service.append_message(h.id, sent_by="U", message="First")
        chats_service.append_message(h.id, sent_by="U", message="Last")
        last = chats_service.get_last_message(h.id)
        assert last is not None
        assert last.message == "Last"

    def test_clear_history(
        self,
        chats_service,
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
        chats_service.append_message(h.id, sent_by="U", message="M1")
        count = chats_service.clear_history(h.id)
        assert count == 1
        assert len(chats_service.list_messages(h.id)) == 0
