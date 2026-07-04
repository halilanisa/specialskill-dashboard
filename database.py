import sqlite3
import pandas as pd
from datetime import datetime
import io

DB_NAME = "history.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            event_name TEXT,
            file_name TEXT,
            periode TEXT,
            target INTEGER,
            total_pendaftar INTEGER,
            created_at TEXT,
            data_json TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_dashboard(
    event_name,
    file_name,
    periode,
    target,
    df
):
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO dashboard_history(
            event_name,
            file_name,
            periode,
            target,
            total_pendaftar,
            created_at,
            data_json
        )
        VALUES(?,?,?,?,?,?,?)
    """, (
        event_name,
        file_name,
        periode,
        target,
        len(df),
        datetime.now().strftime("%d %b %Y %H:%M"),
        df.to_json(orient="records")
    ))

    conn.commit()
    conn.close()


def get_history():
    init_db()

    conn = get_connection()

    df = pd.read_sql("""
        SELECT *
        FROM dashboard_history
        ORDER BY id DESC
    """, conn)

    conn.close()

    return df


def load_dashboard(history_id):
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM dashboard_history
        WHERE id=?
    """, (history_id,))

    row = cursor.fetchone()

    conn.close()

    if row is None:
        return None

    return {
        "id": row[0],
        "event_name": row[1],
        "file_name": row[2],
        "periode": row[3],
        "target": row[4],
        "total_pendaftar": row[5],
        "created_at": row[6],
        "data": pd.read_json(io.StringIO(row[7]))
    }


def delete_dashboard(history_id):
    init_db()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM dashboard_history
        WHERE id=?
    """, (history_id,))

    conn.commit()
    conn.close()