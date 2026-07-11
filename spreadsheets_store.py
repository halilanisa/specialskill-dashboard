from supabase_client import get_client

TABLE_NAME = "spreadsheets"

DEFAULT_SPREADSHEETS = {
    "Master Data (Free Event)": (
        "https://docs.google.com/spreadsheets/d/"
        "14dyD16lRgLZxBLAHiE5BLXN2XAyJyWDAK59KTfbnBaM/"
        "export?format=csv&gid=854838440"
    ),
}


def load_spreadsheets():
    """Ambil semua spreadsheet tersimpan, urut sesuai kapan ditambahkan."""

    client = get_client()

    response = (
        client.table(TABLE_NAME)
        .select("name, url")
        .order("id", desc=False)
        .execute()
    )

    rows = response.data

    if not rows:
        # Tabel masih kosong (baru pertama kali dipakai) -> isi data default.
        for name, url in DEFAULT_SPREADSHEETS.items():
            add_spreadsheet(name, url)
        return dict(DEFAULT_SPREADSHEETS)

    return {row["name"]: row["url"] for row in rows}


def add_spreadsheet(name, url):
    """Tambah/replace satu spreadsheet. Nama dipakai sebagai kunci unik."""

    client = get_client()

    client.table(TABLE_NAME).upsert(
        {"name": name, "url": url},
        on_conflict="name",
    ).execute()


def delete_spreadsheet(name):
    client = get_client()
    client.table(TABLE_NAME).delete().eq("name", name).execute()
