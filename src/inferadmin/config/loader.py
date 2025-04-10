from .models import InferAdminConfig
from loguru import logger


class Config:
    async def load(self):
        self.config = InferAdminConfig()
        logger.info(self.get_config())

    def get_config(self) -> InferAdminConfig:
        return self.config


config_manager = Config()
