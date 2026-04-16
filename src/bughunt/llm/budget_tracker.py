import os
from datetime import date
from typing import Iterator


class BudgetTracker:

    def __init__(self, client, daily_limit: int = 100):
        self.client = client
        self.daily_limit = daily_limit
        self.usage: dict[str, int] = {}

    def _today(self) -> str:
        return str(date.today())

    def _count(self) -> int:
        return self.usage.get(self._today(), 0)

    def _increment(self):
        today = self._today()
        self.usage[today] = self._count() + 1

    def _check(self):
        count = self._count()
        pct = count / self.daily_limit
        if pct >= 1.0:
            raise RuntimeError(
                f"[budget] daily limit reached ({count}/{self.daily_limit}). "
                f"Set LLM_MODE=mock to continue without burning calls."
            )
        if pct >= 0.75:
            print(
                f"[budget] WARNING: {count}/{self.daily_limit} calls used today "
                f"({int(pct*100)}%)"
            )

    def chat(self, messages: list[dict]) -> str:
        self._check()
        self._increment()
        return self.client.chat(messages)

    def stream(self, messages: list[dict]) -> Iterator[str]:
        self._check()
        self._increment()
        return self.client.stream(messages)

    @property
    def calls_today(self) -> int:
        return self._count()
