import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Generator, Iterator

from config import DB_PATH


def _dict_factory(cursor: sqlite3.Cursor, row: tuple) -> dict[str, Any]:
    """Wandelt sqlite3-Rows direkt in dicts um (praktischer als sqlite3.Row für JSON-Export)."""
    fields = [col[0] for col in cursor.description]
    return dict(zip(fields, row))


@contextmanager
def get_connection(
    db_path: Path = DB_PATH,
) -> Generator[sqlite3.Connection, None, None]:
    """Context-Manager für eine DB-Connection mit dict-Rows und FK-Constraints."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = _dict_factory
    conn.execute("PRAGMA foreign_keys = ON")
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(
    query: str, params: tuple = (), db_path: Path = DB_PATH
) -> list[dict[str, Any]]:
    """Führt eine SELECT-Query aus und gibt alle Ergebnisse als Liste von dicts zurück."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(query, params)
        return cursor.fetchall()


def fetch_one(
    query: str, params: tuple = (), db_path: Path = DB_PATH
) -> dict[str, Any] | None:
    """Führt eine SELECT-Query aus und gibt die erste Zeile als dict zurück (oder None)."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(query, params)
        return cursor.fetchone()


def execute_write(query: str, params: tuple = (), db_path: Path = DB_PATH) -> int | None:
    """Führt INSERT/UPDATE/DELETE aus, committed automatisch. Gibt lastrowid zurück."""
    with get_connection(db_path) as conn:
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor.lastrowid


def execute_many(query: str, params_list: list[tuple], db_path: Path = DB_PATH) -> None:
    """Für Bulk-Inserts/Updates."""
    with get_connection(db_path) as conn:
        conn.executemany(query, params_list)
        conn.commit()
