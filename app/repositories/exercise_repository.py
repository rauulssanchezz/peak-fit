from typing import Any
from app.models.excercise_model import Exercise
from app.schemas.exercise_schema import ExerciseCreate
from sqlalchemy.ext.asyncio import  AsyncSession

class ExerciseRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create_exercise(self, exercise: dict[str, Any]) -> str:
        exercise_model: Exercise = Exercise(**exercise)

        self.db.add(exercise_model)
        await self.db.commit()

        return "Ejercicio creado con éxito."