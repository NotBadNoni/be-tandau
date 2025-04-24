from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Query

from src.controllers.speciality import SpecialtyController
from src.core.exeptions import NotFoundException, BadRequestException
from src.schemas.specialty import (
    SpecialtyResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[SpecialtyResponse])
@inject
async def list_specialties(
        controller: FromDishka[SpecialtyController]
):
    return await controller.list_specialties()


#
# @router.post("", response_model=SpecialtyResponse)
# @inject
# async def create_specialty(
#         data: SpecialtyCreate,
#         controller: FromDishka[SpecialtyController]
# ):
#     try:
#         return await controller.create_specialty(data.dict())
#     except BadRequestException as e:
#         raise HTTPException(status_code=400, detail=e.message)

@router.get("/by-subjects", response_model=List[SpecialtyResponse])
@inject
async def get_specialties_by_subjects(
        subject1_id: int = Query(...),
        subject2_id: int = Query(...),
        controller: FromDishka[SpecialtyController] = None
):
    try:
        return await controller.get_specialties_by_subjects(subject1_id, subject2_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.get("/{specialty_id}", response_model=SpecialtyResponse)
@inject
async def get_specialty(
        specialty_id: int,
        controller: FromDishka[SpecialtyController]
):
    try:
        return await controller.get_specialty(specialty_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)

#
# @router.put("/{specialty_id}", response_model=SpecialtyResponse)
# @inject
# async def update_specialty(
#         specialty_id: int,
#         data: SpecialtyUpdate,
#         controller: FromDishka[SpecialtyController]
# ):
#     try:
#         return await controller.update_specialty(specialty_id, data.dict(exclude_unset=True))
#     except NotFoundException as e:
#         raise HTTPException(status_code=404, detail=e.message)
#     except BadRequestException as e:
#         raise HTTPException(status_code=400, detail=e.message)
#
#
#
#
#
# @router.delete("/{specialty_id}")
# @inject
# async def delete_specialty(
#         specialty_id: int,
#         controller: FromDishka[SpecialtyController]
# ):
#     try:
#         return await controller.delete_specialty(specialty_id)
#     except NotFoundException as e:
#         raise HTTPException(status_code=404, detail=e.message)
