from supabase_client import get_client

TABLE_NAME = "spreadsheets"

DEFAULT_SPREADSHEETS = {
    "Master Data (Free Event)": {
        "url": (
            "https://docs.google.com/spreadsheets/d/"
            "14dyD16lRgLZxBLAHiE5BLXN2XAyJyWDAK59KTfbnBaM/"
            "export?format=csv&gid=854838440"
        ),
        "dashboard_title": "Master Data (Free Event)",
    },
}


def load_spreadsheets():
    client = get_client()

    response = (
        client.table(TABLE_NAME)
        .select("name, url, dashboard_title")
        .order("id", desc=False)
        .execute()
    )

    rows = response.data

    if not rows:
        for name, info in DEFAULT_SPREADSHEETS.items():
            add_spreadsheet(
                name,
                info["dashboard_title"],
                info["url"]
            )

        return dict(DEFAULT_SPREADSHEETS)

    return {
        row["name"]: {
            "url": row["url"],
            "dashboard_title": row["dashboard_title"],
        }
        for row in rows
    }

def add_spreadsheet(name, dashboard_title, url):
    """Tambah/replace satu spreadsheet. Nama dipakai sebagai kunci unik."""

    client = get_client()

    client.table(TABLE_NAME).upsert(
        {
            "name": name,
            "dashboard_title": dashboard_title,
            "url": url,
        },
        on_conflict="name",
    ).execute()


def delete_spreadsheet(name):
    client = get_client()
    client.table(TABLE_NAME).delete().eq("name", name).execute()
