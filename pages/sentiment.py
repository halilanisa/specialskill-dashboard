import base64

import pandas as pd
import plotly.express as px
import streamlit as st

from sentiment_analysis import (
    build_csv_url,
    read_feedback_from_url,
    detect_missing_required_columns,
    analyze_reviews,
    sentiment_distribution,
    sentiment_by_group,
    top_keywords_df,
    analyze_improvements,
    category_summary,
    top_ngrams,
)
from spreadsheets_store import load_spreadsheets, add_spreadsheet

st.set_page_config(
    page_title="Analisis Sentimen",
    page_icon="logo.png",
    layout="wide",
)

# ============================================================
# STYLE (samain dengan halaman lain)
# ============================================================
st.markdown("""
<style>

.stApp{
    background:#F4F7FC !important;
}

[data-testid="stAppViewContainer"]{
    background:#F4F7FC !important;
}

[data-testid="stSidebar"]{
    display:none;
}

#MainMenu, footer, header{
    visibility:hidden;
}

.block-container{
    padding-top:1.2rem;
    padding-bottom:3rem;
    max-width:1180px;
}

.stButton button{
    background:white !important;
    color:#0B2B6B !important;
    border:1px solid #D1D5DB !important;
    border-radius:12px !important;
    font-weight:700 !important;
}

.stButton button:hover{
    background:#F3F4F6 !important;
    color:#0B2B6B !important;
    border:1px solid #CBD5E1 !important;
}

.hero-eyebrow{
    text-align:center;
    font-size:12.5px;
    font-weight:700;
    letter-spacing:3px;
    color:#4A82E8;
    text-transform:uppercase;
    margin-bottom:8px;
}

.hero-title{
    text-align:center;
    color:#0B2B6B;
    font-size:36px;
    font-weight:800;
    margin-bottom:6px;
    letter-spacing:-0.5px;
}

.hero-sub{
    text-align:center;
    font-size:16px;
    color:#7A8699;
    margin-bottom:26px;
}

.stat-strip{
    display:flex;
    gap:16px;
    margin:6px 0 30px 0;
    flex-wrap:wrap;
}

.stat-box{
    flex:1;
    min-width:170px;
    border-radius:18px;
    padding:20px 24px;
    color:#fff;
    box-shadow:0 10px 24px rgba(15,23,42,.12);
}

.stat-box.b1{ background:linear-gradient(135deg,#0B2B6B,#2F5FD6); }
.stat-box.b2{ background:linear-gradient(135deg,#10B981,#0B7A87); }
.stat-box.b3{ background:linear-gradient(135deg,#F4B400,#C9720A); }
.stat-box.b4{ background:linear-gradient(135deg,#EF4444,#B91C1C); }

.stat-box-value{
    font-size:28px;
    font-weight:800;
    line-height:1.1;
}

.stat-box-label{
    font-size:12px;
    opacity:.88;
    margin-top:4px;
    letter-spacing:.3px;
    font-weight:500;
}

.section-title{
    font-size:19px;
    font-weight:800;
    color:#0B2B6B;
    margin:26px 0 4px 0;
}

.section-sub{
    font-size:13.5px;
    color:#8794A8;
    margin-bottom:14px;
}

div[class*="st-key-upload_card"]{
    background:#FFFFFF;
    border-radius:20px;
    padding:26px 28px;
    box-shadow:0 10px 26px rgba(15,23,42,.06);
    border:1px solid #EEF1F7;
    margin-bottom:6px;
}

/* ---------- Chart & table cards (rounded, seperti kartu di dashboard) ---------- */
div[data-testid="stPlotlyChart"]{
    background:#FFFFFF;
    border-radius:20px;
    padding:14px 16px;
    box-shadow:0 10px 26px rgba(15,23,42,.06);
    border:1px solid #EEF1F7;
    overflow:hidden;
}

div[data-testid="stPlotlyChart"] > div,
div[data-testid="stPlotlyChart"] iframe{
    border-radius:14px;
    overflow:hidden;
}

div[data-testid="stDataFrame"]{
    border-radius:20px;
    overflow:hidden;
    border:1px solid #EEF1F7;
    box-shadow:0 10px 26px rgba(15,23,42,.06);
}

</style>
""", unsafe_allow_html=True)


def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


logo = get_base64_image("specialskill.png")

# ============================================================
# HEADER
# ============================================================
col1, col2, col3 = st.columns([10, 1, 1])

with col1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:20px;">
        <img src="data:image/png;base64,{logo}" width="140">
        <span style="font-size:20px;font-weight:700;color:#0A2463;">
            Analisis Sentimen
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("", icon=":material/arrow_back:", use_container_width=True, help="Kembali"):
        st.switch_page("pages/dashboard.py")

with col3:
    if st.button("", icon=":material/logout:", use_container_width=True, help="Keluar"):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown("""<hr style="margin-top:5px;margin-bottom:20px;">""", unsafe_allow_html=True)

st.markdown("""
<div class="hero-eyebrow">Special Skill Workspace</div>
<div class="hero-title">Analisis Sentimen Feedback</div>
<div class="hero-sub">
    Upload data dari sheet <b>FEEDBACK</b> (Master Data) untuk melihat sentimen review
    dan kategori masukan peserta secara otomatis
</div>
""", unsafe_allow_html=True)

# ============================================================
# LINK SPREADSHEET (pola sama seperti "Tambah Spreadsheet")
# ============================================================
SPREADSHEETS = load_spreadsheets()

with st.container(key="upload_card"):

    st.markdown("##### Sumber Data Feedback")
    st.caption(
        "Masukkan link Google Spreadsheet ke sheet **FEEDBACK**, atau pilih "
        "spreadsheet yang sudah pernah disimpan sebelumnya."
    )

    source_options = ["+ Link Baru"] + list(SPREADSHEETS.keys())

    source_choice = st.selectbox(
        "Sumber Spreadsheet",
        source_options,
        label_visibility="collapsed",
    )

    is_new = source_choice == "+ Link Baru"

    csv_url = None
    save_this = False
    new_name = ""

    if is_new:
        new_link = st.text_input(
            "Link Google Spreadsheet",
            placeholder="https://docs.google.com/spreadsheets/d/.../edit#gid=...",
        )

        if new_link.strip():
            try:
                csv_url = build_csv_url(new_link.strip())
            except Exception:
                st.error(
                    "Link spreadsheet tidak valid. Pastikan formatnya seperti "
                    "https://docs.google.com/spreadsheets/d/.../edit#gid=..."
                )

        if csv_url:
            save_col1, save_col2 = st.columns([1, 3])
            with save_col1:
                save_this = st.checkbox("Simpan link ini")
            if save_this:
                with save_col2:
                    new_name = st.text_input(
                        "Nama untuk disimpan",
                        placeholder="Contoh: Master Data (Feedback)",
                        label_visibility="collapsed",
                    )
    else:
        csv_url = SPREADSHEETS[source_choice]["url"]
        st.caption(f"Menggunakan spreadsheet tersimpan: **{source_choice}**")

if not csv_url:
    st.info("Masukkan link Google Spreadsheet di atas untuk memulai analisis.")
    st.stop()

@st.cache_data(ttl=30, show_spinner=False)
def _load_from_url(url):
    return read_feedback_from_url(url)

try:
    df_raw = _load_from_url(csv_url)
except Exception as e:
    st.error(
        "Spreadsheet tidak dapat dibaca. Pastikan link benar dan spreadsheet "
        f"dapat diakses publik! ({e})"
    )
    st.stop()

if is_new and save_this:
    if new_name.strip():
        add_spreadsheet(new_name.strip(), "Analisis Sentimen", csv_url)
        st.success(f"Link disimpan sebagai '{new_name.strip()}'. Muncul di daftar sumber spreadsheet lain kali.")
    else:
        st.warning("Isi dulu nama untuk menyimpan link ini.")

missing_cols = detect_missing_required_columns(df_raw)

if missing_cols:
    st.error(
        "Format file tidak dikenali. Kolom berikut tidak ditemukan: "
        f"{', '.join(missing_cols)}. Pastikan file memiliki kolom 'review' "
        "seperti pada sheet FEEDBACK master data."
    )
    st.stop()

st.success(f"File berhasil dibaca • {len(df_raw):,} baris data ditemukan")

# ============================================================
# JALANKAN ANALISIS
# ============================================================
df_reviews = analyze_reviews(df_raw)
df_improvements = analyze_improvements(df_raw) if "improvement" in df_raw.columns else pd.DataFrame()

if df_reviews.empty:
    st.warning("Tidak ada review yang cukup deskriptif untuk dianalisis (min. 4 kata).")
    st.stop()

dist = sentiment_distribution(df_reviews)
total_review = int(dist.sum())
pos_pct = (dist["positive"] / total_review * 100) if total_review else 0
neu_pct = (dist["neutral"] / total_review * 100) if total_review else 0
neg_pct = (dist["negative"] / total_review * 100) if total_review else 0

st.markdown("""
<div class="section-title">Ringkasan Sentimen</div>
<div class="section-sub">Dihitung dari review yang cukup deskriptif (min. 4 kata)</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stat-strip">
    <div class="stat-box b1">
        <div class="stat-box-value">{total_review:,}</div>
        <div class="stat-box-label">REVIEW DIANALISIS</div>
    </div>
    <div class="stat-box b2">
        <div class="stat-box-value">{dist['positive']:,} ({pos_pct:.0f}%)</div>
        <div class="stat-box-label">POSITIF</div>
    </div>
    <div class="stat-box b3">
        <div class="stat-box-value">{dist['neutral']:,} ({neu_pct:.0f}%)</div>
        <div class="stat-box-label">NETRAL</div>
    </div>
    <div class="stat-box b4">
        <div class="stat-box-value">{dist['negative']:,} ({neg_pct:.0f}%)</div>
        <div class="stat-box-label">NEGATIF</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ---- Chart distribusi ----
SENTIMENT_LABEL_ID = {"positive": "Positif", "neutral": "Netral", "negative": "Negatif"}
color_map = {"Positif": "#10B981", "Netral": "#F4B400", "Negatif": "#FB7185"}
CHART_HEIGHT = 380

chart_col1, chart_col2 = st.columns([1.3, 1])

with chart_col1:
    dist_df = dist.reset_index()
    dist_df.columns = ["sentiment", "jumlah"]
    dist_df["sentiment"] = dist_df["sentiment"].map(SENTIMENT_LABEL_ID).fillna(dist_df["sentiment"])
    fig_bar = px.bar(
        dist_df, x="sentiment", y="jumlah", color="sentiment",
        color_discrete_map=color_map, text="jumlah",
        title="Distribusi Sentimen Keseluruhan",
    )
    fig_bar.update_traces(textposition="outside")
    fig_bar.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        height=CHART_HEIGHT, margin=dict(t=50, b=10, l=10, r=10),
        xaxis_title="Sentimen",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_col2:
    fig_pie = px.pie(
        dist_df, names="sentiment", values="jumlah",
        color="sentiment", color_discrete_map=color_map,
        title="Persentase Sentimen",
    )
    fig_pie.update_traces(textposition="inside", textinfo="percent")
    fig_pie.update_layout(
        height=CHART_HEIGHT, margin=dict(t=50, b=10, l=10, r=120),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.02,
            font=dict(size=12),
        ),
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# ============================================================
# SENTIMEN PER EVENT
# ============================================================
if "event_name" in df_reviews.columns and df_reviews["event_name"].nunique() > 1:

    st.markdown("""
    <div class="section-title">Sentimen per Learning Path / Event</div>
    """, unsafe_allow_html=True)

    grouped, pct = sentiment_by_group(df_reviews, "event_name")

    plot_df = grouped.reset_index().melt(
        id_vars="event_name", var_name="sentiment", value_name="jumlah"
    )
    plot_df["sentiment"] = plot_df["sentiment"].map(SENTIMENT_LABEL_ID).fillna(plot_df["sentiment"])

    fig_stack = px.bar(
        plot_df, x="event_name", y="jumlah", color="sentiment",
        color_discrete_map=color_map, barmode="stack",
        title="Sentimen per Event (jumlah)",
    )
    fig_stack.update_layout(
        xaxis_tickangle=-30,
        plot_bgcolor="white",
        paper_bgcolor="white",
        height=460,
        margin=dict(l=10, r=10, t=50, b=110),
        legend_title="Sentimen",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.45,
            xanchor="center",
            x=0.5,
        ),
    )
    st.plotly_chart(fig_stack, use_container_width=True)

    top_pos = pct["positive"].sort_values(ascending=False).reset_index()
    top_neg = pct["negative"].sort_values(ascending=False).reset_index()

    col_top1, col_top2 = st.columns(2)

    with col_top1:
        fig_top_pos = px.bar(
            top_pos.head(10), x="positive", y="event_name", orientation="h",
            title="Top 10 Event - Sentimen Positif Tertinggi (%)",
            color_discrete_sequence=["#10B981"],
        )
        fig_top_pos.update_layout(yaxis={"categoryorder": "total ascending"}, plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_top_pos, use_container_width=True)

    with col_top2:
        fig_top_neg = px.bar(
            top_neg.head(10), x="negative", y="event_name", orientation="h",
            title="Top 10 Event - Sentimen Negatif Tertinggi (%)",
            color_discrete_sequence=["#FB7185"],
        )
        fig_top_neg.update_layout(yaxis={"categoryorder": "total ascending"}, plot_bgcolor="white", paper_bgcolor="white")
        st.plotly_chart(fig_top_neg, use_container_width=True)

# ============================================================
# KATA YANG PALING SERING MUNCUL
# ============================================================
st.markdown("""<div class="section-title">Kata yang Paling Sering Muncul</div>""", unsafe_allow_html=True)

wc_col1, wc_col2 = st.columns(2)


def render_keyword_chart(container, df_reviews, sentiment, title, color):
    with container:
        kw_df = top_keywords_df(df_reviews, sentiment, top_k=12)
        if kw_df.empty:
            st.markdown(f"**{title}**")
            st.caption("Tidak ada data yang cukup untuk kata kunci ini.")
            return

        fig = px.bar(
            kw_df.sort_values("frekuensi", ascending=True),
            x="frekuensi", y="keyword", orientation="h",
            title=title, color_discrete_sequence=[color],
        )
        fig.update_layout(
            plot_bgcolor="white", paper_bgcolor="white",
            height=380, margin=dict(t=50, b=10, l=10, r=10),
        )
        st.plotly_chart(fig, use_container_width=True)


render_keyword_chart(wc_col1, df_reviews, "positive", "Kata Paling Sering - Sentimen Positif", "#10B981")
render_keyword_chart(wc_col2, df_reviews, "negative", "Kata Paling Sering - Sentimen Negatif", "#FB7185")

# ============================================================
# CONTOH REVIEW PER SENTIMEN
# ============================================================
st.markdown("""<div class="section-title">Contoh Review</div>""", unsafe_allow_html=True)

tab_pos, tab_neu, tab_neg = st.tabs(["Positif", "Netral", "Negatif"])

for tab, sentiment_key in [(tab_pos, "positive"), (tab_neu, "neutral"), (tab_neg, "negative")]:
    with tab:
        sample = df_reviews.loc[df_reviews["sentiment"] == sentiment_key, "review"].head(10)
        if sample.empty:
            st.caption("Tidak ada contoh untuk kategori ini.")
        else:
            for text in sample:
                st.markdown(f"- {text}")

# ============================================================
# ANALISIS IMPROVEMENT
# ============================================================
if not df_improvements.empty:

    st.markdown("""
    <div class="section-title">Kategori Masukan Peserta (Improvement)</div>
    <div class="section-sub">Dikelompokkan otomatis berdasarkan tema masukan</div>
    """, unsafe_allow_html=True)

    cat_summary = category_summary(df_improvements)

    fig_cat = px.bar(
        cat_summary.sort_values("count", ascending=True),
        x="count", y="category", orientation="h", text="count",
        title="Distribusi Kategori Masukan",
        color_discrete_sequence=["#4A82E8"],
    )
    fig_cat.update_traces(textposition="outside")
    fig_cat.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        height=420, margin=dict(t=50, b=10, l=10, r=60),
    )
    st.plotly_chart(fig_cat, use_container_width=True)

    st.markdown("**Contoh Masukan per Kategori**")

    category_tabs = st.tabs(cat_summary["category"].tolist())

    for tab, cat in zip(category_tabs, cat_summary["category"].tolist()):
        with tab:
            examples = (
                df_improvements.loc[df_improvements["category"] == cat, "improvement"]
                .dropna().drop_duplicates().head(8)
            )
            if examples.empty:
                st.caption("Tidak ada contoh.")
            else:
                for text in examples:
                    st.markdown(f"- {text}")

    with st.expander("Lihat Top Keyword & Frasa Masukan"):
        kw_col1, kw_col2, kw_col3 = st.columns(3)

        with kw_col1:
            st.markdown("**Top Keyword**")
            st.dataframe(top_ngrams(df_improvements, n=1, top_k=15), hide_index=True, use_container_width=True)

        with kw_col2:
            st.markdown("**Top Bigram**")
            st.dataframe(top_ngrams(df_improvements, n=2, top_k=15, min_df=2), hide_index=True, use_container_width=True)

        with kw_col3:
            st.markdown("**Top Trigram**")
            st.dataframe(top_ngrams(df_improvements, n=3, top_k=15, min_df=2), hide_index=True, use_container_width=True)

else:
    st.info("Kolom 'improvement' tidak ditemukan atau tidak ada data yang bisa dikategorikan.")