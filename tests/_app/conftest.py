import pytest
from fastapi.testclient import TestClient
from app.main import app
import app.db as db

@pytest.fixture(autouse=True)
def reset_db():
    """Reset in-memory DB before every test."""
    db.users.clear()
    db.scenarios.clear()
    yield

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def register_user(client):
    def _register(email, password, name):
        res = client.post("/auth/register", json={
            "email": email,
            "password": password,
            "name": name
        })
        assert res.status_code == 200
        return res.json()
    return _register

@pytest.fixture
def login_user(client):
    def _login(email, password):
        res = client.post("/auth/login", json={
            "email": email,
            "password": password
        })
        assert res.status_code == 200
        return res.json()["access_token"]
    return _login

@pytest.fixture
def auth_client(client, register_user, login_user):
    """Returns a client with Authorization header set."""
    def _auth(email, password, name="Test User"):
        register_user(email, password, name)
        token = login_user(email, password)
        client.headers.update({"Authorization": f"Bearer {token}"})
        return client
    return _auth