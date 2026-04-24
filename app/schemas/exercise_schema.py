from enum import Enum
import uuid
from pydantic import BaseModel, Field

class ExerciseCategory(str, Enum):
    CHEST = "Chest"
    BACK = "Back"
    BICEPS = "Bíceps"
    TRICEPS = "Triceps"

class ExerciseIn(BaseModel):
    name: str = Field(min_length=5, max_length=50)
    description: str
    category: ExerciseCategory

class ExerciseCreate(ExerciseIn):
    user_id: uuid.UUID