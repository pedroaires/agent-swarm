from fastapi import FastAPI
from app.core.config import get_config
from app.endpoints import router


def create_app() -> FastAPI:
    config = get_config()
    app = FastAPI(
        version="0.1.0"
    )
    app.include_router(router)
    return app


app = create_app()
