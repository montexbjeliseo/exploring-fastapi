from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

_= load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class Settings(BaseSettings):
    db_url: str = os.getenv("DB_URL")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")
    access_token_expire_minutes: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
    refresh_token_expire_minutes: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
    algorithm: str = os.getenv("ALGORITHM")

settings = Settings()
