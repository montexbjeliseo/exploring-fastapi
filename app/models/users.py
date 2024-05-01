from typing import Optional
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Mapped, MappedColumn
from app.db import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    first_name: Mapped[str] = MappedColumn(index=True)
    last_name: Mapped[str] = MappedColumn(index=True)
    email: Mapped[str] = MappedColumn(unique=True, index=True)
    password: Mapped[str] = MappedColumn()