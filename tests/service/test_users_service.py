"""Tests for UsersService."""
from datetime import datetime, timedelta, timezone

import pytest

from tests.conftest import make_user_data


class TestUsersServiceCRUD:
    """UsersService CRUD operations."""

    def test_create_user(self, users_service):
        data = make_user_data()
        user = users_service.create_user(data)
        assert user.id is not None
        assert user.fname == data["fname"]

    def test_get_user(self, users_service, sample_user):
        user = users_service.get_user(sample_user.id)
        assert user is not None
        assert user.id == sample_user.id

    def test_list_users(self, users_service, sample_user):
        users = users_service.list_users(email=sample_user.email)
        assert len(users) == 1

    def test_update_user(self, users_service, sample_user):
        updated = users_service.update_user(
            sample_user.id, {"fname": "Updated", "lname": "Name"}
        )
        assert updated.fname == "Updated"

    def test_delete_user(self, users_service, sample_user):
        users_service.delete_user(sample_user.id)
        assert users_service.get_user(sample_user.id) is None

    def test_restore_user(self, users_service, sample_user):
        users_service.delete_user(sample_user.id)
        restored = users_service.restore_user(sample_user.id)
        assert restored.deleted_at is None
        assert users_service.get_user(sample_user.id) is not None


class TestUsersServiceRelationships:
    """UsersService relationship methods."""

    def test_get_scenarios_owned_by_user(
        self, users_service, scenarios_service, sample_user
    ):
        scenarios_service.create_scenario(
            owner_id=sample_user.id,
            title="S1",
        )
        scenarios = users_service.get_scenarios_owned_by_user(sample_user.id)
        assert scenarios is not None
        assert len(scenarios) >= 1

    def test_get_classes_user_is_in(
        self, users_service, classes_service, sample_user, sample_class
    ):
        classes_service.add_student(sample_class.id, sample_user.id)
        classes = users_service.get_classes_user_is_in(sample_user.id)
        assert len(classes) >= 1

    def test_get_classes_taught_by_user(
        self, users_service, classes_service, sample_user, sample_class
    ):
        classes_service.add_teacher(sample_class.id, sample_user.id)
        classes = users_service.get_classes_taught_by_user(sample_user.id)
        assert len(classes) >= 1


class TestUsersServiceSubscription:
    """UsersService subscription management."""

    def test_is_subscription_active_false_when_none(
        self, users_service, sample_user
    ):
        assert users_service.is_subscription_active(sample_user.id) is False

    def test_is_subscription_active_true_when_future(
        self, users_service, sample_user
    ):
        future = datetime.now(timezone.utc) + timedelta(days=7)
        users_service.update_user(
            sample_user.id, {"subscription_expires_at": future}
        )
        assert users_service.is_subscription_active(sample_user.id) is True

    def test_renew_subscription(self, users_service, sample_user):
        user = users_service.renew_subscription(sample_user.id, days=30)
        assert user.subscription_expires_at is not None
        assert users_service.is_subscription_active(sample_user.id) is True

    def test_expire_subscription(self, users_service, sample_user):
        users_service.renew_subscription(sample_user.id, days=30)
        user = users_service.expire_subscription(sample_user.id)
        assert user.subscription_expires_at is not None
        assert users_service.is_subscription_active(sample_user.id) is False
