import uuid
from backend.app.auth.fastapi_users import FastAPIUsers
from backend.app.auth import auth_backend
from backend.app.auth.user_manager import get_user_manager
from backend.app.models.user_model import User
from app.auth.auth_backend import auth_backend

fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)