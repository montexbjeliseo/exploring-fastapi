from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_session

from app.db import Base, engine, SessionLocal
from app.models.roles import Role


async def get_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return SessionLocal()


async def initialize_roles():
    print("Checking if roles already exist...")
    session = await get_session()
    async with session as async_db:
        results = await async_db.execute(select(Role))
        roles_from_db = results.scalars().all()

        if len(roles_from_db) > 0:
            print("Roles already exist. Skipping seeding roles...")
            return

        print("Seeding roles...")
        roles = [
            {"name": "admin"},
            {"name": "user"},
        ]

        for role in roles:
            async_db.add(Role(**role))

        await async_db.commit()
        await async_db.refresh(Role)
        await async_db.close()
        print("Seeding roles done!")
