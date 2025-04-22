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
    ):
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
        if not chat:
            raise NotFoundException("Chat not found")
        return chat

    async def get_chats(self, user_id: int):
        chats = await self.chat_repo.get_chats(user_id)
        return chats

    async def send_message(self, chat_id: int, user_message: str):
        country_keywords = ["uk", "united kingdom", "usa", "canada", "kazakhstan", "europe"]
        country_name = None
        lowered = user_message.lower()
        for keyword in country_keywords:
            if keyword in lowered:
                country_name = keyword.title()
                break

        universities = await self.university_repo.get_universities_by_country(
            country_name) if country_name else await self.university_repo.list_universities()

        universities = universities[:5]

        prompt = self.format_prompt(user_message, universities)

        response = await self.openai.get_chat_response(prompt)
        answer = response.strip()

        async with self.uow:
            return await self.message_repo.add_message(chat_id, user_message, answer)

    def format_prompt(self, user_message: str, universities: list) -> str:
        """
        Format a readable GPT prompt using university + specialties.
        """
        if not universities:
            return f"""
The user asked: "{user_message}".
But no universities are available in the database for the specified country or condition.
"""

        lines = []
        for uni in universities:
            spec_names = [s.name for s in uni.specialties] if hasattr(uni, "specialties") else []
            specs_str = f" — Specialties: {', '.join(spec_names)}" if spec_names else ""
            scholarship = f" — Scholarship: {uni.scholarship_name}" if uni.scholarship_name else ""
            lines.append(f"- {uni.name} ({uni.country_name}){scholarship}{specs_str}")

        university_block = "\n".join(lines)

        return f"""
You are an educational assistant that helps students choose the best universities based on their interests and country.

User asked: "{user_message}"

Here are the top universities available in our database:
{university_block}

Based on this information, respond clearly and helpfully to the user's question.
"""
