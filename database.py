"""SQLite helper functions for users and attendance."""
import sqlite3
from datetime import datetime

import numpy as np

DB_NAME = "attendance.db"


def get_conn():
    return sqlite3.connect(DB_NAME)


def init_db():
    with get_conn() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll_no TEXT NOT NULL UNIQUE,
                encoding BLOB NOT NULL
            )"""
        )
        conn.execute(
            """CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                UNIQUE(user_id, date),
                FOREIGN KEY (user_id) REFERENCES users(id)
            )"""
        )


def add_user(name, roll_no, encoding):
    """Save a user. Returns False if roll_no already exists."""
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO users (name, roll_no, encoding) VALUES (?, ?, ?)",
                (name, roll_no, np.asarray(encoding, dtype=np.float64).tobytes()),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_all_users():
    """Returns list of (id, name, roll_no, encoding_array)."""
    with get_conn() as conn:
        rows = conn.execute("SELECT id, name, roll_no, encoding FROM users").fetchall()
    return [(r[0], r[1], r[2], np.frombuffer(r[3], dtype=np.float64)) for r in rows]


def get_users_list():
    with get_conn() as conn:
        return conn.execute("SELECT id, name, roll_no FROM users ORDER BY name").fetchall()


def mark_attendance(user_id):
    """Mark attendance once per day. Returns True if newly marked, False if duplicate."""
    now = datetime.now()
    try:
        with get_conn() as conn:
            conn.execute(
                "INSERT INTO attendance (user_id, date, time) VALUES (?, ?, ?)",
                (user_id, now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")),
            )
        return True
    except sqlite3.IntegrityError:
        return False


def get_attendance_records(date=None, roll_no=None):
    """Returns list of (name, roll_no, date, time), optionally filtered."""
    query = """SELECT u.name, u.roll_no, a.date, a.time
               FROM attendance a JOIN users u ON u.id = a.user_id WHERE 1=1"""
    params = []
    if date:
        query += " AND a.date = ?"
        params.append(date)
    if roll_no:
        query += " AND u.roll_no = ?"
        params.append(roll_no)
    query += " ORDER BY a.date DESC, a.time DESC"
    with get_conn() as conn:
        return conn.execute(query, params).fetchall()


init_db()
