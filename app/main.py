from fastapi import FastAPI
from dotenv import load_dotenv
from fastapi import FastAPI
from core.deps.fastapi_users import fastapi_users
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