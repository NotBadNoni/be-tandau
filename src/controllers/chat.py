from __future__ import annotations

from typing import List

from src.core.databases import UoW
from src.core.exeptions import NotFoundException
from src.repositories.chat import ChatRepository, ChatMessageRepository
from src.repositories.university import UniversityRepository
from src.services.openai_cli import OpenAIClient


class ChatController:
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
        universities = await self.university_repo.list_universities()

        uni_summary = self._build_university_summary(universities[:5])

        history = await self.message_repo.get_last_messages(chat_id, limit=10)
        messages: List[dict] = [
            {
                "role": "system",
                "content": (
                    "You are a friendly and knowledgeable educational assistant designed to help students "
                    "choose the most suitable university based on their preferences, such as country, program, "
                    "and available scholarships.\n\n"
                    "The list of universities provided to you is sourced from the official educational platform "
                    "'https://univision.kz', which includes verified institutions with relevant data on scholarships and programs.\n\n"
                    f"Here is a summary of the top {len(universities[:5])} universities:\n"
                    f"{uni_summary}\n\n"
                    "When replying to students, always detect the language of the user's message and respond in the same language. "
                    "Be concise, helpful, and polite. If you need more details from the student, ask follow-up questions."
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
