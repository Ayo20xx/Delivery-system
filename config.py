from pydantic_settings import BaseSettings,SettingsConfigDict


class DbSettings(BaseSettings):
    POSTGRES_Server : str
    POSTGRES_PORT: int
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str  
    POSTGRES_DB : str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore = True,
        extra= "ignore",
    )
    @property
    def POSTGRES_URL (self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@host:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings= DbSettings()

