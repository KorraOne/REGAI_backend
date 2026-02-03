from __future__ import annotations

from typing import Iterable, Optional, Sequence

from sqlalchemy.orm import Session

from db.models import (
    Categories,
    MarkingStatus,
    Requirements,
    ScenarioCategories,
    Scenarios,
    Stakeholder,
)


class ScenariosService:
    """
    Handles scenario-related business logic:
    - create scenarios
    - add requirements
    - assign stakeholders
    - manage categories
    - handle templates
    """

    def __init__(
        self,
        scenarios_repo,
        requirements_repo,
        stakeholders_repo,
        categories_repo,
        scenario_categories_repo,
        templates_repo,
    ):
        self.scenarios = scenarios_repo
        self.requirements = requirements_repo
        self.stakeholders = stakeholders_repo
        self.categories = categories_repo
        self.scenario_categories = scenario_categories_repo
        self.templates = templates_repo

    # ---------------------------------------------------------
    # SCENARIO CRUD
    # ---------------------------------------------------------
    def create_scenario(
        self,
        *,
        owner_id: int,
        title: str,
        short_desc: Optional[str] = None,
        long_desc: Optional[str] = None,
        marking_status: Optional[MarkingStatus | str] = None,
        category_ids: Optional[Iterable[int]] = None,
        stakeholders: Optional[Sequence[dict]] = None,
        requirements: Optional[Sequence[dict]] = None,
    ):
        scenario_payload = {
            "owner_id": owner_id,
            "title": title,
            "short_desc": short_desc,
            "long_desc": long_desc,
        }

        if marking_status is not None:
            scenario_payload["marking_status"] = (
                MarkingStatus(marking_status) if isinstance(marking_status, str) else marking_status
            )

        scenario = self.scenarios.create(**scenario_payload)

        if category_ids:
            self.set_categories(scenario.id, category_ids)

        if stakeholders:
            for stakeholder in stakeholders:
                self.add_stakeholder(
                    scenario.id,
                    name=stakeholder.get("name"),
                    role=stakeholder.get("role"),
                    desc=stakeholder.get("desc"),
                    prompt=stakeholder.get("prompt"),
                    is_senior_dev=stakeholder.get("is_senior_dev", False),
                )

        if requirements:
            for requirement in requirements:
                self.add_requirement(
                    scenario.id,
                    type=requirement.get("type"),
                    requirement=requirement.get("requirement"),
                    info=requirement.get("info"),
                )

        return scenario

    def get_scenario(self, scenario_id: int, *, include_deleted: bool = False):
        if not include_deleted:
            return self.scenarios.get(scenario_id)

        return (
            self._db()
            .query(Scenarios)
            .filter(Scenarios.id == scenario_id)
            .first()
        )

    def list_scenarios(self, *, owner_id: Optional[int] = None, include_deleted: bool = False):
        query = self._db().query(Scenarios)
        if not include_deleted:
            query = query.filter(Scenarios.deleted_at.is_(None))
        if owner_id is not None:
            query = query.filter(Scenarios.owner_id == owner_id)
        return query.all()

    def update_scenario(
        self,
        scenario_id: int,
        *,
        data: Optional[dict] = None,
        category_ids: Optional[Iterable[int]] = None,
    ):
        if data is None:
            data = {}

        if "marking_status" in data and isinstance(data["marking_status"], str):
            data = data.copy()
            data["marking_status"] = MarkingStatus(data["marking_status"])

        scenario = self.scenarios.update(scenario_id, **data)

        if scenario and category_ids is not None:
            self.set_categories(scenario_id, category_ids)

        return scenario

    def delete_scenario(self, scenario_id: int):
        return self.scenarios.delete(scenario_id)

    def restore_scenario(self, scenario_id: int):
        return self.scenarios.restore(scenario_id)

    # ---------------------------------------------------------
    # REQUIREMENTS
    # ---------------------------------------------------------
    def list_requirements(self, scenario_id: int, *, include_deleted: bool = False):
        query = self._db().query(Requirements).filter(Requirements.scenario_id == scenario_id)
        if not include_deleted:
            query = query.filter(Requirements.deleted_at.is_(None))
        return query.all()

    def add_requirement(
        self,
        scenario_id: int,
        *,
        type: str,
        requirement: Optional[str] = None,
        info: Optional[str] = None,
    ):
        if not type:
            raise ValueError("Requirement type is required")

        text = requirement if requirement is not None else info
        if text is None:
            raise ValueError("Requirement text is required")

        payload = {
            "scenario_id": scenario_id,
            "type": type,
            "requirement": text,
        }
        return self.requirements.create(**payload)

    def update_requirement(self, requirement_id: int, data: dict):
        payload = data.copy()
        if "info" in payload and "requirement" not in payload:
            payload["requirement"] = payload.pop("info")
        return self.requirements.update(requirement_id, **payload)

    def delete_requirement(self, requirement_id: int):
        return self.requirements.delete(requirement_id)

    def restore_requirement(self, requirement_id: int):
        return self.requirements.restore(requirement_id)

    def clear_requirements(self, scenario_id: int):
        requirements = self.list_requirements(scenario_id)
        for req in requirements:
            self.requirements.delete(req.id)
        return len(requirements)

    # ---------------------------------------------------------
    # STAKEHOLDERS
    # ---------------------------------------------------------
    def list_stakeholders(self, scenario_id: int, *, include_deleted: bool = False):
        query = self._db().query(Stakeholder).filter(Stakeholder.scenario_id == scenario_id)
        if not include_deleted:
            query = query.filter(Stakeholder.deleted_at.is_(None))
        return query.all()

    def add_stakeholder(
        self,
        scenario_id: int,
        *,
        name: Optional[str],
        role: Optional[str],
        desc: Optional[str] = None,
        prompt: Optional[str] = None,
        is_senior_dev: bool = False,
    ):
        if not name or not role:
            raise ValueError("Stakeholder name and role are required")

        payload = {
            "scenario_id": scenario_id,
            "name": name,
            "role": role,
            "desc": desc,
            "prompt": prompt or desc or "",
            "is_senior_dev": is_senior_dev,
        }
        return self.stakeholders.create(**payload)

    def update_stakeholder(self, stakeholder_id: int, data: dict):
        payload = data.copy()
        if "prompt" not in payload and "desc" in payload:
            payload["prompt"] = payload["desc"]
        return self.stakeholders.update(stakeholder_id, **payload)

    def delete_stakeholder(self, stakeholder_id: int):
        return self.stakeholders.delete(stakeholder_id)

    def restore_stakeholder(self, stakeholder_id: int):
        return self.stakeholders.restore(stakeholder_id)

    # ---------------------------------------------------------
    # CATEGORIES
    # ---------------------------------------------------------
    def list_categories(self, *, include_deleted: bool = False):
        query = self._db().query(Categories)
        if not include_deleted:
            query = query.filter(Categories.deleted_at.is_(None))
        return query.all()

    def create_category(self, name: str):
        return self.categories.create(name=name)

    def update_category(self, category_id: int, data: dict):
        return self.categories.update(category_id, **data)

    def delete_category(self, category_id: int):
        return self.categories.delete(category_id)

    def restore_category(self, category_id: int):
        return self.categories.restore(category_id)

    def set_categories(self, scenario_id: int, category_ids: Iterable[int]):
        """
        Replace scenario categories with the provided list of IDs.
        Restores soft-deleted links where possible instead of recreating them.
        """
        desired_ids = set(category_ids or [])
        db = self._db()

        links = (
            db.query(ScenarioCategories)
            .filter(ScenarioCategories.scenario_id == scenario_id)
            .all()
        )

        active_links = {link.category_id: link for link in links if link.deleted_at is None}
        deleted_links = {link.category_id: link for link in links if link.deleted_at is not None}

        for category_id in desired_ids:
            if category_id in active_links:
                continue

            if category_id in deleted_links:
                link = deleted_links[category_id]
                link.deleted_at = None
                db.add(link)
                db.commit()
                db.refresh(link)
                continue

            category = self.categories.get(category_id)
            if not category:
                raise ValueError(f"Category {category_id} not found")

            self.scenario_categories.create(scenario_id=scenario_id, category_id=category_id)

        for category_id, link in active_links.items():
            if category_id not in desired_ids:
                self.scenario_categories.delete(link.id)

        return self.scenario_categories.list(scenario_id=scenario_id)

    def add_category_to_scenario(self, scenario_id: int, category_id: int):
        links = self.scenario_categories.list(scenario_id=scenario_id)
        desired_ids = {link.category_id for link in links}
        desired_ids.add(category_id)
        return self.set_categories(scenario_id, desired_ids)

    def remove_category_from_scenario(self, scenario_id: int, category_id: int):
        links = self.scenario_categories.list(scenario_id=scenario_id)
        remaining = [link.category_id for link in links if link.category_id != category_id]
        return self.set_categories(scenario_id, remaining)

    # ---------------------------------------------------------
    # TEMPLATES
    # ---------------------------------------------------------
    def list_templates(self):
        return self.templates.list()

    def get_template(self, template_id: int):
        return self.templates.get(template_id)

    def create_template(self, data: dict):
        return self.templates.create(**data)

    def update_template(self, template_id: int, data: dict):
        return self.templates.update(template_id, **data)

    def delete_template(self, template_id: int):
        return self.templates.delete(template_id)

    def restore_template(self, template_id: int):
        return self.templates.restore(template_id)

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _db(self) -> Session:
        return self.scenarios.db