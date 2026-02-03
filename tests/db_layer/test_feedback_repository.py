"""Tests for FeedbackReferenceRepository."""
import pytest


class TestFeedbackReferenceRepository:
    """FeedbackReferenceRepository."""

    def test_create_general(
        self, feedback_repo, sample_scenario
    ):
        f = feedback_repo.create(
            feedback="General feedback text",
            scenario_id=sample_scenario.id,
            requirement_id=None,
            chat_message_id=None,
        )
        assert f.id is not None
        assert f.feedback == "General feedback text"
        assert f.scenario_id == sample_scenario.id
        assert f.requirement_id is None

    def test_create_with_requirement(
        self, feedback_repo, sample_scenario, requirements_repo
    ):
        req = requirements_repo.create(
            scenario_id=sample_scenario.id,
            type="functional",
            requirement="R1",
        )
        f = feedback_repo.create(
            feedback="Feedback on R1",
            scenario_id=sample_scenario.id,
            requirement_id=req.id,
            chat_message_id=None,
        )
        assert f.requirement_id == req.id

    def test_list_by_scenario(self, feedback_repo, sample_scenario):
        feedback_repo.create(
            feedback="F1",
            scenario_id=sample_scenario.id,
            requirement_id=None,
            chat_message_id=None,
        )
        items = feedback_repo.list(scenario_id=sample_scenario.id)
        assert len(items) == 1

    def test_delete_and_restore(self, feedback_repo, sample_scenario):
        f = feedback_repo.create(
            feedback="F",
            scenario_id=sample_scenario.id,
            requirement_id=None,
            chat_message_id=None,
        )
        feedback_repo.delete(f.id)
        assert feedback_repo.get(f.id) is None
        restored = feedback_repo.restore(f.id)
        assert restored.deleted_at is None
