from src.bughunt.llm.mock_llm import MockLLM
from src.bughunt.llm.budget_tracker import BudgetTracker

mock = MockLLM(responses={"hello": "Hey!"})
tracker = BudgetTracker(client=mock, daily_limit=3)

print(tracker.chat([{"role": "user", "content": "hello"}]))
print(f"calls today: {tracker.calls_today}")

print(tracker.chat([{"role": "user", "content": "hello"}]))
print(f"calls today: {tracker.calls_today}")

print(tracker.chat([{"role": "user", "content": "hello"}]))
print(f"calls today: {tracker.calls_today}")

print(tracker.chat([{"role": "user", "content": "hello"}]))
