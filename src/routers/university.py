from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Query

from src.controllers.university import UniversityController
from src.core.exeptions import BadRequestException, NotFoundException
from src.schemas.university import (
    UniversityCreate,
    UniversityUpdate,
    UniversityResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[UniversityResponse])
@inject
async def list_universities(
        controller: FromDishka[UniversityController]
):
    return await controller.get_universities()


@router.post("", response_model=UniversityResponse)
@inject
async def create_university(
        data: UniversityCreate,
        controller: FromDishka[UniversityController]
):
    """
    data: { "name": "...", "image": "...", "description": "...", etc. }
    """
    try:
        return await controller.create_university(data.dict())
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{university_id}", response_model=UniversityResponse)
@inject
async def get_university(
        university_id: int,
        controller: FromDishka[UniversityController]
):
    try:
        return await controller.get_university(university_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put("/{university_id}", response_model=UniversityResponse)
@inject
async def update_university(
        university_id: int,
        data: UniversityUpdate,
        controller: FromDishka[UniversityController]
):
    try:
        return await controller.update_university(university_id, data.dict(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.delete("/{university_id}")
@inject
async def delete_university(
        university_id: int,
        controller: FromDishka[UniversityController]
):
    try:
        return await controller.delete_university(university_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/by-specialty/{specialty_id}", response_model=List[UniversityResponse])
@inject
async def get_universities_by_specialty(
        specialty_id: int,
        controller: FromDishka[UniversityController]
):
    """
    Return all universities offering the given specialty.
    """
    return await controller.get_universities_by_specialty(specialty_id)


@router.get("/by-country", response_model=List[UniversityResponse])
@inject
async def get_by_country(
        country_name: str = Query(...),
        controller: FromDishka[UniversityController] = None
):
    return await controller.get_universities_by_country(country_name)
