from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.helpers.jwt import decode_access_token
from db.session import get_db
from db.crud.users import UsersRepository


security = HTTPBearer()


def get_current_user(
    token = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Extract and validate JWT, then return the SQLAlchemy User model.
    """
    try:
        payload = decode_access_token(token.credentials)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    users_repo = UsersRepository(db)
    user = users_repo.get(user_id)

    if user is None:
        raise HTTPException(status_code=401, detail="User not found")

    return user