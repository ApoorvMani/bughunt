from dataclasses import dataclass, field
from typing import Literal
import tiktoken

@dataclass
class Message:
    role: Literal["system", "user", "assistant", "tool_call", "tool_result"]
    content: str

class ConversationHistory:
    def __init__(self, model: str = "gpt-4o"):
        self.messages: list[Message] = []
        self.model = model
        self.encoder = tiktoken.encoding_for_model("gpt-4o")

    def add(self, role: Literal["system", "user", "assistant", "tool_call", "tool_result"], content: str) -> None:      # create a new dataclass
        self.messages.append(Message(role=role, content=content))

    # count tokens
    def count_tokens(self) -> int:
        total = 0
        for message in self.messages:
            total += len(self.encoder.encode(message.content))
        return total

    # convert each msg dataclass into py dict. which format ollama expects
    def to_prompt(self) -> list[dict]:
        return [
            {"role": message.role, "content": message.content}
            for message in self.messages
        ]