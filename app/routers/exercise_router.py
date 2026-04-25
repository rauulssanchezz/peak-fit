from uuid import UUID

from fastapi import Body, Depends, Path, Query
from app.models.user_model import User
from app.schemas.exercise_schema import ExerciseCreate, ExerciseIn
from app.repositories.exercise_repository import ExerciseRepository
from app.core.db import get_async_session
from app.schemas.public_request import PublicRequest
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

@exercise_router.get(
    path="/public-exercises"
)
async def get_public_exercises(
    params: PublicRequest = Query(),
    get_exercise_service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(current_user)
):
    return await get_exercise_service.get_public_exercises(limit=params.limit, offset=params.offset)

@exercise_router.get(
    path="/public-exercises/{user_id}"
)
async def get_public_exercises_by_user_id(
    params: PublicRequest = Query(),
    user_id: UUID = Path(),
    get_exercise_service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(current_user)
):
    return (
        await get_exercise_service.get_public_exercise_by_user(
            limit=params.limit,
            offset=params.offset,
            user_id=user_id
        )
    )

@exercise_router.get(
    path="/private-exercises"
)
async def get_users_private_exercise(
    params: PublicRequest = Query(),
    get_exercise_service: ExerciseService = Depends(get_exercise_service),
    user: User = Depends(current_user)
):
    user_id = user.id
    return (
        await get_exercise_service.get_public_exercise_by_user(
            limit=params.limit,
            offset=params.offset,
            user_id=user_id
        )
    )