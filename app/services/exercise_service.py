from typing import Any, Sequence
from uuid import UUID
from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from fastapi import status
from app.auth.user_manager import UserManager, get_user_manager
from app.core.exceptions import PeakFitError
from app.models.excercise_model import Exercise
from app.schemas.exercise_schema import ExerciseCreate, ExerciseUpdate
from app.repositories.exercise_repository import ExerciseRepository

class ExerciseService:
    def __init__(self, exercise_repository: ExerciseRepository) -> None:
        self.exercise_repository: ExerciseRepository = exercise_repository

    async def create_exercise(self, exercise: ExerciseCreate) -> str:
        exercise_data: dict[str, Any] = exercise.model_dump()

        try:
            return await self.exercise_repository.create_exercise(exercise=exercise_data)
        except IntegrityError:
            await self.exercise_repository.db.rollback()

            raise PeakFitError("Ese nombre de ejercicio ya existe.")
        
    async def get_public_exercises(self, limit: int, offset: int) -> Sequence[Exercise]:
        return await self.exercise_repository.get_public_exercises(limit=limit, offset=offset)
    
    async def get_public_exercise_by_user(
        self,
        limit: int,
        offset: int,
        user_id: UUID,
    ) -> Sequence[Exercise]:
       return (
           await self.exercise_repository.get_public_exercises_by_user(
               limit=limit,
               offset=offset,
               user_id=user_id
            )
        )
    
    async def get_users_private_exercise(
        self,
        user_id: UUID,
        limit: int,
        offset: int
    ) -> Sequence[Exercise]:
        return await self.get_users_private_exercise(user_id=user_id, limit=limit, offset=offset)
    
    async def update_exercise(self, exercise: ExerciseUpdate):
        return await self.exercise_repository.update_exercise(exercise=exercise)