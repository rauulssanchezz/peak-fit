import uuid
from sqlalchemy import UUID, Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.core.db import Base


class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    category: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)

    user_id = Column(UUID, ForeignKey("user.id"), nullable=False, index=True)
    

    user = relationship("User", back_populates="exercises")