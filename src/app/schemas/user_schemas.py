from typing import Optional
from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    role: str


class RegisterUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    role: str


class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None
