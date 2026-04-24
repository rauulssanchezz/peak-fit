from fastapi import Body, Depends
from app.models.user_model import User
from app.schemas.exercise_schema import ExerciseCreate, ExerciseIn
from app.repositories.exercise_repository import ExerciseRepository
from app.core.db import get_async_session
from app.services.exercise_service import ExerciseService
from fastapi.routing import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.auth.fastapi_users import current_user

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
    exercise_in: ExerciseIn = Body(),
    get_exercise_service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(current_user)
):
    exercise: ExerciseCreate = ExerciseCreate(**exercise_in.model_dump(), user_id=user.id)
    return await get_exercise_service.create_exercise(exercise=exercise)