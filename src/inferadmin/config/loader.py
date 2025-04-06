from .models import InferAdminConfig

class Config:
    async def load(self):
        self.config = InferAdminConfig()
        print(self.get_config())

    def get_config(self) -> InferAdminConfig:
        return self.config
    
config_manager = Config()