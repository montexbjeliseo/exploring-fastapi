from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload

from app.db import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.roles import Role
from app.models.users import User
from app.schemas.user_schemas import CreateUser, UpdateUser, UserModel
from app.utils.auth_utils import get_hashed_password

from app.mappers.user_mapper import to_user_model_list, to_user_model


app = APIRouter()


@app.get("", response_model=list[UserModel])
async def get_users(session: AsyncSession = Depends(get_session)):
    results = await session.execute(select(User).options(selectinload(User.role)))
    users = results.scalars().fetchall()

    print("Users:", users[0])
    mapped = to_user_model_list(users)
    return mapped


@app.post("", response_model=UserModel)
async def post_users(user: CreateUser, session: AsyncSession = Depends(get_session)):
    
    user_exists = await session.execute(select(User).where(User.email == user.email))
    user_exists = user_exists.scalars().first()
    if user_exists:
        raise HTTPException(status_code=409, detail="User already exists")
    
    role = await session.execute(select(Role).where(Role.name == user.role.lower().strip()))
    role = role.scalars().first()
    
    if not role:
        raise HTTPException(status_code=404, detail=f"Role {user.role} not found")
    
    saved_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email,
        password=get_hashed_password(user.password),
        role_id=role.id
    )
    session.add(saved_user)
    await session.commit()
    await session.refresh(saved_user)
    await session.refresh(role)
    
    return to_user_model(saved_user)


@app.patch("/{id}", response_model=UserModel)
async def patch_user(user_id: int, user: UpdateUser, session: AsyncSession = Depends(get_session)):
    user_from_db: User | None = await session.get(User, user_id)
    if not user_from_db:
        raise HTTPException(status_code=404, detail="User not found")

    if user.email:
        user_exists = await session.execute(select(User).where(User.email == user.email))
        user_exists = user_exists.scalars().first()
        if user_exists:
            raise HTTPException(status_code=409, detail="Email already exists")

    user_from_db.first_name = user.first_name or user_from_db.first_name
    user_from_db.last_name = user.last_name or user_from_db.last_name
    user_from_db.email = user.email or user_from_db.email
    user_from_db.password = get_hashed_password(user.password) or user_from_db.password

    role = await session.execute(select(Role).where(Role.name == user.role.lower().strip()))
    role = role.scalars().first()

    if role:
        user_from_db.role_id = role.id

    await session.commit()
    await session.refresh(user_from_db, ["role"])

    return to_user_model(user_from_db)


@app.delete("/{id}", response_model=UserModel)
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user_from_db: User | None = await session.get(User, user_id, options=[selectinload(User.role)])

    if not user_from_db or user_from_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    response = to_user_model(user_from_db)

    await session.delete(user_from_db)
    await session.commit()
    return response
