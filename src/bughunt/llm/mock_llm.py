import hashlib
from typing import Iterator


class MockLLM:

    def __init__(self, responses: dict[str, str] | None = None):
        self.responses = responses or {}
        self.call_log = []

    def _hash(self, messages: list[dict]) -> str:
        content = "".join(m["content"] for m in messages)
        return hashlib.md5(content.encode()).hexdigest()

    def _lookup(self, messages: list[dict]) -> str:
        key = self._hash(messages)
        if key in self.responses:
            return self.responses[key]
        last = messages[-1]["content"]
        for pattern, reply in self.responses.items():
            if pattern.lower() in last.lower():
                return reply
        return f"[MockLLM] no canned response for: {last[:60]}"

    def chat(self, messages: list[dict]) -> str:
        response = self._lookup(messages)
        self.call_log.append({"messages": messages, "response": response})
        return response

    def stream(self, messages: list[dict]) -> Iterator[str]:
        response = self._lookup(messages)
        self.call_log.append({"messages": messages, "response": response})
        for word in response.split(" "):
            yield word + " "
