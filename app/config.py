from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    APP_NAME: str = "Qalam"
    DATABASE_URL: str = "sqlite:///./qalam.db"


settings = Settings()
