from fastapi import Body, Depends
from app.schemas.exercise_schema import ExerciseCreate
from app.repositories.exercise_repository import ExerciseRepository
from app.core.db import get_async_session
from app.services.exercise_service import ExerciseService
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

exercise_router = APIRouter(
    prefix="/exercises",
    tags=["Exercise"]
)

def get_exercise_service(db: AsyncSession = Depends(get_async_session)):
    exercise_repo: ExerciseRepository = ExerciseRepository(db=db)
    return ExerciseService(exercise_repository=exercise_repo)


@exercise_router.post(
    path="/"
)
async def create_exercise(
    exercise: ExerciseCreate = Body(),
    get_exercise_service: ExerciseService = Depends(get_exercise_service)
):
    return await get_exercise_service.create_exercise(exercise=exercise)