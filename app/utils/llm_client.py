# app/utils/llm_client.py

import google.generativeai as genai
from app.utils.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

class GeminiClient:
    def __init__(self):
        self.model = genai.GenerativeModel("models/gemini-1.5-flash")

    async def ask(self, prompt: str) -> str:
        response = await self.model.generate_content_async(prompt)
        return response.text

gemini = GeminiClient()
