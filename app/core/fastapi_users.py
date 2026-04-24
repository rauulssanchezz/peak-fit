import uuid
from fastapi_users import FastAPIUsers
from core import auth_backend
from core.user_manager import get_user_manager
from models.user import User
from core.auth_backend import auth_backend


fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)