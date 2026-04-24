from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI
from schemas.user import UserCreate, UserRead, UserUpdate
from core.fastapi_users import fastapi_users
from core.auth_backend import auth_backend

load_dotenv()

app = FastAPI(
    title="Peak Fit"
)

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