from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Playlist API"
    VERSION: str = "1.0"
    API_V1_STR: str = "/api/v1"

    class Config:
        env_file = "api/.env"


settings = Settings()
