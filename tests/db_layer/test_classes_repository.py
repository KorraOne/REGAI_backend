"""Tests for ClassRepository."""
import pytest


class TestClassRepository:
    """ClassRepository CRUD."""

    def test_create(self, class_repo):
        cls = class_repo.create(name="CS101")
        assert cls.id is not None
        assert cls.name == "CS101"
        assert cls.deleted_at is None

    def test_get(self, class_repo, sample_class):
        cls = class_repo.get(sample_class.id)
        assert cls is not None
        assert cls.name == sample_class.name

    def test_list(self, class_repo, sample_class):
        classes = class_repo.list()
        assert len(classes) >= 1
        assert sample_class.id in [c.id for c in classes]

    def test_update(self, class_repo, sample_class):
        updated = class_repo.update(sample_class.id, name="Updated Name")
        assert updated.name == "Updated Name"

    def test_delete_and_restore(self, class_repo, sample_class):
        class_repo.delete(sample_class.id)
        assert class_repo.get(sample_class.id) is None
        restored = class_repo.restore(sample_class.id)
        assert restored.deleted_at is None
        assert class_repo.get(sample_class.id) is not None
