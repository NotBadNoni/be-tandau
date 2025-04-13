from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.controllers.chat import ChatController
from src.core.middlewares import get_current_user
from src.schemas.chat import ChatCreate, ChatMessageCreate, ChatResponse, ChatMessageResponse

router = APIRouter(prefix="/chat")


@router.post("/")
@inject
async def create_chat(
        data: ChatCreate,
        controller: FromDishka[ChatController],
        user=Depends(get_current_user)
):
    return await controller.create_chat(user.id, data.chat_name)


@router.post("/message", response_model=ChatMessageResponse)
@inject
async def send_message(
        data: ChatMessageCreate,
        controller: FromDishka[ChatController]
):
    return await controller.send_message(data.chat_id, data.user_message)


@router.get("/{chat_id}", response_model=ChatResponse)
@inject
async def get_chat(
        chat_id: int,
        controller: FromDishka[ChatController]
):
    return await controller.get_chat(chat_id)
