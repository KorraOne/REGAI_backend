"""
Shared pytest fixtures for REGAI backend tests.
Uses SQLite in-memory database for fast, isolated tests.
"""
import sys
from pathlib import Path

# Ensure project root is on path (pytest may run from tests/)
_root = Path(__file__).resolve().parent.parent
_root_str = str(_root)
if _root_str not in sys.path:
    sys.path.insert(0, _root_str)

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from db.models import Base


# Use SQLite in-memory for tests (no PostgreSQL required)
TEST_DATABASE_URL = "sqlite:///:memory:?check_same_thread=False"


@pytest.fixture(scope="function")
def engine():
    """Create a fresh in-memory SQLite engine per test."""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        echo=False,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()


@pytest.fixture(scope="function")
def db_session(engine):
    """Provide a database session. Rolls back after each test."""
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
        future=True,
    )
    session = SessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


def make_user_data(**overrides):
    """Factory for user creation data."""
    data = {
        "fname": "Test",
        "lname": "User",
        "username": "testuser",
        "email": "test@example.com",
        "password_hash": "hashed",
        **overrides,
    }
    return data
