from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.staticfiles import StaticFiles

from src.core.config import MEDIA_DIR
from src.core.store import init_db
from src.di.app_provider import create_container
from src.routers import auth
from src.routers import user
from src.routers import university

container = create_container()


def create_app():
    app = FastAPI()
    app.mount('/media', StaticFiles(directory=MEDIA_DIR), name='media')
    setup_dishka(container=container, app=app)
    app.include_router(router=auth.router, tags=["auth"], prefix="/auth")
    app.include_router(router=user.router, tags=["user"], prefix="/users")
    app.include_router(router=university.router, tags=["university"], prefix="/universities")
    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    await init_db(await container.get(AsyncEngine))
