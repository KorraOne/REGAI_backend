from __future__ import annotations

from collections import Counter
from typing import Optional

from db.models import MarkingStatus


class FeedbackService:
    """
    Handles feedback-related business logic:
    - attach feedback to requirements
    - compute marking results
    - retrieve feedback for scenarios
    """

    def __init__(
        self,
        feedback_repo,
        requirements_repo=None,
        chat_message_repo=None,
        scenarios_repo=None,
    ):
        self.feedback = feedback_repo
        self.requirements = requirements_repo
        self.chat_messages = chat_message_repo
        self.scenarios = scenarios_repo

    # ---------------------------------------------------------
    # FEEDBACK CREATION
    # ---------------------------------------------------------
    def add_feedback_to_requirement(self, requirement_id: int, feedback_text: str, *, scenario_id: Optional[int] = None):
        """
        Attach feedback to a requirement. Automatically resolves scenario_id when possible.
        """
        scenario_id = self._resolve_requirement_scenario(requirement_id, scenario_id)
        if scenario_id is None:
            raise ValueError("scenario_id is required when requirements repository is unavailable")

        payload = {
            "feedback": feedback_text,
            "scenario_id": scenario_id,
            "requirement_id": requirement_id,
            "chat_message_id": None,
        }
        return self.feedback.create(**payload)

    def add_feedback_to_message(self, chat_message_id: int, feedback_text: str, *, scenario_id: Optional[int] = None):
        """
        Attach feedback to a chat message. Automatically resolves scenario_id when possible.
        """
        scenario_id = self._resolve_message_scenario(chat_message_id, scenario_id)
        if scenario_id is None:
            raise ValueError("scenario_id is required when chat message repository is unavailable")

        payload = {
            "feedback": feedback_text,
            "scenario_id": scenario_id,
            "requirement_id": None,
            "chat_message_id": chat_message_id,
        }
        return self.feedback.create(**payload)

    def add_general_feedback(self, scenario_id: int, feedback_text: str):
        """Create feedback that is attached only to the scenario."""
        payload = {
            "feedback": feedback_text,
            "scenario_id": scenario_id,
            "requirement_id": None,
            "chat_message_id": None,
        }
        return self.feedback.create(**payload)

    # ---------------------------------------------------------
    # FEEDBACK RETRIEVAL
    # ---------------------------------------------------------
    def get_feedback(self, feedback_id: int):
        return self.feedback.get(feedback_id)

    def list_feedback_for_scenario(self, scenario_id: int):
        return self.feedback.list(scenario_id=scenario_id)

    def list_feedback_for_requirement(self, requirement_id: int):
        return self.feedback.list(requirement_id=requirement_id)

    def list_feedback_for_message(self, chat_message_id: int):
        return self.feedback.list(chat_message_id=chat_message_id)

    def delete_feedback(self, feedback_id: int):
        return self.feedback.delete(feedback_id)

    def restore_feedback(self, feedback_id: int):
        return self.feedback.restore(feedback_id)

    # ---------------------------------------------------------
    # MARKING / SUMMARY
    # ---------------------------------------------------------
    def compute_marking_summary(self, scenario_id: int):
        """
        Compute aggregate feedback data for a scenario.
        Returns counts per requirement and chat message plus coverage insights.
        """
        feedback_items = self.list_feedback_for_scenario(scenario_id)
        per_requirement = Counter(
            item.requirement_id for item in feedback_items if item.requirement_id is not None
        )
        per_chat_message = Counter(
            item.chat_message_id for item in feedback_items if item.chat_message_id is not None
        )

        coverage = None
        if self.requirements:
            requirements = self.requirements.list(scenario_id=scenario_id)
            total_requirements = len(requirements)
            if total_requirements:
                covered = sum(1 for req in requirements if per_requirement.get(req.id))
                coverage = {
                    "total_requirements": total_requirements,
                    "requirements_with_feedback": covered,
                    "coverage_ratio": covered / total_requirements,
                }
            else:
                coverage = {"total_requirements": 0, "requirements_with_feedback": 0, "coverage_ratio": 0.0}

        return {
            "total_feedback": len(feedback_items),
            "per_requirement": dict(per_requirement),
            "per_chat_message": dict(per_chat_message),
            "coverage": coverage,
        }

    def set_marking_status(self, scenario_id: int, status: MarkingStatus | str):
        """
        Update the scenario's marking status. Requires a scenarios repository.
        """
        if self.scenarios is None:
            raise RuntimeError("Scenarios repository is required to update marking status")

        status_enum = MarkingStatus(status) if isinstance(status, str) else status
        return self.scenarios.update(scenario_id, marking_status=status_enum)

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _resolve_requirement_scenario(self, requirement_id: int, fallback_scenario_id: Optional[int]):
        if self.requirements is None:
            return fallback_scenario_id

        requirement = self.requirements.get(requirement_id)
        if requirement is None:
            raise ValueError(f"Requirement {requirement_id} not found")

        return requirement.scenario_id

    def _resolve_message_scenario(self, chat_message_id: int, fallback_scenario_id: Optional[int]):
        if self.chat_messages is None:
            return fallback_scenario_id

        message = self.chat_messages.get(chat_message_id)
        if message is None:
            raise ValueError(f"Chat message {chat_message_id} not found")

        history = message.history
        stakeholder = getattr(history, "stakeholder", None)
        scenario = getattr(stakeholder, "scenario", None) if stakeholder else None

        if scenario:
            return scenario.id

        if fallback_scenario_id is None:
            raise ValueError("Unable to infer scenario_id for chat feedback")
        return fallback_scenario_id