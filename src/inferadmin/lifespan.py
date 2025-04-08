from contextlib import asynccontextmanager
from fastapi import FastAPI
from inferadmin.config.loader import config_manager
from inferadmin.docker import DockerManager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await config_manager.load()
    DockerManager.init()
    
    yield # run fastapi app