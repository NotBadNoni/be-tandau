from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter
from fastapi.params import Depends

from src.controllers.user import UserController
from src.core.middlewares import get_current_user
from src.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user


@router.patch("/me", response_model=UserResponse)
@inject
async def patch_me(
        form: UserUpdate,
        use_case: FromDishka[UserController],
        user=Depends(get_current_user)
):
    return await use_case.profile_change(user.id, form)
