# from fastapi import APIRouter, HTTPException, Depends

# from app.schemas.requests import (
#     RegisterRequest,
#     LoginRequest,
# )
# from app.schemas.responses import (
#     RegisterResponse,
#     LoginResponse,
#     UserResponse,
# )

# import app.helpers._utils as _utils
# import app.db as db
# from app.auth.jwt import create_access_token
# from app.auth.dependencies import get_current_user
# from app.models.scenarios.domain.user import User


# router = APIRouter(prefix="/auth", tags=["auth"])


# ###########
# # Register
# ###########
# @router.post("/register", response_model=RegisterResponse)
# def register(payload: RegisterRequest):
#     if _utils.email_exists(payload.email):
#         raise HTTPException(
#             status_code=409,
#             detail={"code": "EMAIL_TAKEN", "message": "Email already exists."},
#         )

#     new_id = db.users[-1].id + 1 if db.users else 1
#     hashed_password = _utils.hash_password(payload.password)

#     new_user = User(
#         id=new_id,
#         email=payload.email,
#         password=hashed_password,
#         name=payload.name,
#     )

#     db.users.append(new_user)

#     return {
#         "id": new_user.id,
#         "email": new_user.email,
#         "name": new_user.name,
#     }


# ###########
# # Login
# ###########
# @router.post("/login", response_model=LoginResponse)
# def login(payload: LoginRequest):
#     user = next(
#         (u for u in db.users if u.email.lower() == payload.email.lower()),
#         None
#     )
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     if not _utils.verify_password(payload.password, user.password):
#         raise HTTPException(status_code=401, detail="Invalid email or password")

#     token = create_access_token({"user_id": user.id})

#     return {
#         "access_token": token,
#         "token_type": "bearer",
#         "user": {
#             "id": user.id,
#             "email": user.email,
#             "name": user.name,
#         },
#     }


# ###########
# # Me (get current user)
# ###########
# @router.get("/me", response_model=UserResponse)
# def get_me(user=Depends(get_current_user)):
#     # get_current_user should now return a User model
#     return {
#         "id": user.id,
#         "email": user.email,
#         "name": user.name,
#     }