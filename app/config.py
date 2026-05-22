from pydantic_settings import BaseSettings,SettingsConfigDict


class DbSettings(BaseSettings):
    POSTGRES_Server : str
    POSTGRES_PORT: int
    POSTGRES_USER:str
    POSTGRES_PASSWORD:str  
    POSTGRES_DB : str

    REDIS_HOST : str
    REDIS_PORT : str

    model_config = SettingsConfigDict(
        env_file="./.env",
        env_ignore = True,
        extra= "ignore",
    )
    @property
    def POSTGRES_URL (self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_Server}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


Db_settings= DbSettings()


class SecuritySettings(BaseSettings):
    JWT_SECRET : str
    JWT_ALGORITHM : str


    model_config=SettingsConfigDict(
        env_file="./.env",
        env_ignore= True,
        extra="ignore",
    )

security_settings = SecuritySettings()