from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, auth
from app.seeders import role_seeder, user_seeder


@asynccontextmanager
async def lifespan(app: FastAPI):
    await role_seeder.initialize_roles()
    await user_seeder.initialize_users()
    yield
    # clear


app = FastAPI(
    lifespan=lifespan,
    title="My First Fast API",
    version="0.0.1",
    description="This is a simple FastAPI app",
)

app.include_router(auth.app, prefix="/auth", tags=["Authentication"])
app.include_router(users.app, prefix="/users", tags=["Users Management"])

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"])


@app.get("/", tags=["root"], summary="Root Endpoint")
async def root():
    return {
        "message": "Service is up and running!",
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
