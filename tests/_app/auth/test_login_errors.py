def test_login_success(auth_client):
    client = auth_client("test@example.com", "pass123")
    res = client.get("/auth/me")
    assert res.status_code == 200
    assert res.json()["email"] == "test@example.com"