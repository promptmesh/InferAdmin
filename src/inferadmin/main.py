from fastapi import FastAPI
from inferadmin.routes import router
from .openapi_tags import tags_metadata

app = FastAPI(
    title="InferAdmin",
    description="A lightweight management interface for local LLM infrastructure.",
    tags_metadata=tags_metadata
)
app.include_router(router=router)