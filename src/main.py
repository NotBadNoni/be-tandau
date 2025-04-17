from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.core.config import MEDIA_DIR
from src.core.store import init_db
from src.di.app_provider import create_container
from src.routers import auth, subject, speciality, subject_combination, subject_combination_specialties, university_specialties, chat
from src.routers import university
from src.routers import user

container = create_container()


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.mount('/media', StaticFiles(directory=MEDIA_DIR), name='media')
    setup_dishka(container=container, app=app)
    app.include_router(router=auth.router, tags=["auth"], prefix="/api/v1/auth")
    app.include_router(router=user.router, tags=["user"], prefix="/api/v1/users")
    app.include_router(router=university.router, tags=["university"], prefix="/api/v1/universities")
    app.include_router(subject.router, prefix="/api/v1/subjects", tags=["subjects"])
    app.include_router(speciality.router, prefix="/api/v1/specialties", tags=["specialties"])
    app.include_router(subject_combination.router, prefix="/api/v1/subject-combinations", tags=["subject combinations"])
    app.include_router(subject_combination_specialties.router, prefix="/api/v1/subject-combinations-specialties", tags=["subject combinations specialties"])
    app.include_router(university_specialties.router, prefix="/api/v1//university-specialties", tags=["university specialties"])
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["ai chat"])
    return app


app = create_app()


@app.on_event("startup")
async def on_startup():
    await init_db(await container.get(AsyncEngine))
