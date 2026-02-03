from __future__ import annotations

from typing import Iterable

from db.models import ClassTeacher, StudentsOfClass


class ClassesService:
    """
    Handles class-related business logic:
    - create classes
    - list classes
    - manage class membership
    """

    def __init__(
        self,
        class_repo,
        students_repo=None,
        class_teacher_repo=None,
    ):
        self.classes = class_repo
        self.students = students_repo
        self.class_teachers = class_teacher_repo

    # ---------------------------------------------------------
    # CLASS CRUD
    # ---------------------------------------------------------
    def create_class(self, data: dict):
        """Create a new class."""
        return self.classes.create(**data)

    def get_class(self, class_id: int):
        """Return a single active class."""
        return self.classes.get(class_id)

    def list_classes(self, **filters):
        """List active classes filtered by kwargs."""
        return self.classes.list(**filters)

    def update_class(self, class_id: int, data: dict):
        """Update class details."""
        return self.classes.update(class_id, **data)

    def delete_class(self, class_id: int):
        """Soft delete a class."""
        return self.classes.delete(class_id)

    def restore_class(self, class_id: int):
        """Restore a previously deleted class."""
        return self.classes.restore(class_id)

    # ---------------------------------------------------------
    # STUDENT MEMBERSHIP
    # ---------------------------------------------------------
    def add_student(self, class_id: int, user_id: int):
        self._ensure_students_repo()

        existing = self.students.list(class_id=class_id, user_id=user_id)
        if existing:
            return existing[0]

        restored = self._restore_soft_deleted_student(class_id, user_id)
        if restored:
            return restored

        return self.students.create(class_id=class_id, user_id=user_id)

    def add_students(self, class_id: int, user_ids: Iterable[int]):
        self._ensure_students_repo()
        return [self.add_student(class_id, user_id) for user_id in user_ids]

    def list_students(self, class_id: int):
        self._ensure_students_repo()
        return self.students.list(class_id=class_id)

    def remove_student(self, class_id: int, user_id: int):
        self._ensure_students_repo()
        membership = self.students.list(class_id=class_id, user_id=user_id)
        if not membership:
            return None
        return self.students.delete(membership[0].id)

    # ---------------------------------------------------------
    # TEACHER MEMBERSHIP
    # ---------------------------------------------------------
    def add_teacher(self, class_id: int, teacher_id: int):
        self._ensure_teachers_repo()

        existing = self.class_teachers.list(class_id=class_id, teacher_id=teacher_id)
        if existing:
            return existing[0]

        restored = self._restore_soft_deleted_teacher(class_id, teacher_id)
        if restored:
            return restored

        return self.class_teachers.create(class_id=class_id, teacher_id=teacher_id)

    def list_teachers(self, class_id: int):
        self._ensure_teachers_repo()
        return self.class_teachers.list(class_id=class_id)

    def remove_teacher(self, class_id: int, teacher_id: int):
        self._ensure_teachers_repo()
        membership = self.class_teachers.list(class_id=class_id, teacher_id=teacher_id)
        if not membership:
            return None
        return self.class_teachers.delete(membership[0].id)

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------
    def _ensure_students_repo(self):
        if self.students is None:
            raise RuntimeError("StudentsOfClass repository is required for this operation")

    def _ensure_teachers_repo(self):
        if self.class_teachers is None:
            raise RuntimeError("ClassTeacher repository is required for this operation")

    def _restore_soft_deleted_student(self, class_id: int, user_id: int):
        db = self.students.db
        record = (
            db.query(StudentsOfClass)
            .filter(
                StudentsOfClass.class_id == class_id,
                StudentsOfClass.user_id == user_id,
                StudentsOfClass.deleted_at.is_not(None),
            )
            .first()
        )
        if not record:
            return None

        record.deleted_at = None
        db.add(record)
        db.commit()
        db.refresh(record)
        return record

    def _restore_soft_deleted_teacher(self, class_id: int, teacher_id: int):
        db = self.class_teachers.db
        record = (
            db.query(ClassTeacher)
            .filter(
                ClassTeacher.class_id == class_id,
                ClassTeacher.teacher_id == teacher_id,
                ClassTeacher.deleted_at.is_not(None),
            )
            .first()
        )
        if not record:
            return None

        record.deleted_at = None
        db.add(record)
        db.commit()
        db.refresh(record)
        return record