import os
import json
import re
import httpx
from typing import List, Dict, Any

DO_INFERENCE_URL = "https://inference.do-ai.run/v1/chat/completions"
DO_API_KEY = os.getenv("DIGITALOCEAN_INFERENCE_KEY")
DEFAULT_MODEL = os.getenv("DO_INFERENCE_MODEL", "openai-gpt-oss-120b")

def _extract_json(text: str) -> str:
    m = re.search(r"```(?:json)?\s*\n?([\s\S]*?)\n?\s*```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    m = re.search(r"(\{.*\}|\[.*\])", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()

def _coerce_unstructured_payload(raw_text: str) -> Dict[str, Any]:
    compact = raw_text.strip()
    tags = [part.strip(" -•\t") for part in re.split(r",|\\n", compact) if part.strip(" -•\t")]
    return {
        "note": "Model returned plain text instead of JSON",
        "raw": compact,
        "text": compact,
        "summary": compact,
        "tags": tags[:6],
    }


async def _call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    headers = {
        "Authorization": f"Bearer {DO_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_completion_tokens": max_tokens,
    }
    async with httpx.AsyncClient(timeout=90.0) as client:
        try:
            resp = await client.post(DO_INFERENCE_URL, headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            # Expected OpenAI‑like response structure
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            json_str = _extract_json(content)
            return json.loads(json_str)
        except Exception as e:
            # Fallback response guaranteeing JSON serializability
            return {"note": f"AI service unavailable: {str(e)}"}

# Public helper used by route handlers
async def call_inference(messages: List[Dict[str, str]], max_tokens: int = 512) -> Dict[str, Any]:
    return await _call_inference(messages, max_tokens)
