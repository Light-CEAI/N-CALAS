import sqlite3
from pathlib import Path
from datetime import datetime, timezone


DB_PATH = Path("data/activity.sqlite")


def log_event(event: str, detail: str = "") -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS activity (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            event TEXT NOT NULL,
            detail TEXT NOT NULL
        )""")
        con.execute("INSERT INTO activity(timestamp, event, detail) VALUES (?, ?, ?)",
                    (datetime.now(timezone.utc).isoformat(), event, detail[:240]))
