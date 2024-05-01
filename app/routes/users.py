from fastapi import APIRouter, Depends, HTTPException
from app.db import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import User
from app.schemas.user_schemas import CreateUser, UpdateUser, UserModel
from app.utils.auth_utils import get_hashed_password

app = APIRouter()


@app.get("", response_model=list[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    results = await session.execute(select(User))
    users = results.scalars().all()
    return users


@app.post("", response_model=UserModel)
async def post_users(user: CreateUser, session: AsyncSession = Depends(get_session)):
    saved_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_hashed_password(user.password)
    )
    session.add(saved_user)
    await session.commit()
    await session.refresh(saved_user)
    return saved_user


@app.patch("/{id}", response_model=UserModel)
async def patch_user(id: int, user: UpdateUser, session: AsyncSession = Depends(get_session)):
    user_from_db = await session.get(User, id)
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    user_from_db.first_name = user.first_name or user_from_db.first_name
    user_from_db.last_name = user.last_name or user_from_db.last_name
    user_from_db.email = user.email or user_from_db.email
    user_from_db.password = get_hashed_password(user.password) or user_from_db.password

    await session.commit()
    await session.refresh(user_from_db)
    return user_from_db


@app.delete("/{id}", response_model=UserModel)
async def delete_user(id: int, session: AsyncSession = Depends(get_session)):
    user_from_db = await session.get(User, id)
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    await session.delete(user_from_db)
    await session.commit()
    return user_from_db
