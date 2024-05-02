from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_session
from app.dependencies import get_current_user
from app.models.users import User
from app.models.roles import Role
from app.utils.auth_utils import *

from app.mappers.user_mapper import to_user_model
from app.schemas.user_schemas import UserModel, RegisterUser

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


@app.post("/register", response_model=UserModel)
async def register(user: RegisterUser, session: AsyncSession = Depends(get_session)):
    user_exists = await session.execute(select(User).where(User.email == user.email))
    user_exists = user_exists.scalars().first()
    if user_exists:
        raise HTTPException(status_code=409, detail="User already exists")

    default_role = await session.execute(select(Role).where(Role.name == "user"))
    default_role = default_role.scalars().first()
    if not default_role:
        raise HTTPException(status_code=404, detail="Default role not found")

    user.password = get_hashed_password(user.password)
    saved_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=user.password,
        role_id=default_role.id
    )
    session.add(saved_user)
    await session.commit()
    await session.refresh(saved_user)
    await session.refresh(default_role)

    return to_user_model(saved_user)


@app.get("/me", response_model=UserModel)
async def me(user: User = Depends(get_current_user)):
    return user
