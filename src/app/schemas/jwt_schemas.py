from pydantic import BaseModel, EmailStr

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str

class TokenPayload(BaseModel):
    sub: EmailStr
    exp: int