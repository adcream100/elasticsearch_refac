from fastapi import FastAPI

from app.di.container import Container

from fastapi.middleware.cors import CORSMiddleware
from core.infrastructure.middleware.logging import AccessLoggingMiddleware

from router.keyword_router import router as keyword_router

container = None

def register_middleware(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(AccessLoggingMiddleware)

def register_router(app: FastAPI) -> None:
    app.include_router(keyword_router)

def create_container():
    container = Container()
    container.wire(packages=["router"])
    container.config.from_yaml("./config.yml")

    return container

def create_app():
    global container
    container = create_container()

    app = FastAPI(docs_url="/docs")
    register_middleware(app)
    register_router(app)

app = create_app()