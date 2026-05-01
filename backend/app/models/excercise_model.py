import uuid
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import UUID, Boolean, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.app.core.db import Base


class Exercise(Base):
    __tablename__ = "exercise"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(Text(), nullable=False)
    category: Mapped[str] = mapped_column(String(30), index=True, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True, index=True, nullable=False)

    user_id: Mapped[UUID_ID] = mapped_column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False, index=True)
    

    user = relationship("User", back_populates="exercises")