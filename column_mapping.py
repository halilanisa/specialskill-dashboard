import re
import pandas as pd


ALIASES = {
    "timestamp": [
        "timestamp",
        "transaction created at",
        "tanggal daftar",
        "tanggal",
    ],
    "email": [
        "email",
        "customer email",
    ],
    "nama": [
        "nama",
        "customer name",
    ],
    "provinsi": [
        "provinsi",
    ],
    "jenjang_pendidikan": [
        "jenjang_pendidikan",
        "jenjang pendidikan",
    ],
    "asal_instansi": [
        "asal_instansi",
        "asal sekolah/universitas/pekerjaan",
        "asal sekolah universitas pekerjaan",
    ],
    "no_wa": [
        "no_wa",
        "customer mobile",
        "no whatsapp",
        "nomor whatsapp",
    ],
    "akun_instagram": [
        "akun_instagram",
        "akun instagram",
    ],
    "is_follow_ig": [
        "is_follow_ig",
        "follow, like, dan tag 3 teman",
        "follow like dan tag 3 teman",
    ],
    "is_follow_tiktok": [
        "is_follow_tiktok",
    ],
    "is_like_and_share": [
        "is_like_and_share",
        "share pamflet kegiatan di media sosial",
    ],
    "is_ever_join_ss": [
        "is_ever_join_ss",
    ],
    "source_info": [
        "source_info",
        "sumber informasi",
    ],
    "id_event": [
        "id_event",
        "transaction id",
    ],
    "event_type": [
        "event_type",
        "tipe produk",
    ],
    "event_name": [
        "event_name",
        "nama produk",
    ],
}


def _clean(text):
    """Rapikan teks header supaya bisa dibandingkan (case/spasi-insensitive)."""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text


_LOOKUP = {}
for standard_name, alias_list in ALIASES.items():
    for alias in alias_list:
        _LOOKUP[_clean(alias)] = standard_name


def normalize_columns(df):
    df = df.copy()

    unnamed_cols = [c for c in df.columns if str(c).startswith("Unnamed:")]
    for c in unnamed_cols:
        if df[c].isna().all():
            df = df.drop(columns=[c])

    rename_map = {}
    standard_sources = {}  

    for col in df.columns:
        standard_name = _LOOKUP.get(_clean(col))
        if standard_name:
            standard_sources.setdefault(standard_name, []).append(col)

    for standard_name, cols in standard_sources.items():
        if standard_name in df.columns and standard_name not in cols:
            continue

        best_col = max(cols, key=lambda c: df[c].notna().sum())
        rename_map[best_col] = standard_name

    df = df.rename(columns=rename_map)

    if df.columns.duplicated().any():
        deduped = {}
        for col in df.columns:
            if col in deduped:
                continue
            same_name_cols = df.loc[:, df.columns == col]
            if same_name_cols.shape[1] > 1:
                merged = same_name_cols.bfill(axis=1).iloc[:, 0]
                deduped[col] = merged
            else:
                deduped[col] = same_name_cols.iloc[:, 0]
        df = pd.DataFrame(deduped)

    return df


def detect_missing_required_columns(df, required=("event_name", "timestamp")):
    return [col for col in required if col not in df.columns]