# from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class InferAdminConfig(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_prefix="INFERADMIN_", extra="ignore"
    )

    model_storage_path: str
    hf_token: str
