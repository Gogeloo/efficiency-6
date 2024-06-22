# Configuration settings using pydantic BaseSettings for environment management
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    path_to_lua_files: str = "lua_files"

    class Config:
        env_file = ".env"
        extra = "ignore"  # Set to 'ignore' to allow extra fields that are not defined in the model


settings = Settings()
