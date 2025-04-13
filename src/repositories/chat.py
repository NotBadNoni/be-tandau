from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from src.models.chat import Chat
from src.models.chat_messages import ChatMessages


class ChatRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_chat(self, user_id: int, chat_name: str) -> Chat:
        stmt = insert(Chat).values(user_id=user_id, chat_name=chat_name).returning(Chat)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def get_chat_with_messages(self, chat_id: int):
        stmt = (
            select(Chat)
            .options(selectinload(Chat.messages))
            .where(Chat.id == chat_id)
        )
        result = await self._session.execute(stmt)
        return result.unique().scalar_one_or_none()


class ChatMessageRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_message(self, chat_id: int, user_message: str, answer_message: str) -> ChatMessages:
        stmt = insert(ChatMessages).values(
            id=len(await self.list_chat_messages(chat_id)) + 1,
            chat_id=chat_id,
            user_message=user_message,
            answer_message=answer_message
        ).returning(ChatMessages)
        res = await self._session.execute(stmt)
        return res.scalar()

    async def list_chat_messages(self, chat_id: int) -> list[ChatMessages]:
        stmt = select(ChatMessages).where(ChatMessages.chat_id == chat_id).order_by(ChatMessages.created_at.asc())
        res = await self._session.execute(stmt)
        return res.scalars().all()
