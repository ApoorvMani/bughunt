from datetime import datetime

def time_now(args: dict) -> str:
    return datetime.now().isoformat()