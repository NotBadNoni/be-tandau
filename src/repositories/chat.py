from __future__ import annotations

import math
from dataclasses import dataclass
from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.models.chat import Chat
from src.models.chat_messages import ChatMessages


@dataclass(slots=True)
class MessageDTO:
    content: str
    is_user: bool


class ChatRepository:

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create_chat(self, user_id: int, chat_name: str) -> Chat:
        stmt = (
            insert(Chat)
            .values(user_id=user_id, chat_name=chat_name)
            .returning(Chat)
        )
        res = await self._session.execute(stmt)
        return res.scalar_one()

    async def get_chat_with_messages(self, chat_id: int) -> Chat | None:
        stmt = (
            select(Chat)
            .options(selectinload(Chat.messages))
            .where(Chat.id == chat_id)
        )
        res = await self._session.execute(stmt)
        return res.unique().scalar_one_or_none()

    async def get_chats(self, user_id: int) -> List[Chat]:
        stmt = select(Chat).where(Chat.user_id == user_id)
        res = await self._session.execute(stmt)
        return res.scalars().all()

    async def get_user_chats(self, user_id: int, chat_id) -> Chat:
        stmt = select(Chat).where(Chat.user_id == user_id, Chat.id == chat_id)
        res = await self._session.execute(stmt)
        return res.scalars().first()


class ChatMessageRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_message(self, chat_id: int, user_message: str, answer_message: str) -> ChatMessages:
        message = ChatMessages(
            chat_id=chat_id,
            user_message=user_message,
            answer_message=answer_message,
        )
        self._session.add(message)
        await self._session.flush()
        return message

    async def list_chat_messages(self, chat_id: int) -> List[ChatMessages]:
        stmt = (
            select(ChatMessages)
            .where(ChatMessages.chat_id == chat_id)
            .order_by(ChatMessages.created_at.asc())
        )
        res = await self._session.execute(stmt)
        return res.scalars().all()

    async def get_last_messages(
            self, chat_id: int, *, limit: int = 10
    ) -> List[MessageDTO]:
        row_limit = max(1, math.ceil(limit / 2))
        stmt = (
            select(ChatMessages)
            .where(ChatMessages.chat_id == chat_id)
            .order_by(ChatMessages.created_at.desc())
            .limit(row_limit)
        )
        res = await self._session.execute(stmt)
        rows: List[ChatMessages] = res.scalars().all()

        flattened: List[MessageDTO] = []
        for row in reversed(rows):
            flattened.append(MessageDTO(content=row.user_message, is_user=True))
            flattened.append(MessageDTO(content=row.answer_message, is_user=False))

        if len(flattened) > limit:
            flattened = flattened[-limit:]
        return flattened
