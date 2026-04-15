import os
from dotenv import load_dotenv
from src.bughunt.llm.ollama_client import OllamaClient

load_dotenv()

client = OllamaClient(
    base_url=os.getenv("OLLAMA_URL"),
    model=os.getenv("OLLAMA_MODEL")
)

response = client.chat([
    {"role": "user", "content": "Say hello in one sentence."}
])

print(response)

print("\n--- streaming ---")
for token in client.stream([
    {"role": "user", "content": "Count from 1 to 5, one number per line."}
]):
    print(token, end="", flush=True)
print()
