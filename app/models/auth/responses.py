from pydantic import BaseModel

class UserResponse(BaseModel):
    id: int
    email: str
    name: str

class RegisterResponse(BaseModel):
    id: int
    email: str
    name: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse