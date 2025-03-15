from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from src.core.store import init_db
from src.di.app_provider import create_container
from src.routers import auth
from src.routers import user

container = create_container()


def create_app():
    app = FastAPI()
    setup_dishka(container=container, app=app)
    app.include_router(router=auth.router, tags=["auth"], prefix="/auth")
    app.include_router(router=user.router, tags=["user"], prefix="/users")

    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    await init_db(await container.get(AsyncEngine))