from jose import jwt
from datetime import datetime, timedelta, UTC
from app.config import SECRET_KEY, ALGORITHM


def test_tampered_token(client, auth_client):
    client = auth_client("a@b.com", "pass")
    token = client.headers["Authorization"].split()[1]

    # Flip the last character
    tampered = token[:-1] + ("A" if token[-1] != "A" else "B")

    res = client.get("/auth/me", headers={
        "Authorization": f"Bearer {tampered}"
    })
    assert res.status_code == 401


def test_expired_token(client, register_user):
    register_user("a@b.com", "pass", "A")

    expired_token = jwt.encode(
        {
            "user_id": 1,
            "exp": datetime.now(UTC) - timedelta(seconds=10)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    res = client.get("/auth/me", headers={
        "Authorization": f"Bearer {expired_token}"
    })
    assert res.status_code == 401