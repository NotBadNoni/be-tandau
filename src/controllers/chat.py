from __future__ import annotations

from typing import List, Optional

from src.core.databases import UoW
from src.core.exeptions import NotFoundException
from src.repositories.chat import ChatRepository, ChatMessageRepository
from src.repositories.university import UniversityRepository
from src.services.openai_cli import OpenAIClient


class ChatController:
    _COUNTRY_KEYWORDS = {
        "uk": "United Kingdom",
        "united kingdom": "United Kingdom",
        "usa": "USA",
        "canada": "Canada",
        "kazakhstan": "Kazakhstan",
        "europe": "Europe",
    }

    def __init__(
            self,
            uow: UoW,
            chat_repo: ChatRepository,
            message_repo: ChatMessageRepository,
            openai_client: OpenAIClient,
            university_repo: UniversityRepository,
    ) -> None:
        self.uow = uow
        self.chat_repo = chat_repo
        self.message_repo = message_repo
        self.openai = openai_client
        self.university_repo = university_repo

    async def create_chat(self, user_id: int, chat_name: str):
        async with self.uow:
            return await self.chat_repo.create_chat(user_id, chat_name)

    async def get_chat(self, chat_id: int):
        chat = await self.chat_repo.get_chat_with_messages(chat_id)
        if chat is None:
            raise NotFoundException("Chat not found")
        return chat

    async def get_chats(self, user_id: int):
        return await self.chat_repo.get_chats(user_id)

    async def send_message(self, chat_id: int, user_message: str):
        country_name = self._extract_country_name(user_message)
        if country_name:
            universities = await self.university_repo.get_universities_by_country(country_name)
        else:
            universities = await self.university_repo.list_universities()

        uni_summary = self._build_university_summary(universities[:5])

        history = await self.message_repo.get_last_messages(chat_id, limit=10)
        messages: List[dict] = [
            {
                "role": "system",
                "content": (
                    "You are an educational assistant that helps students select "
                    "universities tailored to their interests and preferred country."
                    f"\n\nCurrent university context (top {len(universities[:5])}):\n{uni_summary}"
                ),
            }
        ]
        for msg in history:
            role = "user" if msg.is_user else "assistant"
            messages.append({"role": role, "content": msg.content})
        messages.append({"role": "user", "content": user_message})
        ai_answer = (await self.openai.get_chat_response(messages)).strip()
        async with self.uow:
            await self.message_repo.add_message(chat_id, user_message, ai_answer)
        return {"ai_answer": ai_answer}

    @classmethod
    def _extract_country_name(cls, text: str) -> Optional[str]:
        lowered = text.lower()
        for kw, canonical in cls._COUNTRY_KEYWORDS.items():
            if kw in lowered:
                return canonical
        return None

    @staticmethod
    def _build_university_summary(universities: List) -> str:
        if not universities:
            return "*There are no universities available for the user query.*"

        lines: List[str] = []
        for uni in universities:
            spec_names = [s.name for s in getattr(uni, "specialties", [])]
            parts = [f"- {uni.name} ({uni.country_name})"]
            if getattr(uni, "scholarship_name", None):
                parts.append(f"Scholarship: {uni.scholarship_name}")
            if spec_names:
                parts.append(f"Specialties: {', '.join(spec_names)}")
            lines.append(" — ".join(parts))
        return "\n".join(lines)
