"""
db_manager.py
--------------
Stores patient sessions and identified tinnitus frequencies in a
local SQLite database, so results can be reviewed or exported later.
"""

import sqlite3
from datetime import datetime


def init_db(db_path: str = "../data/sessions.db") -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS sessions (
            session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            estimated_frequency_hz REAL NOT NULL,
            steps_taken INTEGER,
            converged INTEGER,
            recorded_at TEXT NOT NULL,
            notes TEXT
        )
        """
    )
    conn.commit()
    return conn


def save_session(conn: sqlite3.Connection, patient_name: str, result: dict, notes: str = "") -> int:
    cursor = conn.execute(
        """
        INSERT INTO sessions (patient_name, estimated_frequency_hz, steps_taken, converged, recorded_at, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            patient_name,
            result["estimated_frequency_hz"],
            result["steps_taken"],
            1 if result["converged"] else 0,
            datetime.now().isoformat(timespec="seconds"),
            notes,
        ),
    )
    conn.commit()
    return cursor.lastrowid


def get_patient_history(conn: sqlite3.Connection, patient_name: str) -> list:
    cursor = conn.execute(
        "SELECT * FROM sessions WHERE patient_name = ? ORDER BY recorded_at DESC",
        (patient_name,),
    )
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_all_sessions(conn: sqlite3.Connection) -> list:
    cursor = conn.execute("SELECT * FROM sessions ORDER BY recorded_at DESC")
    columns = [d[0] for d in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
