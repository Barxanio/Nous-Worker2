import aiohttp

API_URL = "https://inference-api.nousresearch.com/v1/chat/completions"

class NousClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = aiohttp.ClientSession(headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    async def chat(self, messages: list, model: str = "DeepHermes-3-Mistral-24B-Preview", max_tokens: int = 256):
        payload = {
            "model": model,
            "messages": messages,
            "max_tokens": max_tokens
        }
        async with self.session.post(API_URL, json=payload) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def close(self):
        await self.session.close()