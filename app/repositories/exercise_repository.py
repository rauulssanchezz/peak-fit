from typing import Any
from uuid import UUID
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy import select, update, delete
from typing import Sequence
from app.models.excercise_model import Exercise
from sqlalchemy.ext.asyncio import  AsyncSession

from app.schemas.exercise_schema import ExerciseUpdate

class ExerciseRepository:

    def __init__(self, db: AsyncSession) -> None:
        self.db: AsyncSession = db

    async def create_exercise(self, exercise: dict[str, Any]) -> str:
        exercise_model: Exercise = Exercise(**exercise)

        self.db.add(exercise_model)
        await self.db.commit()

        return "Ejercicio creado con éxito."
    
    async def get_public_exercises(self, limit: int, offset: int) -> Sequence[Exercise]:
        query = select(Exercise).where(Exercise.is_public==True).offset(offset=offset).limit(limit=limit)

        db_result = await self.db.execute(query)

        return db_result.scalars().all()
    
    async def get_public_exercises_by_user(self, limit: int, offset: int, user_id: UUID) -> Sequence[Exercise]:
        query = (
            select(Exercise)
            .where(Exercise.is_public==True)
            .where(Exercise.user_id==user_id)
            .offset(offset=offset)
            .limit(limit=limit)
        )

        db_result = await self.db.execute(query)

        return db_result.scalars().all()

    async def get_users_private_exercise(
        self,
        user_id: UUID,
        limit: int,
        offset: int
    ) -> Sequence[Exercise]:
        query = (
            select(Exercise)
            .where(Exercise.is_public==False)
            .where(Exercise.user_id==user_id)
            .limit(limit=limit)
            .offset(offset=offset)
        )

        db_results = await self.db.execute(query)

        return db_results.scalars().all()

    async def update_exercise(self, exercise: ExerciseUpdate) -> Exercise | None:
        exercise_data = exercise.model_dump()
        query = (
            update(Exercise)
            .where(Exercise.id==exercise.id)
            .where(Exercise.user_id==exercise.user_id)
            .values(**exercise_data)
            .returning(Exercise)
        )

        db_results = await self.db.execute(query)
        await self.db.commit()

        return db_results.scalar_one_or_none()
    
    async def delete_exercise(self, exercise_id: UUID, user_id: UUID_ID) -> None:
        query = (
            delete(Exercise)
            .where(Exercise.id==exercise_id)
            .where(Exercise.user_id==user_id)
        )
        await self.db.execute(query)
        await self.db.commit()

    async def get_exercise(self, exercise_id: UUID, user_id: UUID_ID) -> Exercise | None:
        query = (
            select(Exercise)
            .where(Exercise.id==exercise_id)
            .where(Exercise.is_public==True or Exercise.user_id==user_id)
        )

        db_result = await self.db.execute(query)

        return db_result.scalar_one_or_none()