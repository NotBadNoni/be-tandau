from typing import List

from dishka import FromDishka
from dishka.integrations.fastapi import inject
from fastapi import APIRouter, Depends

from src.controllers.chat import ChatController
from src.core.middlewares import get_current_user
from src.schemas.chat import ChatCreate, ChatMessageCreate, ChatResponse, ChatMessageResponse, ListChats

router = APIRouter(prefix="/chats")


@router.get("/", response_model=List[ListChats])
@inject
async def get_all_chats(
        controller: FromDishka[ChatController],
        user=Depends(get_current_user)
):
    return await controller.get_chats(user.id)


@router.post("/", response_model=ListChats)
@inject
async def create_chat(
        data: ChatCreate,
        controller: FromDishka[ChatController],
        user=Depends(get_current_user)
):
    return await controller.create_chat(user.id, data.chat_name)


@router.post("/message")
@inject
async def send_message(
        data: ChatMessageCreate,
        controller: FromDishka[ChatController],
        user=Depends(get_current_user)
):
    return await controller.send_message(data.chat_id, data.user_message, user.id)


@router.get("/{chat_id}", response_model=ChatResponse)
@inject
async def get_chat(
        chat_id: int,
        controller: FromDishka[ChatController]
):
    return await controller.get_chat(chat_id)
