from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Float
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    weight: Mapped[float] = mapped_column(Float(precision=2))
    weight_goal: Mapped[float] = mapped_column(Float(precision=2))