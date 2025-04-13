from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException

from src.controllers.subject import SubjectController
from src.core.exeptions import NotFoundException, BadRequestException
from src.schemas.subject import (
    SubjectCreate,
    SubjectUpdate,
    SubjectResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[SubjectResponse])
@inject
async def list_subjects(
        controller: FromDishka[SubjectController]
):
    """
    Returns a list of all subjects.
    """
    return await controller.list_subjects()


@router.post("", response_model=SubjectResponse)
@inject
async def create_subject(
        data: SubjectCreate,
        controller: FromDishka[SubjectController]
):
    """
    Creates a new subject (e.g., Math, Physics).
    """
    try:
        return await controller.create_subject(data.dict())
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{subject_id}", response_model=SubjectResponse)
@inject
async def get_subject(
        subject_id: int,
        controller: FromDishka[SubjectController],
):
    """
    Retrieve a single subject by ID.
    """
    try:
        return await controller.get_subject(subject_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.put("/{subject_id}", response_model=SubjectResponse)
@inject
async def update_subject(
        subject_id: int,
        data: SubjectUpdate,
        controller: FromDishka[SubjectController],
):
    """
    Update subject name (e.g., rename 'Math' to 'Mathematics').
    """
    try:
        return await controller.update_subject(subject_id, data.dict(exclude_unset=True))
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete("/{subject_id}")
@inject
async def delete_subject(
        subject_id: int,
        controller: FromDishka[SubjectController],
):
    """
    Delete a subject by ID.
    """
    try:
        return await controller.delete_subject(subject_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
