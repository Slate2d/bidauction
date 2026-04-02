from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    database_url: str
    pool_size: int = 10
    max_overflow: int = 20
    pool_pre_ping: bool = True
    pool_recycle: int = 3600
    echo: bool = False

    class Config:
        env_file = ".env"


settings = DatabaseSettings()