from fastapi import Depends
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy.db import DatabaseStrategy
import os
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
from deps.fastapi_users import get_access_token_db
from core.config import settings

SECRET = str(os.getenv("JWT_SECRET"))

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

def get_database_strategy(
    access_token_db: SQLAlchemyAccessTokenDatabase = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=settings.JWT_EXP)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)