from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter

from src.controllers.subject_combination import SubjectCombinationController
from src.schemas.subject_combination import (
    SubjectCombinationResponse
)

router = APIRouter(prefix="")


@router.get("", response_model=List[SubjectCombinationResponse])
@inject
async def list_combinations(
        controller: FromDishka[SubjectCombinationController],
):
    """
    List all subject combinations (e.g., (Math, Physics)).
    """
    return await controller.list_combinations()


#
#
# @router.post("", response_model=SubjectCombinationResponse)
# @inject
# async def create_combination(
#         data: SubjectCombinationCreate,
#         controller: FromDishka[SubjectCombinationController]
# ):
#     """
#     Create a new subject combination by specifying subject1_id and subject2_id.
#     """
#     try:
#         return await controller.create_combination(data.dict())
#     except BadRequestException as e:
#         raise HTTPException(status_code=400, detail=e.message)


@router.get("/{combination_id}")
@inject
async def get_combination(
        combination_id: int,
        controller: FromDishka[SubjectCombinationController]
):
    return await controller.get_combination(combination_id)

#
# @router.put("/{combination_id}", response_model=SubjectCombinationResponse)
# @inject
# async def update_combination(
#         combination_id: int,
#         data: SubjectCombinationUpdate,
#         controller: FromDishka[SubjectCombinationController]
# ):
#     """
#     Update subject1_id and/or subject2_id of an existing combination.
#     """
#     try:
#         return await controller.update_combination(combination_id, data.dict(exclude_unset=True))
#     except NotFoundException as e:
#         raise HTTPException(status_code=404, detail=e.message)
#     except BadRequestException as e:
#         raise HTTPException(status_code=400, detail=e.message)
#
#
# @router.delete("/{combination_id}")
# @inject
# async def delete_combination(
#         combination_id: int,
#         controller: FromDishka[SubjectCombinationController]
# ):
#     """
#     Delete a subject combination by ID.
#     """
#     try:
#         return await controller.delete_combination(combination_id)
#     except NotFoundException as e:
#         raise HTTPException(status_code=404, detail=e.message)
