from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Query

from src.controllers.subject_combination_specialties import SubjectCombinationSpecialtiesController
from src.core.exeptions import NotFoundException, BadRequestException

router = APIRouter(prefix="")


@router.post("/link")
@inject
async def link_specialty(
        combination_id: int = Query(..., description="ID of the subject combination"),
        specialty_id: int = Query(..., description="ID of the specialty"),
        controller: FromDishka[SubjectCombinationSpecialtiesController] = None
):
    """
    Adds a row to the 'subject_combination_specialties' table linking
    combination_id and specialty_id.
    """
    try:
        return await controller.add_specialty_to_combination(combination_id, specialty_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)


@router.delete("/link")
@inject
async def unlink_specialty(
        combination_id: int = Query(..., description="ID of the subject combination"),
        specialty_id: int = Query(..., description="ID of the specialty"),
        controller: FromDishka[SubjectCombinationSpecialtiesController] = None
):
    """
    Removes the row linking combination_id and specialty_id
    from 'subject_combination_specialties'.
    """
    try:
        return await controller.remove_specialty_from_combination(combination_id, specialty_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)
