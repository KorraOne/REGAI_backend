from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError
from app.auth.jwt import decode_access_token
import app.db as db
from app.models.scenarios.domain.user import User

security = HTTPBearer()

def get_current_user(token = Depends(security)) -> User:
    """
    Extracts and validates the JWT from the Authorization header.
    Returns the full User model if valid.
    """
    try:
        payload = decode_access_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    # db.users now contains User Pydantic models
    user = next((u for u in db.users if u.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user