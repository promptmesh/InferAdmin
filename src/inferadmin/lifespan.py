from contextlib import asynccontextmanager
from fastapi import FastAPI
import logging
from inferadmin.config.loader import config_manager
from inferadmin.docker import DockerManager
from inferadmin.common.async_utils import init_thread_pools
from inferadmin.common.logging import logger, setup_logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("InferAdmin starting up")
    await config_manager.load()
    
    # Configure logging based on settings
    config = config_manager.get_config()
    log_level = getattr(logging, config.log_level, logging.INFO)
    log_file = config.log_file if config.log_file else None
    setup_logger(name="inferadmin", log_level=log_level, log_file=log_file)
    
    # Initialize thread pools with configured sizes
    init_thread_pools(
        io_pool_size=config.io_thread_pool_size,
        cpu_pool_size=config.cpu_thread_pool_size
    )
    
    # Initialize docker client
    DockerManager.init()
    logger.info("Docker client initialized")

    yield  # run fastapi app
    
    # Graceful shutdown: Clean up thread pools
    from inferadmin.common.async_utils import _io_executor, _cpu_executor
    
    logger.info("Shutting down thread pools...")
    if _io_executor:
        _io_executor.shutdown(wait=True)
    if _cpu_executor:
        _cpu_executor.shutdown(wait=True)
    logger.info("Thread pools shutdown completed.")
    
    logger.info("InferAdmin shutdown complete")
