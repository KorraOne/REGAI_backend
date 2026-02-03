"""Fixtures for service layer tests."""
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

from app.services.users_service import UsersService
from app.services.classes_service import ClassesService
from app.services.scenarios_service import ScenariosService
from app.services.chats_service import ChatsService
from app.services.feedback_service import FeedbackService

from tests.conftest import make_user_data


# --- Repositories (from db/conftest) ---
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


# --- Services ---
@pytest.fixture
def users_service(users_repo, students_repo, class_teacher_repo):
    return UsersService(users_repo, students_repo, class_teacher_repo)


@pytest.fixture
def classes_service(class_repo, students_repo, class_teacher_repo):
    return ClassesService(class_repo, students_repo, class_teacher_repo)


@pytest.fixture
def scenarios_service(
    scenarios_repo,
    requirements_repo,
    stakeholders_repo,
    categories_repo,
    scenario_categories_repo,
    templates_repo,
):
    return ScenariosService(
        scenarios_repo,
        requirements_repo,
        stakeholders_repo,
        categories_repo,
        scenario_categories_repo,
        templates_repo,
    )


@pytest.fixture
def chats_service(chat_history_repo, chat_message_repo):
    return ChatsService(chat_history_repo, chat_message_repo)


@pytest.fixture
def feedback_service(
    feedback_repo,
    requirements_repo,
    chat_message_repo,
    scenarios_repo,
):
    return FeedbackService(
        feedback_repo,
        requirements_repo,
        chat_message_repo,
        scenarios_repo,
    )


# --- Sample data ---
@pytest.fixture
def sample_user(users_repo):
    return users_repo.create(**make_user_data())


@pytest.fixture
def sample_class(class_repo):
    return class_repo.create(name="Test Class")


@pytest.fixture
def sample_scenario(scenarios_repo, sample_user):
    return scenarios_repo.create(
        owner_id=sample_user.id,
        title="Test Scenario",
        short_desc="Short",
        long_desc="Long",
    )
