from sqlalchemy import ForeignKey, Integer, Column
from sqlalchemy.orm import Mapped, MappedColumn, relationship
from app.db import Base
from app.models.roles import Role


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    first_name: Mapped[str] = MappedColumn(index=True)
    last_name: Mapped[str] = MappedColumn(index=True)
    email: Mapped[str] = MappedColumn(unique=True, index=True)
    password: Mapped[str] = MappedColumn()
    role_id: Mapped[int] = MappedColumn(ForeignKey("roles.id"), index=True)

    role: Mapped["Role"] = relationship("Role", back_populates="users", primaryjoin="User.role_id == Role.id")
