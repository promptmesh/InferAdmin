from contextlib import asynccontextmanager
from fastapi import FastAPI
from inferadmin.config.loader import config_manager
from inferadmin.docker import DockerManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await config_manager.load()
    await DockerManager.init()
    
    yield # run fastapi app
    
    await DockerManager.close()