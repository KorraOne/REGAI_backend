from pydantic import BaseModel

class Register_Request(BaseModel):
    email: str
    password: str
    name: str

class Register_Response(BaseModel):
    user_id: int
    email: str
    name: str

class Login_Request(BaseModel):
    email: str
    password: str

class Login_Response(BaseModel):
    access_token: str
    token_type: str = "bearer"