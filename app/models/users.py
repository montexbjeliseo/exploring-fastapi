from sqlalchemy import ForeignKey
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
    role_id = MappedColumn(ForeignKey("roles.id"))
    roles: Mapped[Role] = relationship("Role", back_populates="users")
