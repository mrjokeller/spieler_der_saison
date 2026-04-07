import sqlite3
from typing import List, Dict, Any


def execute_query(db_path: str, query: str) -> List[Dict[str, Any]]:
    """Excecutes a SQL-query and returns the result as a list of dictionaries."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query)
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result
