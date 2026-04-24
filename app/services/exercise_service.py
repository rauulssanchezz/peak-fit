from typing import Any
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import PeakFitError
from app.schemas.exercise_schema import ExerciseCreate
from app.repositories.exercise_repository import ExerciseRepository

class ExerciseService:
    def __init__(self, exercise_repository: ExerciseRepository) -> None:
        self.exercise_repository: ExerciseRepository = exercise_repository

    async def create_exercise(self, exercise: ExerciseCreate):
        exercise_data: dict[str, Any] = exercise.model_dump()

        try:
            return await self.exercise_repository.create_exercise(exercise=exercise_data)
        except IntegrityError as error:
            await self.exercise_repository.db.rollback()

            raise PeakFitError("Ese nombre de ejercicio ya existe.")
    