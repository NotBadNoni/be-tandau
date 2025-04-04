from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.controllers.university import UniversityController
from src.schemas.university import CreateUniversity, UpdateUniversity, UniversityResponse

router = APIRouter(prefix="")


@router.get("/")
@inject
async def get_universities(
        controller: FromDishka[UniversityController],
):
    return await controller.get_universities()


@router.get("/{university_id}")
@inject
async def get_university(
        university_id: int,
        controller: FromDishka[UniversityController],
):
    return await controller.get_university(university_id)


@router.post("/")
@inject
async def create_university(
        form: CreateUniversity,
        controller: FromDishka[UniversityController],
):
    return await controller.create_university(form.dict())


@router.put("/{university_id}")
@inject
async def update_university(
        university_id: int,
        form: UpdateUniversity,
        controller: FromDishka[UniversityController],
):
    return await controller.update_university(university_id, form.dict(exclude_unset=True))


@router.delete("/{university_id}")
@inject
async def delete_university(
        university_id: int,
        controller: FromDishka[UniversityController],
):
    return await controller.delete_university(university_id)
