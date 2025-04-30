from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Header

from src.controllers.subject_combination import SubjectCombinationController
from src.routers import parse_language
from src.schemas.subject_combination import (
    SubjectCombinationResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[SubjectCombinationResponse])
@inject
async def list_combinations(
        controller: FromDishka[SubjectCombinationController],
        accept_language: str = Header(default="en")
):
    return await controller.list_combinations(lang=parse_language(accept_language))


@router.get("/{combination_id}")
@inject
async def get_combination(
        combination_id: int,
        controller: FromDishka[SubjectCombinationController]
):
    return await controller.get_combination(combination_id)
