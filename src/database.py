import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "mailing_list.db"


def get_db_path():
    DATA_DIR.mkdir(exist_ok=True)
    return str(DB_PATH)


def get_connection():
    conn = sqlite3.connect(get_db_path())
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()
    return get_db_path()


def add_subscriber(email):
    init_db()
    normalized_email = (email or "").strip().lower()

    if not normalized_email:
        raise ValueError("Email is required.")

    conn = get_connection()
    try:
        conn.execute(
            "INSERT OR IGNORE INTO subscribers (email, created_at) VALUES (?, ?)",
            (normalized_email, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
    finally:
        conn.close()

    return normalized_email


def get_subscribers():
    init_db()
    conn = get_connection()
    try:
        rows = conn.execute("SELECT email FROM subscribers ORDER BY id").fetchall()
    finally:
        conn.close()

    return [row["email"] for row in rows]


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "add" and len(sys.argv) > 2:
        add_subscriber(sys.argv[2])
        print("saved")
    elif command == "list":
        for email in get_subscribers():
            print(email)
    else:
        print("Usage: python src/database.py add <email> | python src/database.py list")
