# app/utils/llm_client.py

import os
import httpx

class GroqClient:
    def __init__(self):
        self.api_key = "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"
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-70b-8192"

    async def ask(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a helpful AI assistant."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

groq = GroqClient()
