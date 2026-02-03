"""Tests for ClassesService."""
import pytest


class TestClassesServiceCRUD:
    """ClassesService CRUD operations."""

    def test_create_class(self, classes_service):
        cls = classes_service.create_class({"name": "CS101"})
        assert cls.id is not None
        assert cls.name == "CS101"

    def test_get_class(self, classes_service, sample_class):
        cls = classes_service.get_class(sample_class.id)
        assert cls is not None
        assert cls.id == sample_class.id

    def test_list_classes(self, classes_service, sample_class):
        classes = classes_service.list_classes()
        assert len(classes) >= 1

    def test_update_class(self, classes_service, sample_class):
        updated = classes_service.update_class(
            sample_class.id, {"name": "Updated"}
        )
        assert updated.name == "Updated"

    def test_delete_class(self, classes_service, sample_class):
        classes_service.delete_class(sample_class.id)
        assert classes_service.get_class(sample_class.id) is None

    def test_restore_class(self, classes_service, sample_class):
        classes_service.delete_class(sample_class.id)
        restored = classes_service.restore_class(sample_class.id)
        assert restored.deleted_at is None


class TestClassesServiceStudentMembership:
    """ClassesService student add/remove."""

    def test_add_student(self, classes_service, sample_class, sample_user):
        result = classes_service.add_student(sample_class.id, sample_user.id)
        assert result is not None
        students = classes_service.list_students(sample_class.id)
        assert len(students) == 1
        assert students[0].user_id == sample_user.id

    def test_add_student_idempotent(
        self, classes_service, sample_class, sample_user
    ):
        r1 = classes_service.add_student(sample_class.id, sample_user.id)
        r2 = classes_service.add_student(sample_class.id, sample_user.id)
        assert r1.id == r2.id

    def test_remove_student(
        self, classes_service, sample_class, sample_user
    ):
        classes_service.add_student(sample_class.id, sample_user.id)
        result = classes_service.remove_student(
            sample_class.id, sample_user.id
        )
        assert result is not None
        students = classes_service.list_students(sample_class.id)
        assert len(students) == 0


class TestClassesServiceTeacherMembership:
    """ClassesService teacher add/remove."""

    def test_add_teacher(self, classes_service, sample_class, sample_user):
        result = classes_service.add_teacher(
            sample_class.id, sample_user.id
        )
        assert result is not None
        teachers = classes_service.list_teachers(sample_class.id)
        assert len(teachers) == 1

    def test_remove_teacher(
        self, classes_service, sample_class, sample_user
    ):
        classes_service.add_teacher(sample_class.id, sample_user.id)
        result = classes_service.remove_teacher(
            sample_class.id, sample_user.id
        )
        assert result is not None
        teachers = classes_service.list_teachers(sample_class.id)
        assert len(teachers) == 0
