from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware

from src import SubjectCombinationSpecialtiesAdmin
from src.core.config import MEDIA_DIR
from src.di.app_provider import create_container
from src.models import sqlalchemy_models
from src.routers import (
    auth,
    subject,
    speciality,
    subject_combination,
    subject_combination_specialties,
    university_specialties,
    chat
)
from src.routers import university
from src.routers import user

container = create_container()

from sqladmin import ModelView


def register_models(admin, models: list[type]):
    for model in models:
        class ModelViewClass(ModelView, model=model):
            column_list = [c.name for c in model.__table__.columns]
            form_include_pk = True

        admin.add_view(ModelViewClass)
    admin.add_view(SubjectCombinationSpecialtiesAdmin)


def create_app():
    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(ProxyHeadersMiddleware)
    app.mount('/media', StaticFiles(directory=MEDIA_DIR), name='media')
    setup_dishka(container=container, app=app)
    app.include_router(router=auth.router, tags=["auth"], prefix="/api/v1/auth")
    app.include_router(router=user.router, tags=["user"], prefix="/api/v1/users")
    app.include_router(router=university.router, tags=["university"], prefix="/api/v1/universities")
    app.include_router(subject.router, prefix="/api/v1/subjects", tags=["subjects"])
    app.include_router(speciality.router, prefix="/api/v1/specialties", tags=["specialties"])
    app.include_router(subject_combination.router, prefix="/api/v1/subject-combinations", tags=["subject combinations"])
    app.include_router(subject_combination_specialties.router, prefix="/api/v1/subject-combinations-specialties",
                       tags=["subject combinations specialties"])
    app.include_router(university_specialties.router, prefix="/api/v1//university-specialties",
                       tags=["university specialties"])
    app.include_router(chat.router, prefix="/api/v1/chat", tags=["ai chat"])
    return app


app = create_app()


async def register_admin(app) -> Admin:
    admin = Admin(app, await container.get(AsyncEngine))

    register_models(admin, sqlalchemy_models)
    return admin


@app.on_event("startup")
async def on_startup():
    await register_admin(app)
