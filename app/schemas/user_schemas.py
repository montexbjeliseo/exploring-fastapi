from typing import Optional
from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
        
class CreateUser(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    
class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None