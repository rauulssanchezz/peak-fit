from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., validation_alias="DATABASE_URL")
    JWT_SECRET: str = Field(..., validation_alias="JWT_SECRET")
    JWT_ALG: str = Field(default="HS256", validation_alias="JWT_ALG")
    JWT_EXP: int = Field(default=60 * 24, validation_alias="JWT_EXP")
    PROJECT_NAME: str = "Peak Fit"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignora variables extra en el .env que no estén aquí
    )

settings = Settings() # type:ignore