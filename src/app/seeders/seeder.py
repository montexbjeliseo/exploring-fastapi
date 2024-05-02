from app.db import engine, Base, SessionLocal


async def get_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    return SessionLocal()
