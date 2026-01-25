from fastapi import APIRouter, HTTPException
from app.models.auth import *
import app.helpers._utils as _utils
import app.db as db
from app.auth.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

###########
# Register
###########
@router.post("/register", response_model=Register_Response)
def register(payload: Register_Request):
    if _utils.email_exists(payload.email):
        raise HTTPException(
            status_code=409,
            detail={"code": "EMAIL_TAKEN", "message": "Email already exists."}
        )

    new_id = db.users[-1]["id"] + 1 if db.users else 1
    hashed_password = _utils.hash_password(payload.password)

    db.users.append({
        "id": new_id,
        "email": payload.email,
        "password": hashed_password,
        "name": payload.name
    })

    return {
        "user_id": new_id,
        "email": payload.email,
        "name": payload.name
    }

###########
# Login
###########
@router.post("/login", response_model=Login_Response)
def login(payload: Login_Request):
    user = next((u for u in db.users if u["email"].lower() == payload.email.lower()), None)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    hashed_password = _utils.hash_password(payload.password)
    if user["password"] != hashed_password:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token({"user_id": user["id"]})

    return {
        "access_token": token,
        "token_type": "bearer"
    }