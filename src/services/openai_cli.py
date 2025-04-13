from openai import AsyncOpenAI


class OpenAIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = AsyncOpenAI(api_key=self.api_key)

    async def get_chat_response(self, prompt: str) -> str:
        """
        Sends a prompt to OpenAI and returns the assistant's reply.
        """
        try:
            response = await self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=800,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}")
            return "Sorry, something went wrong while generating a response."
