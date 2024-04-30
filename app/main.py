from fastapi import FastAPI
from .routes import users, auth

app = FastAPI(title="My First Fast API", version="0.0.1")

app.include_router(auth.app, prefix="/auth", tags=["auth"])
app.include_router(users.app, prefix="/users", tags=["users"])

@app.get("/", tags=["root"])
async def root():
    return {
        "message": "Service is up and running!",
        }