from typing import Any, Sequence
from uuid import UUID
from fastapi_users_db_sqlalchemy import UUID_ID
from sqlalchemy.exc import IntegrityError
from fastapi import status
from backend.app.core.groq import GroqClient
from backend.app.errors.exceptions import PeakFitError
from backend.app.models.excercise_model import Exercise
from backend.app.schemas.exercise_schema import ExerciseCreate, ExerciseUpdate
from backend.app.repositories.exercise_repository import ExerciseRepository
from groq.types.chat import ChatCompletionMessageParam

class ExerciseService:
    def __init__(
            self,
            exercise_repository: ExerciseRepository,
            groq_client: GroqClient
        ) -> None:
        self.exercise_repository: ExerciseRepository = exercise_repository
        self.groq_client: GroqClient = groq_client

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
    
    async def update_exercise(self, exercise: ExerciseUpdate) -> Exercise:
        result: Exercise | None = await self.exercise_repository.update_exercise(exercise=exercise)
        if result is None:
            raise PeakFitError(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No se encuentra el ejercicio"
            )
        
        return result
    
    async def delete_exercise(self, exercise_id: UUID, user_id: UUID_ID) -> None:
        await self.exercise_repository.delete_exercise(exercise_id=exercise_id, user_id=user_id)

    async def get_exercise(self, exercise_id: UUID, user_id: UUID_ID) -> Exercise:
        result: Exercise | None = await self.exercise_repository.get_exercise(exercise_id=exercise_id, user_id=user_id)
        if result is None:
            raise PeakFitError(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No se encuentra el ejercicio"
            )
        
        return result
    
    async def resume_exercise(self, exercise_id: UUID, user_id: UUID_ID) -> str:
        exercise: Exercise | None = await self.exercise_repository.get_exercise(exercise_id=exercise_id, user_id=user_id)
        if exercise is None:
            raise PeakFitError(
                status_code=status.HTTP_404_NOT_FOUND,
                message="No se encuentra el ejercicio"
            )
        
        system_message: ChatCompletionMessageParam = {
            "role": "system",
            "content": ("Eres un experto en fitnnes, explicas los ejercicios que"
                "se te pasan y das recomendaciones ademas de aportar enlaces de videos"
                " y o imágenes de ejemplo. Si no tienes videos o imagenes no pases nada."
                "Bajo ningún concepto envies videos de memes o inapropiados,"
                " si no estan relacionados con el ejercicio no los mandes.")
        }

        user_message: ChatCompletionMessageParam = {
            "role": "user",
            "content": (
                "Resume y explica este ejercicio, además da consejos y proporciona "
                "enlaces para ver vídeos y o fotos de ejmplo: "
                f"Nombre: {exercise.name}, Descripcion: {exercise.description}, Categoria: {exercise.category}"
            )
        }
        
        return str(await self.groq_client.chat_completion(
            system_message=system_message,
            user_message=user_message
        ))