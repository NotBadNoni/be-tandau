from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, HTTPException, Depends

from src.controllers.user import UserController
from src.core.exeptions import BadRequestException, NotFoundException
from src.core.middlewares import get_current_user
from src.schemas.user import (
    UserUpdate,
    UserResponse, )

router = APIRouter(prefix="")


@router.get("/me", response_model=UserResponse)
@inject
async def me(
        controller: FromDishka[UserController],
        current_user=Depends(get_current_user)
):
    try:
        updated_user = await controller.profile_user(current_user.id)
        return updated_user
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)


@router.patch("/me", response_model=UserResponse)
@inject
async def patch_me(
        data: UserUpdate,
        controller: FromDishka[UserController],
        current_user=Depends(get_current_user)
):
    try:
        updated_user = await controller.profile_change(current_user.id, data)
        return updated_user
    except BadRequestException as e:
        raise HTTPException(status_code=400, detail=e.message)
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.message)
