"""Tests for ScenariosRepository, RequirementsRepository, StakeholdersRepository, etc."""
import pytest

from db.models import MarkingStatus


class TestScenariosRepository:
    """ScenariosRepository CRUD."""

    def test_create(self, scenarios_repo, sample_user):
        s = scenarios_repo.create(
            owner_id=sample_user.id,
            title="My Scenario",
            short_desc="Short",
            long_desc="Long",
        )
        assert s.id is not None
        assert s.title == "My Scenario"
        assert s.marking_status == MarkingStatus.draft

    def test_get_and_list(self, scenarios_repo, sample_scenario, sample_user):
        s = scenarios_repo.get(sample_scenario.id)
        assert s is not None
        assert s.owner_id == sample_user.id
        all_s = scenarios_repo.list(owner_id=sample_user.id)
        assert len(all_s) >= 1

    def test_update(self, scenarios_repo, sample_scenario):
        updated = scenarios_repo.update(
            sample_scenario.id,
            title="Updated",
            marking_status=MarkingStatus.submitted,
        )
        assert updated.title == "Updated"
        assert updated.marking_status == MarkingStatus.submitted

    def test_delete_and_restore(self, scenarios_repo, sample_scenario):
        scenarios_repo.delete(sample_scenario.id)
        assert scenarios_repo.get(sample_scenario.id) is None
        restored = scenarios_repo.restore(sample_scenario.id)
        assert restored.deleted_at is None


class TestRequirementsRepository:
    """RequirementsRepository."""

    def test_create(self, requirements_repo, sample_scenario):
        r = requirements_repo.create(
            scenario_id=sample_scenario.id,
            type="functional",
            requirement="User can login",
        )
        assert r.id is not None
        assert r.scenario_id == sample_scenario.id
        assert r.type == "functional"
        assert r.requirement == "User can login"

    def test_list_by_scenario(self, requirements_repo, sample_scenario):
        requirements_repo.create(
            scenario_id=sample_scenario.id,
            type="functional",
            requirement="R1",
        )
        reqs = requirements_repo.list(scenario_id=sample_scenario.id)
        assert len(reqs) == 1


class TestStakeholdersRepository:
    """StakeholdersRepository."""

    def test_create(self, stakeholders_repo, sample_scenario):
        s = stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="Alice",
            role="Product Owner",
            desc="Owns the product",
            prompt="You are Alice",
        )
        assert s.id is not None
        assert s.name == "Alice"
        assert s.prompt == "You are Alice"

    def test_list_by_scenario(self, stakeholders_repo, sample_scenario):
        stakeholders_repo.create(
            scenario_id=sample_scenario.id,
            name="Bob",
            role="Dev",
            prompt="You are Bob",
        )
        sts = stakeholders_repo.list(scenario_id=sample_scenario.id)
        assert len(sts) == 1


class TestCategoriesRepository:
    """CategoriesRepository."""

    def test_create(self, categories_repo):
        c = categories_repo.create(name="Education")
        assert c.id is not None
        assert c.name == "Education"

    def test_list(self, categories_repo):
        categories_repo.create(name="Cat1")
        cats = categories_repo.list()
        assert len(cats) >= 1


class TestScenarioCategoriesRepository:
    """ScenarioCategories many-to-many."""

    def test_create(self, scenario_categories_repo, sample_scenario, categories_repo):
        cat = categories_repo.create(name="Cat")
        link = scenario_categories_repo.create(
            scenario_id=sample_scenario.id,
            category_id=cat.id,
        )
        assert link.id is not None
        assert link.scenario_id == sample_scenario.id
        assert link.category_id == cat.id

    def test_list_by_scenario(
        self, scenario_categories_repo, sample_scenario, categories_repo
    ):
        cat = categories_repo.create(name="Cat")
        scenario_categories_repo.create(
            scenario_id=sample_scenario.id,
            category_id=cat.id,
        )
        links = scenario_categories_repo.list(scenario_id=sample_scenario.id)
        assert len(links) == 1


class TestSeniorDevTemplatesRepository:
    """SeniorDevTemplatesRepository."""

    def test_create(self, templates_repo):
        t = templates_repo.create(
            name="Senior Dev",
            role="Developer",
            desc="Senior dev template",
            prompt="You are a senior developer",
        )
        assert t.id is not None
        assert t.name == "Senior Dev"
