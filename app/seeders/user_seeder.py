from sqlalchemy import select

from app.models.users import User
from app.seeders.seeder import get_session
from app.settings import settings


async def initialize_users():
    print("Checking if users already exist...")
    session = await get_session()
    async with session as async_db:
        results = await async_db.execute(select(User))
        users_from_db = results.scalars().all()

        if len(users_from_db) > 0:
            print("Users already exist. Skipping seeding users...")
            return

        print("Seeding users...")
        users = [
            {
                "first_name": "John",
                "last_name": "Doe",
                "email": settings.admin_email,
                "password": settings.admin_password,
                "role_id": 1
            },
            {
                "first_name": "Jane",
                "last_name": "Doe",
                "email": "janedoe@example.com",
                "password": "Test1234@!",
                "role_id": 2
            }
        ]

        for user in users:
            async_db.add(User(**user))

        await async_db.commit()
        await async_db.refresh(User)
        await async_db.close()
        print("Seeding users done!")
