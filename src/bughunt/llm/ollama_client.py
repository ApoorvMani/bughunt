import requests
import json
import time
from typing import Iterator

OLLAMA_DEFAULT_URL = "http://localhost:11434"


class OllamaClient:

    def __init__(self, base_url: str, model: str, timeout: int = 60):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    def chat(self, messages: list[dict]) -> str:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
        }
        for attempt in range(3):
            try:
                response = requests.post(url, json=payload, timeout=self.timeout)
                response.raise_for_status()
                return response.json()["message"]["content"]
            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError):
                if attempt == 2:
                    raise
                wait = 2 ** attempt
                print(f"[ollama] attempt {attempt + 1} failed, retrying in {wait}s...")
                time.sleep(wait)

    def stream(self, messages: list[dict]) -> Iterator[str]:
        url = f"{self.base_url}/api/chat"
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
        }
        with requests.post(url, json=payload, stream=True, timeout=self.timeout) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if not chunk.get("done"):
                        yield chunk["message"]["content"]