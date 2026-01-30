from db.crud.base_repository import BaseRepository
from db.models import (
    Scenarios,
    Requirements,
    Stakeholder,
    Categories,
    ScenarioCategories,
    SeniorDevTemplates
)

class ScenariosRepository(BaseRepository):
    model = Scenarios

class RequirementsRepository(BaseRepository):
    model = Requirements

class StakeholdersRepository(BaseRepository):
    model = Stakeholder

class CategoriesRepository(BaseRepository):
    model = Categories

class ScenarioCategoriesRepository(BaseRepository):
    model = ScenarioCategories

class SeniorDevTemplatesRepository(BaseRepository):
    model = SeniorDevTemplates