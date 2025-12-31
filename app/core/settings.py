from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # -------------------------
    # Application
    # -------------------------
    app_name: str = "FastAPI MDC Logger"
    environment: str = "local"
    debug: bool = True
    enable_profiler: bool = True

    # -------------------------
    # Server
    # -------------------------
    host: str = "localhost"
    port: int = 8000

    # -------------------------
    # Logging
    # -------------------------
    log_level: str = "DEBUG"
    log_to_file: bool = True
    log_to_console: bool = True

    # -------------------------
    # Database
    # -------------------------
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "mydb"
    db_user: str = "postgres"
    db_password: str = "postgres"

    db_pool_size: int = 40
    db_max_overflow: int = 80
    db_pool_timeout: int = 60
    db_pool_recycle: int = 1800

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    class Config:
        env_file = ".env"
        env_prefix = ""
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings instance.
    Loaded once per process.
    """
    return Settings()
