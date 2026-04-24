from fastapi import FastAPI
from dotenv import load_dotenv
import uuid
from fastapi import FastAPI
from fastapi_users import FastAPIUsers
from core.auth_backend import auth_backend
from models.user import User
from core.user_manager import get_user_manager

load_dotenv()

app = FastAPI(
    title="Peak Fit"
)

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

app = FastAPI()
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)