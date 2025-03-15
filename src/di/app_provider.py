from dishka import make_async_container

from src.di.controllers import ControllersDi
from src.di.databases import DatabasesDi
from src.di.repositories import RepositoriesDi
from src.di.services import ServicesDi


def create_container():
    """Создаёт главный DI-контейнер"""
    container = make_async_container(
        DatabasesDi(),
        RepositoriesDi(),
        ServicesDi(),
        ControllersDi(),
    )

    return container
