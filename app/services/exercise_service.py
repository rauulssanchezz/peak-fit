from typing import Any
from uuid import UUID
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from fastapi import status
from app.auth.user_manager import UserManager, get_user_manager
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
        except IntegrityError:
            await self.exercise_repository.db.rollback()

            raise PeakFitError("Ese nombre de ejercicio ya existe.")
        
    async def get_public_exercises(self, limit: int, offset: int):
        return await self.exercise_repository.get_public_exercises(limit=limit, offset=offset)
    
    async def get_public_exercise_by_user(
        self,
        limit: int,
        offset: int,
        user_id: UUID,
    ):
       return (
           await self.exercise_repository.get_public_exercises_by_user(
               limit=limit,
               offset=offset,
               user_id=user_id
            )
        )