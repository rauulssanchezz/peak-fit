from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from core.db import Base

class User(SQLAlchemyBaseUserTableUUID, Base):
    pass