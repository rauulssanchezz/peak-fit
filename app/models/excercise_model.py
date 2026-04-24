import uuid
from sqlalchemy import UUID, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from core.db import Base


class Exercise(Base):
    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text())
    category: Mapped[str] = mapped_column(String(30))