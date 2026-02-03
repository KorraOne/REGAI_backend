"""Tests for UsersRepository, StudentsOfClassRepository, ClassTeacherRepository."""
import pytest

from db.models import MarkingStatus

from tests.conftest import make_user_data


class TestUsersRepository:
    """UsersRepository CRUD and soft delete."""

    def test_create_user(self, users_repo):
        user = users_repo.create(**make_user_data())
        assert user.id is not None
        assert user.fname == "Test"
        assert user.lname == "User"
        assert user.username == "testuser"
        assert user.email == "test@example.com"
        assert user.deleted_at is None
        assert user.created_at is not None

    def test_get_returns_active_user(self, users_repo, sample_user):
        user = users_repo.get(sample_user.id)
        assert user is not None
        assert user.id == sample_user.id

    def test_get_returns_none_for_deleted_user(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        assert users_repo.get(sample_user.id) is None

    def test_get_returns_none_for_nonexistent(self, users_repo):
        assert users_repo.get(99999) is None

    def test_list_filters_by_kwargs(self, users_repo, sample_user):
        users_repo.create(**make_user_data(username="other", email="other@ex.com"))
        by_email = users_repo.list(email=sample_user.email)
        assert len(by_email) == 1
        assert by_email[0].id == sample_user.id

    def test_list_excludes_deleted(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        assert len(users_repo.list()) == 0

    def test_update(self, users_repo, sample_user):
        updated = users_repo.update(sample_user.id, fname="Updated", lname="Name")
        assert updated.fname == "Updated"
        assert updated.lname == "Name"
        fetched = users_repo.get(sample_user.id)
        assert fetched.fname == "Updated"

    def test_update_returns_none_for_nonexistent(self, users_repo):
        assert users_repo.update(99999, fname="X") is None

    def test_delete_sets_deleted_at(self, users_repo, sample_user):
        result = users_repo.delete(sample_user.id)
        assert result.deleted_at is not None
        assert users_repo.get(sample_user.id) is None

    def test_restore_clears_deleted_at(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        restored = users_repo.restore(sample_user.id)
        assert restored.deleted_at is None
        assert users_repo.get(sample_user.id) is not None

    def test_all_includes_deleted(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        all_users = users_repo.all()
        assert len(all_users) >= 1
        deleted = next(u for u in all_users if u.id == sample_user.id)
        assert deleted.deleted_at is not None


class TestStudentsOfClassRepository:
    """StudentsOfClass many-to-many."""

    def test_create(self, students_repo, sample_user, sample_class):
        link = students_repo.create(user_id=sample_user.id, class_id=sample_class.id)
        assert link.id is not None
        assert link.user_id == sample_user.id
        assert link.class_id == sample_class.id

    def test_list_by_class(self, students_repo, sample_user, sample_class):
        students_repo.create(user_id=sample_user.id, class_id=sample_class.id)
        links = students_repo.list(class_id=sample_class.id)
        assert len(links) == 1
        assert links[0].user_id == sample_user.id

    def test_list_by_user(self, students_repo, sample_user, sample_class):
        students_repo.create(user_id=sample_user.id, class_id=sample_class.id)
        links = students_repo.list(user_id=sample_user.id)
        assert len(links) == 1
        assert links[0].class_id == sample_class.id


class TestClassTeacherRepository:
    """ClassTeacher many-to-many."""

    def test_create(self, class_teacher_repo, sample_user, sample_class):
        link = class_teacher_repo.create(
            teacher_id=sample_user.id, class_id=sample_class.id
        )
        assert link.id is not None
        assert link.teacher_id == sample_user.id
        assert link.class_id == sample_class.id

    def test_list_by_class(self, class_teacher_repo, sample_user, sample_class):
        class_teacher_repo.create(
            teacher_id=sample_user.id, class_id=sample_class.id
        )
        links = class_teacher_repo.list(class_id=sample_class.id)
        assert len(links) == 1
