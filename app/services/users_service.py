from datetime import datetime, timedelta, timezone


class UsersService:
    """
    Handles user-related business logic:
    - create users
    - get single user by id
    - get list of users by filter
    - update user details
    - delete user
    - restore user

    - get scenarios owned by user
    - get classes user is in
    - get classes taught by user

    - get subscription active status
    - get subscription expiry date
    - renew subscription
    - expire subscription
    """

    def __init__(self, users_repo, students_of_class_repo, class_teacher_repo):
        self.users = users_repo
        self.students_of_class = students_of_class_repo
        self.class_teacher = class_teacher_repo

    # ---------------------------------------------------------
    # USER CRUD
    # ---------------------------------------------------------
    def create_user(self, data: dict):
        """Create a new user."""
        return self.users.create(**data)

    def get_user(self, user_id: int):
        """Return a single active user."""
        return self.users.get(user_id)

    def list_users(self, **filters):
        """Return all active users matching filters."""
        return self.users.list(**filters)

    def update_user(self, user_id: int, data: dict):
        """Update user fields."""
        return self.users.update(user_id, **data)

    def delete_user(self, user_id: int):
        """Soft delete a user."""
        return self.users.delete(user_id)

    def restore_user(self, user_id: int):
        """Restore a soft-deleted user."""
        return self.users.restore(user_id)

    # ---------------------------------------------------------
    # USER RELATIONSHIPS
    # ---------------------------------------------------------
    def get_scenarios_owned_by_user(self, user_id: int):
        """
        Return all scenarios owned by the user.
        Uses the relationship defined in the Users model.
        """
        user = self.users.get(user_id)
        if not user:
            return None
        return user.owned_scenarios

    def get_classes_user_is_in(self, user_id: int):
        """
        Return all classes the user is enrolled in.
        """
        return self.students_of_class.list(user_id=user_id)

    def get_classes_taught_by_user(self, user_id: int):
        """
        Return all classes the user teaches.
        """
        return self.class_teacher.list(teacher_id=user_id)

    # ---------------------------------------------------------
    # SUBSCRIPTION MANAGEMENT
    # ---------------------------------------------------------
    def is_subscription_active(self, user_id: int):
        """
        Check if the user's subscription is still valid.
        Assumes the Users model has a subscription_expires_at field.
        """
        user = self.users.get(user_id)
        if not user or not hasattr(user, "subscription_expires_at"):
            return False

        if user.subscription_expires_at is None:
            return False

        return user.subscription_expires_at > datetime.now(timezone.utc)

    def get_subscription_expiry(self, user_id: int):
        """Return the subscription expiry datetime."""
        user = self.users.get(user_id)
        if not user or not hasattr(user, "subscription_expires_at"):
            return None
        return user.subscription_expires_at

    def renew_subscription(self, user_id: int, days: int = 30):
        """
        Extend subscription by N days.
        If expired, start from now.
        If active, extend from current expiry.
        """
        user = self.users.get(user_id)
        if not user:
            return None

        now = datetime.now(timezone.utc)

        if not hasattr(user, "subscription_expires_at") or user.subscription_expires_at is None:
            new_expiry = now + timedelta(days=days)
        else:
            base = max(now, user.subscription_expires_at)
            new_expiry = base + timedelta(days=days)

        user.subscription_expires_at = new_expiry
        self.users.db.commit()
        self.users.db.refresh(user)
        return user

    def expire_subscription(self, user_id: int):
        """Immediately expire a user's subscription."""
        user = self.users.get(user_id)
        if not user:
            return None

        user.subscription_expires_at = datetime.now(timezone.utc)
        self.users.db.commit()
        self.users.db.refresh(user)
        return user