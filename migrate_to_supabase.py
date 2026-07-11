import json
import os
import sqlite3

import streamlit as st
from supabase import create_client


def get_client_standalone():
    """
    Baca secrets.toml langsung (tanpa lewat st.cache_resource) karena
    script ini dijalankan lewat `python`, bukan `streamlit run`.
    """
    secrets_path = os.path.join(".streamlit", "secrets.toml")

    if not os.path.exists(secrets_path):
        raise SystemExit(
            "Tidak ketemu .streamlit/secrets.toml. "
            "Buat dulu file itu dan isi SUPABASE_URL & SUPABASE_KEY "
            "(lihat README_SUPABASE.md)."
        )

    try:
        import tomllib  # Python 3.11+
    except ImportError:
        import tomli as tomllib  # Python <3.11, perlu `pip install tomli`

    with open(secrets_path, "rb") as f:
        secrets = tomllib.load(f)

    return create_client(secrets["SUPABASE_URL"], secrets["SUPABASE_KEY"])


def migrate_spreadsheets(client):
    if not os.path.exists("spreadsheets.json"):
        print("spreadsheets.json tidak ditemukan, dilewati.")
        return

    with open("spreadsheets.json", "r") as f:
        data = json.load(f)

    if not data:
        print("spreadsheets.json kosong, dilewati.")
        return

    count = 0
    for name, url in data.items():
        client.table("spreadsheets").upsert(
            {"name": name, "url": url},
            on_conflict="name",
        ).execute()
        count += 1

    print(f"{count} spreadsheet berhasil dipindahkan ke Supabase.")


def migrate_history(client):
    if not os.path.exists("history.db"):
        print("history.db tidak ditemukan, dilewati.")
        return

    conn = sqlite3.connect("history.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT event_name, file_name, periode, target,
               total_pendaftar, created_at, data_json
        FROM dashboard_history
        ORDER BY id ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("history.db tidak ada isinya, dilewati.")
        return

    count = 0
    for row in rows:
        payload = {
            "event_name": row[0],
            "file_name": row[1],
            "periode": row[2],
            "target": row[3],
            "total_pendaftar": row[4],
            "created_at": row[5],
            "data_json": row[6],
        }
        client.table("dashboard_history").insert(payload).execute()
        count += 1

    print(f"{count} riwayat dashboard berhasil dipindahkan ke Supabase.")


if __name__ == "__main__":
    client = get_client_standalone()

    print("Memulai migrasi ke Supabase...\n")
    migrate_spreadsheets(client)
    migrate_history(client)
    print("\nSelesai. Cek hasilnya di Supabase > Table Editor.")
