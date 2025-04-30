from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Header

from src.controllers.subject import SubjectController
from src.routers import parse_language
from src.schemas.subject import (
    SubjectResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[SubjectResponse])
@inject
async def list_subjects(
        controller: FromDishka[SubjectController],
        accept_language: str = Header(default="en")
):
    lang = parse_language(accept_language)
    return await controller.list_subjects(lang)


@router.get("/{subject_id}", response_model=SubjectResponse)
@inject
async def get_subject(
        subject_id: int,
        controller: FromDishka[SubjectController],
        accept_language: str = Header(default="en")
):
    lang = parse_language(accept_language)
    return await controller.get_subject(subject_id, lang)
