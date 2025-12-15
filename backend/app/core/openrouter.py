import asyncio
import json
from typing import Any, Dict, List, Optional

import httpx

from .config import settings


async def chat_completion(model: str, messages: List[Dict[str, str]], temperature: float = 0.6, max_tokens: int = 1200) -> Dict[str, Any]:
    if not settings.openrouter_api_key:
        return _fake_response(messages)

    headers = {
        "Authorization": f"Bearer {settings.openrouter_api_key}",
        "HTTP-Referer": settings.openrouter_referer,
        "X-Title": settings.openrouter_title,
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(settings.openrouter_endpoint, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()


def _fake_response(messages: List[Dict[str, str]]) -> Dict[str, Any]:
    content = messages[-1].get("content", "")
    pseudo = {
        "summary": content[:120],
        "notes": ["OpenRouter API key missing; returning placeholder."],
    }
    return {
        "choices": [
            {
                "message": {"role": "assistant", "content": json.dumps(pseudo)},
            }
        ],
        "usage": None,
    }


async def safe_chat_completion(*args: Any, **kwargs: Any) -> Dict[str, Any]:
    try:
        return await chat_completion(*args, **kwargs)
    except Exception as exc:  # noqa: BLE001
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": json.dumps({"error": str(exc)}),
                    }
                }
            ],
            "usage": None,
        }


async def run_parallel(requests: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    tasks = [safe_chat_completion(**req) for req in requests]
    return await asyncio.gather(*tasks)
