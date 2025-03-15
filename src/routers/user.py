from fastapi import APIRouter
from fastapi.params import Depends

from src.core.middlewares import get_current_user
from src.schemas.user import UserResponse

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_me(user=Depends(get_current_user)):
    return user
