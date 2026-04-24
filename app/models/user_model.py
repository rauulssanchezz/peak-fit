from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Float, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    weight: Mapped[float] = mapped_column(Float(precision=2))
    goal: Mapped[str] = mapped_column(String(50))

    exercises = relationship("Exercise", back_populates="user", cascade="all, delete-orphan")