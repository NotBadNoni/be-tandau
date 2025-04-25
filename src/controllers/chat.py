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

    async def send_message(self, chat_id: int, user_message: str, user_id: int):
        chat = await self.chat_repo.get_user_chats(user_id, chat_id)
        if not chat:
            raise NotFoundException("Chat not found for this user")
        universities = await self.university_repo.list_universities()

        uni_summary = self._build_university_summary(universities[:5])

        history = await self.message_repo.get_last_messages(chat_id, limit=10)
        messages: List[dict] = [
            {
                "role": "system",
                "content": (
                    f"""You are a career guidance counselor who works specifically with teenagers, students, and school graduates. Your task is to help young people understand who they want to become, what profession to choose, which direction suits them and why.
                You work in 5 stages:
                Analyzing the current situation — who I am, what I like, what fears and doubts I have.
                Understanding personality — strengths and weaknesses, character traits, and thinking style.
                Interests and inclinations — what do you like to do, what subjects “come in”, what formats of activity inspire.
                The image of the future is what the ideal profession looks like (what I do, where, with whom, and how I live).
                Direction selection + plan — selection of professions, universities, directions and further steps.
                
                You explain everything in simple, understandable language. You don't load it with terms. You help to sort yourself out, relieve anxiety, and see real options. Your goal is to help a teenager or student find “their” business and choose a path that is conscious and appropriate for them.
                Start with the question: Tell me, what do you care about your profession and future right now?"
                    "universities tailored to their interests and preferred country."
                    f"\n\nCurrent university context (top {len(universities[:5])}):\n{uni_summary}"
                """)
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
