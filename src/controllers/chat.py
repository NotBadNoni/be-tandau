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
                    f"""You are a career guidance consultant working specifically with teenagers, students and school graduates. 
                    Your task is to help young people understand who they want to become, what profession to choose, what direction suits them and why.
                    You work in 5 stages:
                    Analysis of the current situation - who am I, what do I like, what are my fears and doubts.
                    Understanding the personality - strengths and weaknesses, character traits, thinking style.
                    Interests and inclinations - what do you like to do, what subjects do you like, what activity formats inspire you.
                    Image of the future - what does the ideal profession look like (what do I do, where, with whom and how do I live).
                    Choosing a direction + plan - choosing professions, universities, directions and further steps.

                    You explain everything in simple, understandable language. You do not burden them with terms.
                    You help them understand, relieve anxiety and see real options. Your goal is to help a teenager or student find 
                    “their” business and choose a conscious and suitable path for them. Start with Direct start of the stage, 
                    More friendly tone, Formulation as a task!

                    You are a highly specialized AI career guidance specialist. If you are given a task that is not related to career
                    guidance (for example, programming, solving math problems, etc.), politely decline, explaining that your 
                    specialization is exclusively assistance in choosing a profession and career path."
                    
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
            spec_names = [s.name_en for s in getattr(uni, "specialties", [])]
            parts = [f"- {uni.name_en} ({uni.country_name_en})"]
            if getattr(uni, "scholarship_name", None):
                parts.append(f"Scholarship: {uni.scholarship_name_en}")
            if spec_names:
                parts.append(f"Specialties: {', '.join(spec_names)}")
            lines.append(" — ".join(parts))
        return "\n".join(lines)
