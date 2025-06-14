# File purpose: Manage SQLite DB for user preferences (active model only).
import sqlite3
from pathlib import Path

DB_PATH = Path("data/bot_memory.sqlite3")


def setup_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    with conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS user_preferences (user_id INTEGER PRIMARY KEY, active_model TEXT, params_json TEXT)"
        )
    conn.close()


def get_user_settings(user_id: int) -> dict:
    if not DB_PATH.exists():
        return {"active_model": "o3"}
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT active_model FROM user_preferences WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    active_model = row[0] if row else None
    return {"active_model": active_model or "o3"}


def set_user_setting(user_id: int, key: str, value) -> None:
    setup_database()
    conn = sqlite3.connect(DB_PATH)
    with conn:
        row = conn.execute(
            "SELECT active_model FROM user_preferences WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        active_model = row[0] if row else None
        if key == "active_model":
            active_model = str(value)
        conn.execute(
            "REPLACE INTO user_preferences (user_id, active_model, params_json) VALUES (?, ?, NULL)",
            (user_id, active_model),
        )
    conn.close()
