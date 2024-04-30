from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.dependencies import get_current_user
from app.models.users import User, UserModel
from app.utils.auth_utils import *


app = APIRouter()


@app.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user_from_db = await session.execute(select(User).where(User.email == user.username))
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_from_db = user_from_db.scalars().first()
    if not verify_password(user.password, user_from_db.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {
        "access_token": create_access_token(user_from_db.email), 
        "refresh_token": create_refresh_token(user_from_db.email)
        }

@app.post("/register")
async def register():
    pass

@app.get("/me", response_model=UserModel)
async def me(user: User = Depends(get_current_user)):
    return user