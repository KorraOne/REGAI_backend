"""Tests for BaseRepository soft delete and filtering behavior."""
import pytest

from tests.conftest import make_user_data


class TestBaseRepositorySoftDelete:
    """Verify soft delete behavior across repositories."""

    def test_deleted_records_excluded_from_get(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        assert users_repo.get(sample_user.id) is None

    def test_deleted_records_excluded_from_list(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        assert len(users_repo.list()) == 0

    def test_restore_returns_record_to_active(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        restored = users_repo.restore(sample_user.id)
        assert restored.deleted_at is None
        assert users_repo.get(sample_user.id) is not None

    def test_all_includes_deleted(self, users_repo, sample_user):
        users_repo.delete(sample_user.id)
        all_records = users_repo.all()
        found = next((u for u in all_records if u.id == sample_user.id), None)
        assert found is not None
        assert found.deleted_at is not None
