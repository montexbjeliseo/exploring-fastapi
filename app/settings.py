from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

_= load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))


class Settings(BaseSettings):
    db_url: str = os.getenv("DB_URL")
    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY")
    jwt_refresh_secret_key: str = os.getenv("JWT_REFRESH_SECRET_KEY")

settings = Settings()
