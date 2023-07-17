import sqlite3
from pathlib import Path
from typing import List, Tuple

from app.app_context import todo_store

DB_PATH = Path("rocket.db")


def _get_connection() -> sqlite3.Connection:
    """
    Opens the database.
    SQLite automatically creates the file if it does not exist.
    """
    return sqlite3.connect(DB_PATH)


def _init_schema(conn: sqlite3.Connection) -> None:
    """
    Creates required tables if they do not exist.
    Safe to call multiple times.
    """
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL UNIQUE,
            status INTEGER NOT NULL
        )
    """)
    conn.commit()


def _ensure_db() -> sqlite3.Connection:
    """
    Ensures the database file and schema exist.
    Returns a ready-to-use connection.
    """
    conn = _get_connection()
    _init_schema(conn)
    return conn


# ============================================================
# Public API (USED BY UI)
# ============================================================


def add_task(task_text: str) -> None:
    """
    Adds a new task.
    Creates DB and tables automatically if needed.
    """
    if not task_text:
        return

    with _ensure_db() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO tasks (task, status) VALUES (?, ?)",
            (task_text, 0),
        )
        conn.commit()

    todo_store.notify()


def delete_task(task_text: str) -> None:
    """
    Deletes a task.
    """
    with _ensure_db() as conn:
        conn.execute(
            "DELETE FROM tasks WHERE task = ?",
            (task_text,),
        )
        conn.commit()

    todo_store.notify()


def update_task_status(task_text: str, status: bool) -> None:
    """
    Updates task completion status.
    """
    with _ensure_db() as conn:
        conn.execute(
            "UPDATE tasks SET status = ? WHERE task = ?",
            (1 if status else 0, task_text),
        )
        conn.commit()

    todo_store.notify()


def get_all_tasks() -> List[Tuple[str, bool]]:
    """
    Returns all tasks.
    """
    with _ensure_db() as conn:
        cursor = conn.execute("SELECT task, status FROM tasks ORDER BY id ASC")

        data = [(task, bool(status)) for task, status in cursor.fetchall()]
        return data
