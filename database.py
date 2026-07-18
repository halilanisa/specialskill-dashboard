import io
import pandas as pd
from datetime import datetime

from supabase_client import get_client
from spreadsheets_store import load_spreadsheets
from column_mapping import normalize_columns

TABLE_NAME = "dashboard_history"


def init_db():
    pass


def save_dashboard(event_name, file_name, periode, target, df):
    client = get_client()

    payload = {
        "event_name": event_name,
        "file_name": file_name,
        "periode": periode,
        "target": int(target),
        "total_pendaftar": len(df),
        "created_at": datetime.now().strftime("%d %b %Y %H:%M"),
        "data_json": df.to_json(orient="records"),
    }

    client.table(TABLE_NAME).insert(payload).execute()


def save_or_update_dashboard(event_name, file_name, periode, target, df):
    """Simpan dashboard baru, atau update dashboard yang sudah ada
    untuk kombinasi file_name + event_name yang sama (tidak duplikat)."""

    client = get_client()

    payload = {
        "event_name": event_name,
        "file_name": file_name,
        "periode": periode,
        "target": int(target),
        "total_pendaftar": len(df),
        "created_at": datetime.now().strftime("%d %b %Y %H:%M"),
        "data_json": df.to_json(orient="records"),
    }

    existing = (
        client.table(TABLE_NAME)
        .select("id")
        .eq("file_name", file_name)
        .eq("event_name", event_name)
        .limit(1)
        .execute()
    )

    rows = existing.data or []

    if rows:
        history_id = rows[0]["id"]
        client.table(TABLE_NAME).update(payload).eq("id", history_id).execute()
        return history_id

    result = client.table(TABLE_NAME).insert(payload).execute()

    if result.data:
        return result.data[0]["id"]

    return None


def get_history():
    client = get_client()

    response = (
        client.table(TABLE_NAME)
        .select(
            "id, event_name, file_name, periode, "
            "target, total_pendaftar, created_at"
        )
        .order("id", desc=True)
        .execute()
    )

    rows = response.data or []

    if not rows:
        return pd.DataFrame(rows)

    spreadsheets = load_spreadsheets()
    df_cache = {}

    for row in rows:
        file_name = row["file_name"]

        sheet = spreadsheets.get(file_name)

        if sheet is None:
            continue

        url = sheet["url"]

        if file_name not in df_cache:
            try:
                df_live = pd.read_csv(url)
                df_live = normalize_columns(df_live)
            except Exception:
                df_live = None

            df_cache[file_name] = df_live

        df_live = df_cache[file_name]

        if df_live is None:
            continue

        if "event_name" in df_live.columns:
            row["total_pendaftar"] = int(
                (df_live["event_name"] == row["event_name"]).sum()
            )
        else:
            row["total_pendaftar"] = len(df_live)

    return pd.DataFrame(rows)


def load_dashboard(history_id):
    client = get_client()

    response = (
        client.table(TABLE_NAME)
        .select("*")
        .eq("id", history_id)
        .maybe_single()
        .execute()
    )

    row = response.data if response else None

    if row is None:
        return None

    df = None

    spreadsheets = load_spreadsheets()

    sheet = spreadsheets.get(row["file_name"])

    if sheet is not None:
        try:
            url = sheet["url"]

            df_live = pd.read_csv(url)
            df_live = normalize_columns(df_live)

            if "event_name" in df_live.columns:
                df = df_live[
                    df_live["event_name"] == row["event_name"]
                ].copy()
            else:
                df = df_live.copy()

        except Exception:
            df = None

    if df is None:
        df = pd.read_json(io.StringIO(row["data_json"]))

    return {
        "id": row["id"],
        "event_name": row["event_name"],
        "file_name": row["file_name"],
        "periode": row["periode"],
        "target": row["target"],
        "total_pendaftar": len(df),
        "created_at": row["created_at"],
        "data": df,
    }

def delete_dashboard(history_id):
    client = get_client()

    client.table(TABLE_NAME).delete().eq("id", history_id).execute()