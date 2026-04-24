import uuid
from fastapi_users import schemas
from pydantic import Field


class UserRead(schemas.BaseUser[uuid.UUID]):
    weight: float = Field(gt=35, lt=400)
    goal: str = Field(min_length=0, max_length=50)

class UserCreate(schemas.BaseUserCreate):
    weight: float = Field(gt=35, lt=400)
    goal: str = Field(min_length=0, max_length=50)

class UserUpdate(schemas.BaseUserUpdate):
    weight: float = Field(gt=35, lt=400)
    goal: str = Field(min_length=0, max_length=50)