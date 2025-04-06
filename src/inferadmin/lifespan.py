from contextlib import asynccontextmanager
from fastapi import FastAPI
from inferadmin.config.loader import config_manager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await config_manager.load()
    yield