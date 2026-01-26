from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from jose import JWTError
from app.auth.jwt import decode_access_token
import app.db as db

security = HTTPBearer()

def get_current_user(token = Depends(security)):
    """
    Extracts and validates the JWT from the Authorization header.
    Returns the full user dict if valid.
    """
    try:
        payload = decode_access_token(token.credentials)
    except Exception:
        # Catch ANY decode failure, not just JWTError
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = next((u for u in db.users if u["id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user