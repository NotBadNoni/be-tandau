from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Query, Header

from src.controllers.speciality import SpecialtyController
from src.routers import parse_language
from src.schemas.specialty import (
    SpecialtyResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[SpecialtyResponse])
@inject
async def list_specialties(
        controller: FromDishka[SpecialtyController],
        accept_language: str = Header(default="en")
):
    return await controller.list_specialties(language=parse_language(accept_language))


@router.get("/by-subjects", response_model=List[SpecialtyResponse])
@inject
async def get_specialties_by_subjects(
        subject1_id: int = Query(...),
        subject2_id: int = Query(...),
        controller: FromDishka[SpecialtyController] = None,
        accept_language: str = Header(default="en")
):
    return await controller.get_specialties_by_subjects(subject1_id, subject2_id,
                                                        language=parse_language(accept_language))


@router.get("/{specialty_id}", response_model=SpecialtyResponse)
@inject
async def get_specialty(
        specialty_id: int,
        controller: FromDishka[SpecialtyController],
        accept_language: str = Header(default="en")
):
    return await controller.get_specialty(specialty_id, language=parse_language(accept_language))
