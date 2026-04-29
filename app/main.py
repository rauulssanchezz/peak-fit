from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI
from app.routers.routers import exercise_router
from app.schemas.user_schema import UserCreate, UserRead, UserUpdate
from app.auth.fastapi_users import fastapi_users
from app.auth.auth_backend import auth_backend
from app.errors.error_handler import register_error_handlers

load_dotenv()

app = FastAPI(
    title="Peak Fit"
)

register_error_handlers(app)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

# TODO
# app.include_router(
#     fastapi_users.get_users_router(UserRead, UserUpdate, requires_verification=True),
#     prefix="/users",
#     tags=["users"],
# )

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

app.include_router(
    exercise_router
)