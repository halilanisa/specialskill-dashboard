import streamlit as st
import pandas as pd
import base64
from column_mapping import normalize_columns, detect_missing_required_columns
from spreadsheets_store import load_spreadsheets, add_spreadsheet
from database import get_history, load_dashboard, delete_dashboard, save_or_update_dashboard

SPREADSHEETS = load_spreadsheets()

st.set_page_config(
    page_title="Dashboard Analitik",
    page_icon="logo.png",
    layout="wide"
)

# ============================================================
# STYLE
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

[data-testid="collapsedControl"]{
    display:none;
}

header{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

#MainMenu{
    visibility:hidden;
}

.block-container{
    padding-top:1.2rem;
    padding-bottom:3rem;
    max-width:1180px;
}

/* ---------- Hero ---------- */
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
    font-size:40px;
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

/* ---------- Stat strip ---------- */
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
    position:relative;
    overflow:hidden;
}

.stat-box.b1{ background:linear-gradient(135deg,#0B2B6B,#2F5FD6); }
.stat-box.b2{ background:linear-gradient(135deg,#0EA5A0,#0B7A87); }
.stat-box.b3{ background:linear-gradient(135deg,#F4A100,#C9720A); }

.stat-box-value{
    font-size:30px;
    font-weight:800;
    line-height:1.1;
}

.stat-box-label{
    font-size:12.5px;
    opacity:.88;
    margin-top:4px;
    letter-spacing:.3px;
    font-weight:500;
}

/* ---------- Add spreadsheet CTA button ---------- */
div[class*="st-key-add_btn_wrap"] .stButton button{
    background:linear-gradient(90deg,#0B2B6B,#3167E0) !important;
    color:#fff !important;
    border:none !important;
    padding:0 28px !important;
    box-shadow:0 10px 22px rgba(23,62,147,.28) !important;
    letter-spacing:.2px;
}

div[class*="st-key-add_btn_wrap"] .stButton button:hover{
    background:linear-gradient(90deg,#0A2560,#2857C7) !important;
    box-shadow:0 12px 26px rgba(23,62,147,.36) !important;
}

/* ---------- Form card ---------- */
div[class*="st-key-add_form_card"]{
    background:#FFFFFF;
    border-radius:22px;
    padding:28px 30px 20px 30px;
    box-shadow:0 12px 30px rgba(15,23,42,.08);
    border:1px solid #EEF1F7;
    margin-top:18px;
    margin-bottom:26px;
}

div[class*="st-key-add_form_card"] h3{
    color:#0B2B6B !important;
    margin-top:0;
}

/* File Uploader */
[data-testid="stFileUploaderDropzone"]{
    background:#F3F4F6 !important;
    border:2px dashed #CBD5E1 !important;
}

[data-testid="stFileUploaderDropzone"] *{
    color:#0B2B6B !important;
}

[data-testid="stFileUploaderDropzone"] button{
    background:#E0E7FF !important;
    color:#0B2B6B !important;
    border:1px solid #93C5FD !important;
}

/* Number Input */
[data-testid="stNumberInputContainer"]{
    background:#F3F4F6 !important;
    border-radius:12px !important;
}

[data-testid="stNumberInputContainer"] input{
    background:#F3F4F6 !important;
    color:#0B2B6B !important;
}

[data-testid="stNumberInputContainer"] button{
    background:#F3F4F6 !important;
    color:#0B2B6B !important;
    border:none !important;
}

[data-testid="stNumberInputContainer"] button:hover{
    background:#E5E7EB !important;
    color:#0B2B6B !important;
}

/* Generic buttons */
.stButton button {
    background:white !important;
    color:#0B2B6B !important;
    border:1px solid #D1D5DB !important;
    border-radius:12px !important;
    font-weight:700 !important;
}

.stButton button:hover {
    background:#F3F4F6 !important;
    color:#0B2B6B !important;
    border:1px solid #CBD5E1 !important;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    background:white !important;
    border:1px solid #E5E7EB !important;
    border-radius:12px !important;
}

[data-testid="stDataFrame"] td{
    color:#374151 !important;
    background:white !important;
}

[data-testid="stDataFrame"] th{
    color:#0B2B6B !important;
    background:#F3F4F6 !important;
}

[data-testid="stDataFrame"] div{
    color:#374151 !important;
}

/* ---------- Daftar Dashboard section ---------- */
.section-title{
    color:#0B2B6B;
    font-size:24px;
    font-weight:800;
    margin:8px 0 4px 0;
}

.section-sub{
    color:#94A3B8;
    font-size:14px;
    margin-bottom:18px;
}

/* ---------- Dashboard cards ---------- */
div[class*="st-key-dash_card_"]{
    background:#FFFFFF;
    border-radius:20px;
    box-shadow:0 4px 16px rgba(15,23,42,.06);
    border:1px solid #EEF1F6;
    overflow:hidden;
    margin-bottom:22px;
    transition:transform .18s ease, box-shadow .18s ease;
}

div[class*="st-key-dash_card_"]:hover{
    transform:translateY(-4px);
    box-shadow:0 16px 32px rgba(15,23,42,.12);
}

.dash-card-top{
    height:6px;
    width:100%;
}

.dash-card-body{
    padding:22px 22px 4px 22px;
}

.dash-card-icon{
    width:44px;
    height:44px;
    border-radius:13px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:21px;
    margin-bottom:14px;
}

.dash-card-title{
    font-size:18.5px;
    font-weight:700;
    color:#0F172A;
    margin-bottom:10px;
    line-height:1.3;
    min-height:48px;
}

.dash-card-meta{
    display:flex;
    flex-direction:column;
    gap:6px;
    font-size:13px;
    color:#64748B;
    margin-bottom:16px;
}

.dash-card-meta b{
    color:#94A3B8;
    font-weight:700;
    font-size:11px;
    letter-spacing:.4px;
    text-transform:uppercase;
    margin-right:2px;
}

.dash-progress-row{
    display:flex;
    align-items:center;
    gap:10px;
    margin-bottom:16px;
}

.dash-progress-track{
    flex:1;
    height:8px;
    border-radius:999px;
    background:#EEF2F7;
    overflow:hidden;
}

.dash-progress-fill{
    height:100%;
    border-radius:999px;
}

.dash-progress-label{
    font-size:12.5px;
    font-weight:800;
    min-width:44px;
    text-align:right;
}

.dash-card-stats{
    display:flex;
    gap:26px;
    margin-bottom:14px;
}

.dash-card-stats .stat-num{
    display:block;
    font-size:19px;
    font-weight:800;
    color:#0F172A;
}

.dash-card-stats .stat-label{
    font-size:11.5px;
    color:#94A3B8;
    letter-spacing:.2px;
}

.dash-card-footer{
    font-size:11px;
    color:#B0B8C4;
    border-top:1px dashed #EEF1F6;
    padding-top:10px;
    margin-top:2px;
}

div[class*="st-key-dash_card_"] div[data-testid="stHorizontalBlock"]{
    padding:0 22px 20px 22px;
    gap:10px !important;
}

div[class*="st-key-dash_card_"] div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button{
    background:#0B2B6B !important;
    color:#fff !important;
    border:none !important;
}

div[class*="st-key-dash_card_"] div[data-testid="stHorizontalBlock"] > div:nth-child(1) .stButton button:hover{
    background:#173E93 !important;
}

div[class*="st-key-dash_card_"] div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button{
    background:#fff !important;
    color:#EF4444 !important;
    border:1px solid #FEE2E2 !important;
}

div[class*="st-key-dash_card_"] div[data-testid="stHorizontalBlock"] > div:nth-child(2) .stButton button:hover{
    background:#FEF2F2 !important;
    border-color:#FCA5A5 !important;
}

/* ---------- Empty state ---------- */
.empty-state{
    text-align:center;
    background:#FFFFFF;
    border:1px dashed #D8E0EE;
    border-radius:20px;
    padding:50px 30px;
    color:#7A8699;
}

.empty-state .emoji{
    font-size:40px;
    margin-bottom:12px;
}

</style>
""", unsafe_allow_html=True)

# LOAD LOGO
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64_image("specialskill.png")

# ============================================================
# HEADER
# ============================================================
col1, col2 = st.columns([10, 1])

with col1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:20px;">
        <img src="data:image/png;base64,{logo}" width="140">
        <span style="
            font-size:20px;
            font-weight:700;
            color:#0A2463;">
            Dashboard Analitik
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button(
        "",
        icon=":material/logout:",
        use_container_width=True,
        help="Keluar"
    ):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown("""
<hr style="
    margin-top:5px;
    margin-bottom:20px;
">
""", unsafe_allow_html=True)

# ============================================================
# HERO
# ============================================================
st.markdown("""
<div class="hero-eyebrow">Special Skill Workspace</div>
<div class="hero-title">Kelola Dashboard</div>
<div class="hero-sub">
    Tambahkan spreadsheet baru untuk membuat dashboard, atau buka dashboard yang sudah ada
</div>
""", unsafe_allow_html=True)

# ============================================================
# STAT STRIP (ringkasan)
# ============================================================
history_preview = get_history()

total_dashboard_count = len(history_preview)

if total_dashboard_count > 0:
    total_pendaftar_all = int(
        pd.to_numeric(history_preview["total_pendaftar"], errors="coerce")
        .fillna(0)
        .sum()
    )

    target_num = pd.to_numeric(history_preview["target"], errors="coerce")
    pendaftar_num = pd.to_numeric(history_preview["total_pendaftar"], errors="coerce")

    capaian_series = (pendaftar_num / target_num * 100)
    capaian_series = capaian_series.replace([float("inf"), float("-inf")], pd.NA)

    avg_capaian = capaian_series.mean()
    avg_capaian = 0 if pd.isna(avg_capaian) else avg_capaian

else:
    total_pendaftar_all = 0
    avg_capaian = 0

st.markdown(f"""
<div class="stat-strip">
    <div class="stat-box b1">
        <div class="stat-box-value">{total_dashboard_count}</div>
        <div class="stat-box-label">DASHBOARD AKTIF</div>
    </div>
    <div class="stat-box b2">
        <div class="stat-box-value">{total_pendaftar_all:,}</div>
        <div class="stat-box-label">TOTAL PENDAFTAR</div>
    </div>
    <div class="stat-box b3">
        <div class="stat-box-value">{avg_capaian:.0f}%</div>
        <div class="stat-box-label">RATA-RATA CAPAIAN TARGET</div>
    </div>
</div>
""", unsafe_allow_html=True)

# CACHE PEMBACAAN SPREADSHEET (biar cepat tapi tetap fresh)
@st.cache_data(ttl=30, show_spinner=False)
def read_sheet(url):
    df = pd.read_csv(url)
    df = normalize_columns(df)
    return df

# ============================================================
# TAMBAH SPREADSHEET
# ============================================================
if "show_form" not in st.session_state:
    st.session_state.show_form = False

with st.container(key="add_btn_wrap"):
    if st.button(
        "Tambah Spreadsheet",
        icon=":material/add:",
        use_container_width=False
    ):
        st.session_state.show_form = True

if st.session_state.show_form:

    with st.container(key="add_form_card"):

        st.markdown("### Tambah Spreadsheet Baru")

        source_options = ["+ Spreadsheet Baru"] + list(SPREADSHEETS.keys())

        source_choice = st.selectbox(
            "Sumber Spreadsheet",
            source_options,
            help="Pilih spreadsheet yang sudah tersimpan untuk membuat dashboard "
                 "event lain dari sumber data yang sama, atau tambahkan spreadsheet baru."
        )

        is_new = source_choice == "+ Spreadsheet Baru"

        csv_url = None
        new_link = ""

        if is_new:

            new_name = st.text_input(
                "Nama Spreadsheet",
                placeholder="Contoh: Webinar AI"
            )

            dashboard_title = st.text_input(
                "Judul Dashboard / Nama Event",
                placeholder="Contoh: Free Class SQL Batch 8"
            )

            new_link = st.text_input(
                "Link Google Spreadsheet",
                placeholder="https://docs.google.com/spreadsheets/..."
            )

            if new_link.strip():
                try:
                    spreadsheet_id = new_link.split("/d/")[1].split("/")[0]

                    gid = "0"

                    if "gid=" in new_link:
                        gid = new_link.split("gid=")[1].split("&")[0]

                    csv_url = (
                        f"https://docs.google.com/spreadsheets/d/"
                        f"{spreadsheet_id}/export?format=csv&gid={gid}"
                    )

                except Exception:
                    st.error(
                        "Link spreadsheet tidak valid. "
                        "Pastikan formatnya seperti "
                        "https://docs.google.com/spreadsheets/d/.../edit"
                    )

        else:

            new_name = source_choice
            sheet_info = SPREADSHEETS[source_choice]
            dashboard_title = sheet_info["dashboard_title"]
            csv_url = sheet_info["url"]

            st.caption(f"Menggunakan spreadsheet tersimpan: **{source_choice}**")

        df_preview = None

        if csv_url:
            try:
                df_preview = read_sheet(csv_url)
            except Exception as e:
                st.error(
                    "Spreadsheet tidak dapat dibaca. Pastikan link benar dan "
                    f"spreadsheet dapat diakses publik! ({e})"
                )
                df_preview = None

        selected_event = dashboard_title
        df_event = None
        target_pendaftar = 1000

        if df_preview is not None:

            missing_cols = detect_missing_required_columns(df_preview)

            if missing_cols:
                st.error(
                    "Format spreadsheet tidak dikenali. Kolom berikut tidak "
                    f"ditemukan/tidak bisa dipetakan: {', '.join(missing_cols)}. "
                    "Cek nama header di spreadsheet, atau tambahkan aliasnya "
                    "di column_mapping.py."
                )
                df_preview = None

            else:

                st.info(
                    "Kolom yang dianalisis otomatis: "
                    "Sumber Informasi • Jenjang Pendidikan • Provinsi • Tanggal Daftar"
                )

                # PILIH EVENT (khusus spreadsheet yang punya banyak event,
                # misal Master Data (Free Event))
                if "event_name" in df_preview.columns:

                    event_list = (
                        df_preview["event_name"]
                        .dropna()
                        .sort_values()
                        .unique()
                    )

                    if len(event_list) > 1:
                        selected_event = st.selectbox(
                            "Pilih Event",
                            event_list
                        )
                    elif len(event_list) == 1:
                        selected_event = event_list[0]

                    df_event = df_preview[
                        df_preview["event_name"] == selected_event
                    ].copy()

                else:
                    df_event = df_preview.copy()

                # TARGET PENDAFTAR
                target_pendaftar = st.number_input(
                    "Target Pendaftar",
                    min_value=1,
                    value=1000,
                    step=100
                )

                # INFORMASI DATA
                st.success(
                    f"Total Spreadsheet: {len(df_preview)} baris | "
                    f"Event '{selected_event}': {len(df_event)} baris"
                )

                # PREVIEW
                st.markdown("""
                <p style="
                    font-size:14px;
                    font-weight:400;
                    color:#31333F;
                    margin-bottom:0.2rem;
                ">
                    Preview Data
                </p>
                """, unsafe_allow_html=True)

                st.dataframe(
                    df_event.head(),
                    use_container_width=True,
                    hide_index=True
                )

        col_btn1, col_btn2, _ = st.columns([1, 1, 8])

        with col_btn1:
            save_clicked = st.button(
                "Simpan",
                use_container_width=True,
                type="primary"
            )

        with col_btn2:
            cancel_clicked = st.button(
                "Batal",
                use_container_width=True
            )

        if cancel_clicked:
            st.session_state.show_form = False
            st.rerun()

        if save_clicked:

            errors = []

            if is_new:
                if not new_name.strip():
                    errors.append("Nama Spreadsheet wajib diisi")
                if not new_link.strip():
                    errors.append("Link Google Spreadsheet wajib diisi")
                if (
                    not dashboard_title.strip()
                    and (df_preview is None or "event_name" not in df_preview.columns)
                ):
                    errors.append("Judul Dashboard / Nama Event wajib diisi")

            if df_preview is None:
                errors.append(
                    "Spreadsheet belum berhasil dibaca, cek kembali link/format datanya"
                )

            if df_preview is not None and (df_event is None or len(df_event) == 0):
                errors.append("Tidak ada data untuk event yang dipilih")

            if errors:
                st.warning(" • ".join(errors))

            else:

                if is_new:
                    add_spreadsheet(
                        new_name,
                        dashboard_title.strip() or str(selected_event),
                        csv_url
                    )

                df_to_save = df_event.copy()

                if "timestamp" in df_to_save.columns:
                    df_to_save["timestamp"] = pd.to_datetime(
                        df_to_save["timestamp"],
                        errors="coerce"
                    )

                    start_date = df_to_save["timestamp"].min()
                    end_date = df_to_save["timestamp"].max()

                    if pd.notna(start_date) and pd.notna(end_date):
                        periode = (
                            start_date.strftime("%d %b %Y")
                            + " - " +
                            end_date.strftime("%d %b %Y")
                        )
                    else:
                        periode = "-"

                else:
                    periode = "-"

                save_or_update_dashboard(
                    event_name=str(selected_event),
                    file_name=new_name,
                    periode=periode,
                    target=target_pendaftar,
                    df=df_to_save
                )

                st.session_state.show_form = False

                read_sheet.clear()

                st.success("Dashboard berhasil dibuat!")

                st.rerun()

    st.stop()

# ============================================================
# DAFTAR DASHBOARD
# ============================================================
st.markdown("""
<div class="section-title">Daftar Dashboard</div>
<div class="section-sub">Setiap dashboard selalu memuat data terbaru dari spreadsheet sumbernya</div>
""", unsafe_allow_html=True)

history = get_history()

ACCENT_COLORS = ["#4A82E8", "#8B5CF6", "#0EA5A0", "#F4B400", "#FF6B81", "#06B6D4"]


def pick_icon(event_name):
    name = str(event_name).lower()
    if any(k in name for k in ["ui/ux", "ui", "ux", "design"]):
        return "🎨"
    if any(k in name for k in ["python", "sql", "data", "program", "coding"]):
        return "💻"
    if any(k in name for k in ["wordpress", "web"]):
        return "🌐"
    if any(k in name for k in ["marketing", "sosial", "social", "digital"]):
        return "📢"
    if any(k in name for k in ["business", "bisnis", "socio", "wirausaha"]):
        return "📈"
    return "🎯"


if history.empty:

    st.markdown("""
    <div class="empty-state">
        <div class="emoji">🗂️</div>
        <b>Belum ada dashboard yang disimpan</b><br>
        Klik <b>Tambah Spreadsheet</b> di atas untuk membuat dashboard pertama Anda.
    </div>
    """, unsafe_allow_html=True)

else:

    rows = list(history.iterrows())

    for row_start in range(0, len(rows), 2):

        pair = rows[row_start:row_start + 2]
        cols = st.columns(2)

        for col, (idx, row) in zip(cols, pair):

            accent = ACCENT_COLORS[idx % len(ACCENT_COLORS)]
            icon = pick_icon(row["event_name"])

            target_val = float(row["target"]) if row["target"] else 1
            total_val = float(row["total_pendaftar"])
            pct = (total_val / target_val * 100) if target_val else 0

            if pct >= 100:
                bar_color = "#10B981"
            elif pct >= 50:
                bar_color = "#4A82E8"
            else:
                bar_color = "#F4B400"

            with col:

                with st.container(key=f"dash_card_{row['id']}"):

                    st.markdown(f"""
                    <div class="dash-card-top" style="background:{accent};"></div>
                    <div class="dash-card-body">
                        <div class="dash-card-icon" style="background:{accent}1F;color:{accent};">
                            {icon}
                        </div>
                        <div class="dash-card-title">{row['event_name']}</div>
                        <div class="dash-card-meta">
                            <span><b>File</b> · {row['file_name']}</span>
                            <span><b>Periode</b> · {row['periode']}</span>
                        </div>
                        <div class="dash-progress-row">
                            <div class="dash-progress-track">
                                <div class="dash-progress-fill" style="width:{min(pct,100):.1f}%;background:{bar_color};"></div>
                            </div>
                            <div class="dash-progress-label" style="color:{bar_color};">{pct:.0f}%</div>
                        </div>
                        <div class="dash-card-stats">
                            <div>
                                <span class="stat-num">{int(total_val):,}</span>
                                <span class="stat-label">PENDAFTAR</span>
                            </div>
                            <div>
                                <span class="stat-num">{int(target_val):,}</span>
                                <span class="stat-label">TARGET</span>
                            </div>
                        </div>
                        <div class="dash-card-footer">Disimpan pada {row['created_at']}</div>
                    </div>
                    """, unsafe_allow_html=True)

                    c1, c2 = st.columns([3, 1])

                    with c1:
                        if st.button(
                            "Buka Dashboard",
                            key=f"open_{row['id']}",
                            use_container_width=True
                        ):

                            dashboard = load_dashboard(row["id"])

                            st.session_state["data"] = dashboard["data"]
                            st.session_state["target"] = dashboard["target"]
                            st.session_state["file_name"] = dashboard["file_name"]
                            st.session_state["event_name"] = dashboard["event_name"]
                            st.session_state["saved"] = True

                            st.switch_page("pages/analytics.py")

                    with c2:
                        if st.button(
                            "",
                            icon=":material/delete:",
                            key=f"delete_{row['id']}",
                            use_container_width=True,
                            help="Hapus dashboard"
                        ):

                            delete_dashboard(row["id"])
                            st.rerun()