from bughunt.tools.time_now import time_now

REGISTRY: dict[str, dict] = {
    "time_now": {
        "fn": time_now,
        "description": "Returns the current date and time. Use when the user asks what time or date it is.",
        "args": {},
    },
}

def call_tool(name: str, args: dict) -> str:
    if name not in REGISTRY:
        return f"Error: unknown tool '{name}'"
    return REGISTRY[name]["fn"](args)

def list_tools() -> str:
    lines = []
    for name, meta in REGISTRY.items():
        lines.append(f"- {name}: {meta['description']}")
    return "\n".join(lines)