from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    name: str
    last_name: str
    email: EmailStr
    tel: str
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    last_name: str
    email: str
    tel: str
    role: str