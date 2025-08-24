from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = {"env_file": ".env"}
    PROJECT_NAME: str = "Playlist API"
    VERSION: str = "1.0"
    API_V1_STR: str = "/api/v1"
    SPOTIFY_CLIENT_ID: Optional[str] = None
    SPOTIFY_CLIENT_SECRET: Optional[str] = None
    LASTFM_API_KEY: Optional[str] = None
    LASTFM_SECRET: Optional[str] = None


settings = Settings()
