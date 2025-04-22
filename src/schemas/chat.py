from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class ChatMessageCreate(BaseModel):
    chat_id: int
    user_message: str


class ChatMessageResponse(BaseModel):
    id: int
    chat_id: int
    user_message: str
    answer_message: str
    created_at: datetime

    class Config:
        orm_mode = True


class ChatCreate(BaseModel):
    chat_name: str


class ChatResponse(BaseModel):
    id: int
    chat_name: str
    created_at: datetime
    messages: Optional[List[ChatMessageResponse]] = []

    class Config:
        orm_mode = True


class ListChats(BaseModel):
    id: int
    chat_name: str
