from pydantic import ConfigDict
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:root@localhost:5432/dbname"
    API_KEY: str = "static_api_key"

    model_config = ConfigDict(
        env_file = ".env"
    )

settings = Settings()
