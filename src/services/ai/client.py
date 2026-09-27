import json
import httpx
from fastapi import HTTPException, status
from services.utils import get_client
from config import GEMINI_API_KEY

GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/openai/chat/completions"

class AIService:

    @staticmethod
    async def call_gemini(system_prompt: str, user_input: str) -> dict:
        if not GEMINI_API_KEY:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="GEMINI_API_KEY не установлен в конфигурации"
            )

        HEADERS = {
            "Authorization": f"Bearer {GEMINI_API_KEY}",
            "Content-Type": "application/json"
        }
        
        body = {
            "model": "gemini-3.6-flash",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            "response_format": {"type": "json_object"},
        }

        client = await get_client(name='gemini_call')
        try:
            response = await client.post(GEMINI_URL, headers=HEADERS, json=body)
            response.raise_for_status()
            
            res_data = response.json()
            # print(res_data)
            content = res_data["choices"][0]["message"]["content"]
            return json.loads(content)
            
        except httpx.TimeoutException:
            raise HTTPException(status.HTTP_504_GATEWAY_TIMEOUT, detail="AI не ответил вовремя")
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status.HTTP_502_BAD_GATEWAY, 
                detail=f"Ошибка AI API ({e.response.status_code}): {e.response.text}"
            )