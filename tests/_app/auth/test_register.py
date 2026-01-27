def test_login_wrong_password(client, register_user):
    register_user("a@b.com", "correct", "A")
    res = client.post("/auth/login", json={
        "email": "a@b.com",
        "password": "wrong"
    })
    assert res.status_code == 401


def test_login_missing_email(client):
    res = client.post("/auth/login", json={
        "password": "pass123"
    })
    assert res.status_code == 422


def test_login_missing_password(client):
    res = client.post("/auth/login", json={
        "email": "test@example.com"
    })
    assert res.status_code == 422


def test_login_nonexistent_user(client):
    res = client.post("/auth/login", json={
        "email": "nobody@example.com",
        "password": "pass123"
    })
    assert res.status_code == 401