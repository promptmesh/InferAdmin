from pydantic_settings import BaseSettings, SettingsConfigDict


class InferAdminConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="INFERADMIN_", extra="ignore"
    )

    # Storage paths
    model_storage_path: str
    
    # Authentication tokens
    hf_token: str
    
    # Thread pool settings
    io_thread_pool_size: int = 10
    cpu_thread_pool_size: int = 0  # 0 means use CPU count - 1
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: str = ""  # Empty means log to console only
