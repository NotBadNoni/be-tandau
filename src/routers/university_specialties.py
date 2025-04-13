from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Query

from src.controllers.university_specialties import UniversitySpecialtiesController
from src.core.exeptions import NotFoundException, BadRequestException

router = APIRouter(prefix="")

@router.post("/link")
@inject
async def link_specialty_to_university(
    university_id: int = Query(..., description="ID of the university"),
    specialty_id: int = Query(..., description="ID of the specialty"),
    controller: FromDishka[UniversitySpecialtiesController] = None
):
    try:
        return await controller.add_specialty_to_university(university_id, specialty_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)

@router.delete("/link")
@inject
async def unlink_specialty_from_university(
    university_id: int = Query(..., description="ID of the university"),
    specialty_id: int = Query(..., description="ID of the specialty"),
    controller: FromDishka[UniversitySpecialtiesController] = None
):
    try:
        return await controller.remove_specialty_from_university(university_id, specialty_id)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)
