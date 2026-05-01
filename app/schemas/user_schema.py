from enum import Enum
import uuid
from fastapi_users import schemas
from pydantic import Field

class Goals(str, Enum):
    GAIN_WEIGHT = "Ganar Peso."
    LOSE_WEIGHT = "Perder Peso."
    DEFINITION = "Definir."
    VOLUME = "Volumen."
    FIT = "Estar en forma."

class Genre(str, Enum):
    MALE = "Hombre"
    FEMALE = "Mujer"


class UserRead(schemas.BaseUser[uuid.UUID]):
    weight: float = Field(gt=35, lt=400)
    goal: Goals
    genre: Genre

class UserCreate(schemas.BaseUserCreate):
    weight: float = Field(gt=35, lt=400)
    goal: Goals
    genre: Genre

class UserUpdate(schemas.BaseUserUpdate):
    weight: float = Field(gt=35, lt=400)
    goal: Goals
    genre: Genre