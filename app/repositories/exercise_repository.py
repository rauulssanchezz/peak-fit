from typing import Any
from uuid import UUID
from sqlalchemy import select
from typing import Sequence
from app.models.excercise_model import Exercise
from sqlalchemy.ext.asyncio import  AsyncSession

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
