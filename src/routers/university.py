from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Query, Header

from src.controllers.university import UniversityController
from src.core.exeptions import NotFoundException
from src.routers import parse_language
from src.schemas.university import (
    UniversityResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[UniversityResponse])
@inject
async def list_universities(
        controller: FromDishka[UniversityController],
        accept_language: str = Header(default="en")
):
    return await controller.get_universities(language=parse_language(accept_language))


@router.get("/by-country", response_model=List[UniversityResponse])
@inject
async def get_by_country(
        country_name: str = Query(...),
        controller: FromDishka[UniversityController] = None,
        accept_language: str = Header(default="en")
):
    return await controller.get_universities_by_country(
        country_name, language=parse_language(accept_language)
    )


@router.get("/{university_id}", response_model=UniversityResponse)
@inject
async def get_university(
        university_id: int,
        controller: FromDishka[UniversityController],
        accept_language: str = Header(default="en")
):
    try:
        return await controller.get_university(university_id, language=parse_language(accept_language))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.get("/by-specialty/{specialty_id}", response_model=List[UniversityResponse])
@inject
async def get_universities_by_specialty(
        specialty_id: int,
        controller: FromDishka[UniversityController],
        accept_language: str = Header(default="en")
):
    return await controller.get_universities_by_specialty(
        specialty_id, language=parse_language(accept_language)
    )
