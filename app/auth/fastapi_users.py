import uuid
from fastapi_users import FastAPIUsers
from app.auth import auth_backend
from app.auth.user_manager import get_user_manager
from models.user_model import User
from auth.auth_backend import auth_backend


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)