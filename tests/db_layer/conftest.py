"""Fixtures for db layer tests."""
import pytest

from db.crud.users import UsersRepository, StudentsOfClassRepository, ClassTeacherRepository
from db.crud.classes import ClassRepository
from db.crud.scenarios import (
    ScenariosRepository,
    RequirementsRepository,
    StakeholdersRepository,
    CategoriesRepository,
    ScenarioCategoriesRepository,
    SeniorDevTemplatesRepository,
)
from db.crud.chats import ChatHistoryRepository, ChatMessageRepository
from db.crud.feedback import FeedbackReferenceRepository

from tests.conftest import make_user_data


@pytest.fixture
def users_repo(db_session):
    return UsersRepository(db_session)


@pytest.fixture
def students_repo(db_session):
    return StudentsOfClassRepository(db_session)


@pytest.fixture
def class_teacher_repo(db_session):
    return ClassTeacherRepository(db_session)


@pytest.fixture
def class_repo(db_session):
    return ClassRepository(db_session)


@pytest.fixture
def scenarios_repo(db_session):
    return ScenariosRepository(db_session)


@pytest.fixture
def requirements_repo(db_session):
    return RequirementsRepository(db_session)


@pytest.fixture
def stakeholders_repo(db_session):
    return StakeholdersRepository(db_session)


@pytest.fixture
def categories_repo(db_session):
    return CategoriesRepository(db_session)


@pytest.fixture
def scenario_categories_repo(db_session):
    return ScenarioCategoriesRepository(db_session)


@pytest.fixture
def templates_repo(db_session):
    return SeniorDevTemplatesRepository(db_session)


@pytest.fixture
def chat_history_repo(db_session):
    return ChatHistoryRepository(db_session)


@pytest.fixture
def chat_message_repo(db_session):
    return ChatMessageRepository(db_session)


@pytest.fixture
def feedback_repo(db_session):
    return FeedbackReferenceRepository(db_session)


@pytest.fixture
def sample_user(users_repo):
    """Create and return a test user."""
    return users_repo.create(**make_user_data())


@pytest.fixture
def sample_class(class_repo):
    """Create and return a test class."""
    return class_repo.create(name="Test Class")


@pytest.fixture
def sample_scenario(scenarios_repo, sample_user):
    """Create and return a test scenario."""
    return scenarios_repo.create(
        owner_id=sample_user.id,
        title="Test Scenario",
        short_desc="Short",
        long_desc="Long",
    )
