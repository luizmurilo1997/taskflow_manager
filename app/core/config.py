from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration.
    Loads environment variables from .env.local file.
    """
    PROJECT_NAME: str = "TaskFlow Manager"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    API_KEY: str = "dev_api_key_super_secret"

    @property
    def SQLALCHEMY_DATABASE_URL(self) -> str:
        """
        Constructs the database URL from environment variables.

        Returns:
            str: Complete PostgreSQL connection URL
        """
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    model_config = ConfigDict(
        env_file='.env.local',
        case_sensitive=True
    )


settings = Settings()
