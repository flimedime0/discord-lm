# File purpose: Manage SQLite DB for user preferences.
import json
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
        return {}
    conn = sqlite3.connect(DB_PATH)
    row = conn.execute(
        "SELECT active_model, params_json FROM user_preferences WHERE user_id = ?",
        (user_id,),
    ).fetchone()
    conn.close()
    if not row:
        return {}
    active_model, params_json = row
    params = json.loads(params_json) if params_json else {}
    return {"active_model": active_model, "params": params}


def set_user_setting(user_id: int, key: str, value) -> None:
    setup_database()
    conn = sqlite3.connect(DB_PATH)
    with conn:
        row = conn.execute(
            "SELECT active_model, params_json FROM user_preferences WHERE user_id = ?",
            (user_id,),
        ).fetchone()
        active_model = row[0] if row else None
        params = json.loads(row[1]) if row and row[1] else {}
        if key == "active_model":
            active_model = str(value)
        else:
            params[key] = value
        conn.execute(
            "REPLACE INTO user_preferences (user_id, active_model, params_json) VALUES (?, ?, ?)",
            (user_id, active_model, json.dumps(params)),
        )
    conn.close()
