from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.dependencies import get_current_user
from app.models.users import User
from app.schemas.user_schemas import CreateUser, UserModel
from app.utils.auth_utils import *

app = APIRouter()


@app.post("/login")
async def login(user: OAuth2PasswordRequestForm = Depends(), session: AsyncSession = Depends(get_session)):
    user_from_db = await session.execute(select(User).where(User.email == user.username))
    user_from_db = user_from_db.scalars().first()
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, user_from_db.password):
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {
        "access_token": create_access_token(user_from_db.email),
        "refresh_token": create_refresh_token(user_from_db.email)
    }


@app.post("/register")
async def register(user: CreateUser, session: AsyncSession = Depends(get_session)):
    user.password = get_hashed_password(user.password)
    saved_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password
    )
    session.add(saved_user)
    await session.commit()
    await session.refresh(saved_user)
    return saved_user


@app.get("/me", response_model=UserModel)
async def me(user: User = Depends(get_current_user)):
    return user
