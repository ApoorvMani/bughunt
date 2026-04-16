import sqlite3
import os
from datetime import datetime


SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT NOT NULL,
    target      TEXT NOT NULL,
    created_at  TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS llm_calls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,
    messages    TEXT NOT NULL,
    response    TEXT NOT NULL,
    model       TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS tool_calls (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,
    tool_name   TEXT NOT NULL,
    arguments   TEXT NOT NULL,
    result      TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS findings (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,
    title       TEXT NOT NULL,
    severity    TEXT NOT NULL,
    description TEXT NOT NULL,
    poc         TEXT,
    status      TEXT NOT NULL DEFAULT 'suspected',
    created_at  TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);

CREATE TABLE IF NOT EXISTS approvals (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id  INTEGER NOT NULL,
    tool_name   TEXT NOT NULL,
    arguments   TEXT NOT NULL,
    approved    INTEGER NOT NULL,
    approved_by TEXT NOT NULL,
    created_at  TEXT NOT NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(id)
);
"""


def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA)
    conn.commit()
    return conn


def now() -> str:
    return datetime.utcnow().isoformat()


def insert_session(conn: sqlite3.Connection, name: str, target: str) -> int:
    cursor = conn.execute(
        "INSERT INTO sessions (name, target, created_at) VALUES (?, ?, ?)",
        (name, target, now())
    )
    conn.commit()
    return cursor.lastrowid


def insert_llm_call(conn: sqlite3.Connection, session_id: int,
                    messages: str, response: str, model: str) -> int:
    cursor = conn.execute(
        "INSERT INTO llm_calls (session_id, messages, response, model, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (session_id, messages, response, model, now())
    )
    conn.commit()
    return cursor.lastrowid


def insert_tool_call(conn: sqlite3.Connection, session_id: int,
                     tool_name: str, arguments: str, result: str) -> int:
    cursor = conn.execute(
        "INSERT INTO tool_calls (session_id, tool_name, arguments, result, created_at) "
        "VALUES (?, ?, ?, ?, ?)",
        (session_id, tool_name, arguments, result, now())
    )
    conn.commit()
    return cursor.lastrowid


def insert_finding(conn: sqlite3.Connection, session_id: int, title: str,
                   severity: str, description: str, poc: str = None) -> int:
    cursor = conn.execute(
        "INSERT INTO findings (session_id, title, severity, description, poc, created_at) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (session_id, title, severity, description, poc, now())
    )
    conn.commit()
    return cursor.lastrowid
