import os
import httpx

class GroqClient:
    def __init__(self):
        self.api_key = os.getenv(
            "GROQ_API_KEY",
            "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"
        )
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.model = "llama3-70b-8192"

    async def ask(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        system_prompt = (
            "You are a precise and helpful assistant for answering insurance policy questions. "
            "Use only the provided context to answer the question. "
            "Respond with a single, concise, and factual sentence. "
            "If the question is strictly yes/no, start with 'Yes,' or 'No,' followed by a brief concise short reason. "
            "Otherwise, respond directly without using yes/no language."
            "Strictly and very strictly small and consice setences, no long explanations. "
        )

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.1,
            "top_p": 1.0,
            "max_tokens": 512
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"].strip()

groq = GroqClient()
