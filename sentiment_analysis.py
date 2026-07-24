import re
from collections import Counter

import numpy as np
import pandas as pd

try:
    from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
    STOPWORDS = set(StopWordRemoverFactory().get_stop_words())
except Exception:
    STOPWORDS = set()


# BACA & NORMALISASI FILE

EXPECTED_COLUMNS = [
    "timestamp", "email", "nama", "asal_instansi", "email_aktif", "no_wa",
    "rating_event", "rating_materi", "rating_mentor", "review", "improvement",
    "reason_to_join", "price_opinion", "is_price_worth", "price_increase",
    "quality_improvemet", "bootcamp_theme_aspiration",
    "id_event", "event_type", "event_name",
]

REQUIRED_COLUMNS = ["review"]


def normalize_feedback_columns(df):
    """Samakan nama kolom (case/spasi-insensitive) dengan format sheet FEEDBACK."""
    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    lower_map = {c.lower().strip(): c for c in df.columns}
    rename_map = {}

    for expected in EXPECTED_COLUMNS:
        if expected in lower_map:
            rename_map[lower_map[expected]] = expected

    df = df.rename(columns=rename_map)
    return df


def detect_missing_required_columns(df):
    return [c for c in REQUIRED_COLUMNS if c not in df.columns]


def read_feedback_file(uploaded_file):
    """Baca file upload (.xlsx / .xls / .csv). Untuk excel, otomatis cari
    sheet bernama FEEDBACK (case-insensitive); kalau tidak ada, pakai sheet
    pertama. Return (df, sheet_name_used, sheet_options)."""

    name = uploaded_file.name.lower()

    if name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
        df = normalize_feedback_columns(df)
        return df, None, None

    xls = pd.ExcelFile(uploaded_file)
    sheet_names = xls.sheet_names

    target_sheet = None
    for s in sheet_names:
        if s.strip().lower() == "feedback":
            target_sheet = s
            break

    if target_sheet is None:
        target_sheet = sheet_names[0]

    df = pd.read_excel(xls, sheet_name=target_sheet)
    df = normalize_feedback_columns(df)

    return df, target_sheet, sheet_names


def read_feedback_sheet(uploaded_file, sheet_name):
    """Baca ulang file excel dengan sheet tertentu (dipakai kalau user ganti sheet)."""
    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
    df = normalize_feedback_columns(df)
    return df


def build_csv_url(sheet_link):
    """Ubah link Google Spreadsheet (edit link) jadi link export CSV.
    Menangani link seperti .../edit?gid=X#gid=X (gid muncul 2x)."""

    sheet_link = sheet_link.strip()
    spreadsheet_id = sheet_link.split("/d/")[1].split("/")[0]

    gid = "0"
    if "gid=" in sheet_link:
        raw_gid = sheet_link.split("gid=")[-1]
        gid = "".join(ch for ch in raw_gid if ch.isdigit()) or "0"

    return (
        f"https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/export?format=csv&gid={gid}"
    )


def read_feedback_from_url(csv_url):
    """Baca sheet feedback langsung dari link Google Spreadsheet (CSV export)."""
    df = pd.read_csv(csv_url)
    df = normalize_feedback_columns(df)
    return df


# TEXT CLEANING (dipakai review & improvement)

_BASE_NORMALIZE_MAP = {
    'kereenn': 'keren', 'mambantu': 'membantu', 'mantaaap': 'mantap',
    'bgt': 'banget', 'bgtt': 'banget', 'gk': 'tidak', 'ga': 'tidak',
    'ngga': 'tidak', 'jg': 'juga', 'yg': 'yang', 'krn': 'karena',
    'dr': 'dari', 'udah': 'sudah', 'dgn': 'dengan',
}

_IMPROVEMENT_NORMALIZE_MAP = {
    **_BASE_NORMALIZE_MAP,
    'materinya': 'materi', 'pembawaannya': 'penyampaian',
    'praktek': 'praktik', 'waktunya': 'waktu',
}


def _normalize_words(text, mapping):
    words = text.split()
    return ' '.join(mapping.get(w, w) for w in words)


def _clean_text(text, keep_dash=False):
    pattern = r'[^\w\s-]' if keep_dash else r'[^\w\s]'
    text = re.sub(pattern, ' ', text)
    text = re.sub(r'\d+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _remove_stopwords(text, extra_stopwords=None):
    stop = STOPWORDS if not extra_stopwords else STOPWORDS.union(extra_stopwords)
    return ' '.join(w for w in text.split() if w not in stop)


# SENTIMENT ANALYSIS - KOLOM REVIEW

POSITIVE_WORDS = [
    'bagus', 'keren', 'mantap', 'baik', 'bermanfaat', 'membantu', 'seru',
    'menambah', 'paham', 'ilmu', 'menyenangkan', 'suka', 'berkembang',
    'senang', 'tau', 'mengerti', 'menarik', 'puas', 'memuaskan',
    'insight', 'insightful', 'wawasan', 'belajar', 'nambah',
    'informatif', 'jelas', 'tertarik', 'berkualitas', 'praktik',
    'praktek', 'oke',
]

NEGATIVE_WORDS = [
    'jelek', 'buruk', 'sulit', 'monoton', 'bosan', 'membosankan',
]

POSITIVE_PHRASES = [
    'mudah dipahami', 'mudah dimengerti', 'sangat membantu',
    'sangat bermanfaat', 'menambah wawasan', 'mentor ramah',
    'mentornya ramah', 'banyak hal yang saya pelajari',
    'banyak hal yang sebelumnya saya tidak tahu jadi tahu',
    'materi mudah dipahami', 'penjelasan mudah dimengerti',
    'sangat mudah dipahami',
]

NEGATIVE_PHRASES = [
    'kurang waktu', 'waktunya kurang', 'kurang durasi', 'durasi kurang',
    'kurang panjang', 'terlalu cepat', 'kurang ekspresif', 'cepat bosan',
]


def indo_sentiment(text):
    text = str(text).lower()
    score = 0

    for splitter in ['tetapi', 'namun', 'tapi']:
        if splitter in text:
            text = text.split(splitter)[-1].strip()
            break

    words = text.split()

    for phrase in POSITIVE_PHRASES:
        if phrase in text:
            score += 2

    for phrase in NEGATIVE_PHRASES:
        if phrase in text:
            score -= 2

    for word in POSITIVE_WORDS:
        if word in words:
            score += 1

    for word in NEGATIVE_WORDS:
        if word in words:
            score -= 1

    if score > 0:
        return 'positive'
    elif score < 0:
        return 'negative'
    return 'neutral'


LOW_INFO_REVIEWS = ['bagus', 'keren', 'mantap', 'lumayan', 'oke']


def analyze_reviews(df):
    """Preprocessing + scoring sentimen untuk kolom `review`.
    Return dataframe hasil filter (review deskriptif, min 4 kata / 20 karakter)
    lengkap dengan kolom sentiment, event_name, id_event (kalau ada)."""

    if 'review' not in df.columns:
        return pd.DataFrame(columns=['review', 'sentiment'])

    keep_cols = ['review']
    for extra in ['event_name', 'id_event', 'event_type']:
        if extra in df.columns:
            keep_cols.append(extra)

    d = df[keep_cols].copy()
    d['review'] = d['review'].replace('-', np.nan)
    d = d.dropna(subset=['review']).copy()

    d['clean_review'] = d['review'].astype(str).str.lower()
    d['clean_review'] = d['clean_review'].apply(lambda t: _normalize_words(t, _BASE_NORMALIZE_MAP))
    d['clean_review'] = d['clean_review'].apply(_clean_text)

    d['word_count'] = d['clean_review'].str.split().str.len()
    d = d[(d['word_count'] >= 4) & (d['clean_review'].str.len() >= 20)].copy()
    d = d[~d['clean_review'].str.strip().isin(LOW_INFO_REVIEWS)].copy()

    d['final_review'] = d['clean_review'].apply(_remove_stopwords)
    d['sentiment'] = d['clean_review'].apply(indo_sentiment)

    return d


def sentiment_distribution(df_reviews):
    dist = df_reviews['sentiment'].value_counts().reindex(
        ['positive', 'neutral', 'negative']
    ).fillna(0).astype(int)
    return dist


def sentiment_by_group(df_reviews, group_col):
    if group_col not in df_reviews.columns:
        return pd.DataFrame()

    grouped = (
        df_reviews.groupby([group_col, 'sentiment'])
        .size()
        .unstack(fill_value=0)
    )

    for col in ['positive', 'neutral', 'negative']:
        if col not in grouped.columns:
            grouped[col] = 0

    grouped = grouped[['positive', 'neutral', 'negative']]

    pct = grouped.div(grouped.sum(axis=1), axis=0).fillna(0) * 100

    return grouped, pct


def top_keywords_text(df_reviews, sentiment):
    text = ' '.join(df_reviews.loc[df_reviews['sentiment'] == sentiment, 'final_review'])
    return text.strip()


def top_keywords_df(df_reviews, sentiment, top_k=15):
    """Frekuensi kata dari review dengan sentiment tertentu, dalam bentuk dataframe
    (dipakai untuk chart 'kata paling sering muncul' pengganti wordcloud)."""
    text = top_keywords_text(df_reviews, sentiment)
    if not text.strip():
        return pd.DataFrame(columns=['keyword', 'frekuensi'])

    freq = Counter(text.split())
    return pd.DataFrame(freq.most_common(top_k), columns=['keyword', 'frekuensi'])


# KATEGORISASI - KOLOM IMPROVEMENT

IMPROVEMENT_CUSTOM_STOPWORDS = {
    'nya', 'yang', 'dan', 'untuk', 'dengan', 'agar',
    'lebih', 'bisa', 'mungkin', 'sudah', 'ada',
    'peserta', 'kak', 'camp', 'intensive',
    'banyak', 'perlu', 'terlalu', 'kalau', 'jadi',
    'buat', 'kurang', 'lagi', 'biar',
    'far', 'so', 'good', 'benar',
    'machine', 'learning', 'ui', 'ux',
    'data', 'analyst', 'special', 'skill',
}

NO_SUGGESTION_PATTERN = (
    r'\btidak ada\b|\bsudah oke\b|\budah oke\b|\bcukup\b|\bbaik\b|\bbagus\b|'
    r'\boke\b|\baman\b|\bnihil\b|\bno\b|\bnothing\b'
)


def categorize_improvement(text):
    text = str(text).lower()

    if any(w in text for w in ['materi', 'penjelasan', 'penyampaian', 'pembelajaran']):
        return 'Materi dan Penyampaian'
    if any(w in text for w in ['waktu', 'durasi', 'lama', 'hari', 'jam', 'diperpanjang']):
        return 'Durasi dan Waktu'
    if any(w in text for w in ['praktik', 'studi kasus', 'case', 'kasus']):
        return 'Praktik dan Studi Kasus'
    if any(w in text for w in ['mentor', 'pemateri']):
        return 'Mentor atau Pemateri'
    if any(w in text for w in ['kelas', 'sesi', 'tanya jawab']):
        return 'Interaksi dan Struktur Kelas'
    return 'Lainnya'


def analyze_improvements(df):
    """Preprocessing + kategorisasi kolom `improvement`. Return dataframe
    hasil filter (buang jawaban kosong / low-info / bukan saran)."""

    if 'improvement' not in df.columns:
        return pd.DataFrame(columns=['improvement', 'category'])

    d = df[['improvement']].copy()
    d['improvement'] = d['improvement'].replace('-', np.nan)
    d = d.dropna(subset=['improvement']).copy()

    d['clean_improvement'] = d['improvement'].astype(str).str.lower()
    d['clean_improvement'] = d['clean_improvement'].apply(
        lambda t: _normalize_words(t, _IMPROVEMENT_NORMALIZE_MAP)
    )
    d['clean_improvement'] = d['clean_improvement'].apply(lambda t: _clean_text(t, keep_dash=True))

    d['clean_improvement'] = (
        d['clean_improvement']
        .str.replace(r'\bdi perpanjang\b', 'diperpanjang', regex=True)
        .str.replace(r'\bdi tambah\b', 'ditambah', regex=True)
        .str.replace(r'\bdi tingkatkan\b', 'ditingkatkan', regex=True)
        .str.replace(r'\bterburu buru\b', 'terburu-buru', regex=True)
    )

    d['word_count'] = d['clean_improvement'].str.split().str.len()
    d = d[(d['word_count'] >= 2) & (d['clean_improvement'].str.len() >= 8)].copy()

    d = d[
        ~d['clean_improvement'].str.contains(NO_SUGGESTION_PATTERN, regex=True, na=False)
    ].copy()

    d['final_improvement'] = d['clean_improvement'].apply(
        lambda t: _remove_stopwords(t, IMPROVEMENT_CUSTOM_STOPWORDS)
    )
    d = d[d['final_improvement'].str.strip() != ''].copy()

    d['category'] = d['clean_improvement'].apply(categorize_improvement)

    return d


def category_summary(df_improvements):
    summary = df_improvements['category'].value_counts().reset_index()
    summary.columns = ['category', 'count']
    summary['percentage'] = (summary['count'] / summary['count'].sum() * 100).round(1)
    return summary


def top_ngrams(df_improvements, n=1, top_k=15, min_df=1):
    all_text = ' '.join(df_improvements['final_improvement'])

    if n == 1:
        words = all_text.split()
        freq = Counter(words)
        result = pd.DataFrame(freq.most_common(top_k), columns=['keyword', 'frekuensi'])
        return result

    try:
        from sklearn.feature_extraction.text import CountVectorizer
    except Exception:
        return pd.DataFrame(columns=['ngram', 'frekuensi'])

    texts = df_improvements['final_improvement'].tolist()
    if len(texts) == 0:
        return pd.DataFrame(columns=['ngram', 'frekuensi'])

    try:
        vectorizer = CountVectorizer(ngram_range=(n, n), min_df=min_df)
        X = vectorizer.fit_transform(texts)
    except ValueError:
        return pd.DataFrame(columns=['ngram', 'frekuensi'])

    counts = pd.DataFrame({
        'ngram': vectorizer.get_feature_names_out(),
        'frekuensi': X.toarray().sum(axis=0),
    }).sort_values(by='frekuensi', ascending=False).head(top_k).reset_index(drop=True)

    return counts
