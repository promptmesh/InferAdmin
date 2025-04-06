from fastapi import FastAPI
from inferadmin.routes import router

app = FastAPI(
    title="InferAdmin",
    description="A lightweight management interface for local LLM infrastructure."
)
app.include_router(router=router)