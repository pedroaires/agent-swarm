from app.core.config import get_config
from app.api.endpoints import router
from contextlib import asynccontextmanager
from fastapi import FastAPI
from logging import Logger
from app.rag.ingestion import build_index
from app.core.logging import setup_logging




@asynccontextmanager
async def lifespan(app: FastAPI):
    build_index()
    yield
    Logger.info("App shutdown")

def create_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        version="0.1.0",
        # lifespan=lifespan
    )
    app.include_router(router)
    return app

setup_logging()
app = create_app()
