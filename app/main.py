from fastapi import FastAPI
from .routes import users, auth

app = FastAPI(
    title="My First Fast API", 
    version="0.0.1",
    description= "This is a simple FastAPI app",
    )

app.include_router(auth.app, prefix="/auth", tags=["Authentication"])
app.include_router(users.app, prefix="/users", tags=["Users Management"])

@app.get("/", tags=["root"], summary="Root Endpoint")
async def root():
    return {
        "message": "Service is up and running!",
        }