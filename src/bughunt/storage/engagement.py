import os
import json
from datetime import datetime
from src.bughunt.storage.db import get_connection


ENGAGEMENTS_DIR = "engagements"

SUBDIRS = ["logs", "scans", "evidence", "reports"]


def create_engagement(name: str, target: str) -> dict:
    base = os.path.join(ENGAGEMENTS_DIR, name)
    if os.path.exists(base):
        raise ValueError(f"Engagement '{name}' already exists.")
    os.makedirs(base)
    for subdir in SUBDIRS:
        os.makedirs(os.path.join(base, subdir))
    meta = {
        "name": name,
        "target": target,
        "created_at": datetime.utcnow().isoformat(),
    }
    with open(os.path.join(base, "meta.json"), "w") as f:
        json.dump(meta, f, indent=2)
    db_path = os.path.join(base, "bughunt.db")
    conn = get_connection(db_path)
    session_id = _insert_session(conn, name, target)
    conn.close()
    return {"meta": meta, "db_path": db_path, "session_id": session_id}


def load_engagement(name: str) -> dict:
    base = os.path.join(ENGAGEMENTS_DIR, name)
    if not os.path.exists(base):
        raise ValueError(f"Engagement '{name}' not found.")
    with open(os.path.join(base, "meta.json")) as f:
        meta = json.load(f)
    db_path = os.path.join(base, "bughunt.db")
    conn = get_connection(db_path)
    row = conn.execute(
        "SELECT id FROM sessions WHERE name = ?", (name,)
    ).fetchone()
    conn.close()
    return {"meta": meta, "db_path": db_path, "session_id": row["id"]}


def list_engagements() -> list[str]:
    if not os.path.exists(ENGAGEMENTS_DIR):
        return []
    return [
        d for d in os.listdir(ENGAGEMENTS_DIR)
        if os.path.isdir(os.path.join(ENGAGEMENTS_DIR, d))
    ]


def _insert_session(conn, name: str, target: str) -> int:
    from src.bughunt.storage.db import insert_session
    return insert_session(conn, name, target)
