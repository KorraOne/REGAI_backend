"""Tests for FeedbackService."""
import pytest


class TestFeedbackServiceCreation:
    """FeedbackService feedback creation."""

    def test_add_general_feedback(
        self, feedback_service, sample_scenario
    ):
        f = feedback_service.add_general_feedback(
            sample_scenario.id, "General comment"
        )
        assert f.id is not None
        assert f.feedback == "General comment"
        assert f.scenario_id == sample_scenario.id
        assert f.requirement_id is None

    def test_add_feedback_to_requirement(
        self,
        feedback_service,
        sample_scenario,
        requirements_repo,
    ):
        req = requirements_repo.create(
            scenario_id=sample_scenario.id,
            type="functional",
            requirement="R1",
        )
        f = feedback_service.add_feedback_to_requirement(
            req.id, "Feedback on R1"
        )
        assert f.requirement_id == req.id
        assert f.feedback == "Feedback on R1"

    def test_add_feedback_to_message(
        self,
        feedback_service,
        chat_history_repo,
        chat_message_repo,
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
        f = feedback_service.add_feedback_to_message(
            msg.id, "Feedback on message", scenario_id=sample_scenario.id
        )
        assert f.chat_message_id == msg.id


class TestFeedbackServiceRetrieval:
    """FeedbackService retrieval."""

    def test_list_feedback_for_scenario(
        self, feedback_service, sample_scenario
    ):
        feedback_service.add_general_feedback(
            sample_scenario.id, "F1"
        )
        items = feedback_service.list_feedback_for_scenario(
            sample_scenario.id
        )
        assert len(items) == 1

    def test_delete_feedback(
        self, feedback_service, sample_scenario
    ):
        f = feedback_service.add_general_feedback(
            sample_scenario.id, "F"
        )
        feedback_service.delete_feedback(f.id)
        assert feedback_service.get_feedback(f.id) is None

    def test_restore_feedback(
        self, feedback_service, sample_scenario
    ):
        f = feedback_service.add_general_feedback(
            sample_scenario.id, "F"
        )
        feedback_service.delete_feedback(f.id)
        restored = feedback_service.restore_feedback(f.id)
        assert restored.deleted_at is None


class TestFeedbackServiceMarking:
    """FeedbackService marking and summary."""

    def test_compute_marking_summary(
        self,
        feedback_service,
        sample_scenario,
        requirements_repo,
    ):
        req = requirements_repo.create(
            scenario_id=sample_scenario.id,
            type="functional",
            requirement="R1",
        )
        feedback_service.add_feedback_to_requirement(
            req.id, "FB"
        )
        summary = feedback_service.compute_marking_summary(
            sample_scenario.id
        )
        assert summary["total_feedback"] == 1
        assert summary["coverage"] is not None
        assert summary["coverage"]["total_requirements"] == 1
        assert summary["coverage"]["requirements_with_feedback"] == 1

    def test_set_marking_status(
        self, feedback_service, sample_scenario
    ):
        s = feedback_service.set_marking_status(
            sample_scenario.id, "submitted"
        )
        assert s.marking_status.value == "submitted"
