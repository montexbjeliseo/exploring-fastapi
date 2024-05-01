from sqlalchemy.orm import Mapped, MappedColumn, relationship

from app.db import Base


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = MappedColumn(primary_key=True, index=True)
    name: Mapped[str] = MappedColumn(unique=True, index=True)
    users: Mapped[list["User"]] = relationship("User", back_populates="roles")
