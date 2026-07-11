import streamlit as st
import pandas as pd
import base64
from column_mapping import normalize_columns, detect_missing_required_columns
from spreadsheets_store import load_spreadsheets, add_spreadsheet, delete_spreadsheet

SPREADSHEETS = load_spreadsheets()

st.set_page_config(
    page_title="Dashboard Analitik",
    page_icon="logo.png",
    layout="wide"
)

# HIDE STREAMLIT SIDEBAR
st.markdown("""
<style>

.stApp{
    background:white !important;
}

[data-testid="stAppViewContainer"]{
    background:white !important;
}

/* Sidebar */
[data-testid="stSidebar"]{
    display:none;
}

/* Tombol buka sidebar */
[data-testid="collapsedControl"]{
    display:none;
}

/* Header Streamlit */
header{
    visibility:hidden;
}

/* Footer */
footer{
    visibility:hidden;
}

/* Main Menu */
#MainMenu{
    visibility:hidden;
}

/* Spacing */
.block-container{
    padding-top:1rem;
    max-width:100%;
}

/* File Uploader */
[data-testid="stFileUploaderDropzone"]{
    background:#F3F4F6 !important;
    border:2px dashed #CBD5E1 !important;
}

[data-testid="stFileUploaderDropzone"] *{
    color:#0B2B6B !important;
}

/* Tombol Browse Files */
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

/* Tombol + dan - */
[data-testid="stNumberInputContainer"] button{
    background:#F3F4F6 !important;
    color:#0B2B6B !important;
    border:none !important;
}

[data-testid="stNumberInputContainer"] button:hover{
    background:#E5E7EB !important;
    color:#0B2B6B !important;
}
            
/* Tombol Keluar */

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
            
/* Preview Data */
h3{
    color:#0B2B6B !important;
}

/* Dataframe */
[data-testid="stDataFrame"]{
    background:white !important;
    border:1px solid #E5E7EB !important;
    border-radius:12px !important;
}

/* Isi sel tabel */
[data-testid="stDataFrame"] td{
    color:#374151 !important;
    background:white !important;
}

/* Header tabel */
[data-testid="stDataFrame"] th{
    color:#0B2B6B !important;
    background:#F3F4F6 !important;
}

/* Seluruh teks dataframe */
[data-testid="stDataFrame"] div{
    color:#374151 !important;
}

</style>
""", unsafe_allow_html=True)

# LOAD LOGO
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64_image("specialskill.png")

# HEADER
col1, col2, col3 = st.columns([9, 1, 1])

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
        icon=":material/history:",
        use_container_width=True,
        help="History"
    ):
        st.switch_page("pages/history.py")

with col3:
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
    margin-bottom:10px;
">
""", unsafe_allow_html=True)

# TITLE
st.markdown("""
<div style="text-align:center;margin-top:30px;">
    <h1 style="color:#0A2463;">
        Unggah Data
    </h1>
    <p style="font-size:18px;color:#666;">
        Unggah file XLSX, XLS, CSV untuk menghasilkan dashboard otomatis
    </p>
</div>
""", unsafe_allow_html=True)

# TAMBAH SPREADSHEET

if "show_form" not in st.session_state:
    st.session_state.show_form = False

# tombol tambah
if st.button(
    "Tambah Spreadsheet",
    icon=":material/add:",
    use_container_width=False
):
    st.session_state.show_form = True

# FORM TAMBAH
if st.session_state.show_form:

    st.markdown("### Tambah Spreadsheet Baru")

    new_name = st.text_input(
        "Nama Spreadsheet",
        placeholder="Contoh: Webinar AI"
    )

    new_link = st.text_input(
        "Link Google Spreadsheet",
        placeholder="https://docs.google.com/spreadsheets/..."
    )

    col_btn1, col_btn2, _ = st.columns([1, 1, 8])

    with col_btn1:
        save_clicked = st.button(
            "Simpan",
            use_container_width=True
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

        if not new_name.strip() or not new_link.strip():
            st.warning("Nama spreadsheet dan link wajib diisi!")

        else:

            try:

                spreadsheet_id = new_link.split("/d/")[1].split("/")[0]

                gid = "0"

                if "gid=" in new_link:
                    gid = new_link.split("gid=")[1].split("&")[0]

                csv_url = (
                    f"https://docs.google.com/spreadsheets/d/"
                    f"{spreadsheet_id}/export?format=csv&gid={gid}"
                )

                # Coba baca dulu supaya dipastikan valid
                pd.read_csv(csv_url)

            except Exception:
                st.error(
                    "Spreadsheet tidak dapat dibaca. Pastikan link benar dan spreadsheet dapat diakses publik!"
                )
                st.stop()

            add_spreadsheet(new_name, csv_url)

            st.session_state.show_form = False

            st.success("Spreadsheet berhasil ditambahkan!")

            st.rerun()

    st.stop()

# PILIH SPREADSHEET
if len(SPREADSHEETS) == 0:
    st.warning("Belum ada spreadsheet yang tersimpan!")
    st.stop()

col_select, col_delete = st.columns([5, 1])

with col_select:
    selected_sheet = st.selectbox(
        "Pilih Spreadsheet",
        list(SPREADSHEETS.keys())
    )

with col_delete:
    st.markdown("<div style='height:1.8rem'></div>", unsafe_allow_html=True)
    if st.button(
        "Hapus",
        icon=":material/delete:",
        use_container_width=True
    ):
        st.session_state.confirm_delete = selected_sheet

# KONFIRMASI HAPUS SPREADSHEET
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None

if st.session_state.confirm_delete == selected_sheet:

    st.warning(
        f"Yakin ingin menghapus spreadsheet **{selected_sheet}** dari daftar? "
        "Dashboard yang sudah pernah disimpan dari spreadsheet ini "
        "tidak akan ikut terhapus (histori tetap aman)"
    )

    col_yes, col_no, _ = st.columns([1, 1, 8])

    with col_yes:
        if st.button("Ya, Hapus", use_container_width=True):
            delete_spreadsheet(selected_sheet)
            st.session_state.confirm_delete = None
            st.rerun()

    with col_no:
        if st.button("Batal", use_container_width=True, key="cancel_delete_sheet"):
            st.session_state.confirm_delete = None
            st.rerun()

    st.stop()

# INFO
st.info(
    "Kolom yang dianalisis otomatis: "
    "Sumber Informasi • Jenjang Pendidikan • Provinsi • Tanggal Daftar"
)

# LOAD DATA
try:

    url = SPREADSHEETS[selected_sheet]

    df = pd.read_csv(url)

    df = normalize_columns(df)

    missing_cols = detect_missing_required_columns(df)

    if missing_cols:
        st.error(
            "Format spreadsheet tidak dikenali. Kolom berikut tidak "
            f"ditemukan/tidak bisa dipetakan: {', '.join(missing_cols)}. "
            "Cek nama header di spreadsheet, atau tambahkan aliasnya "
            "di column_mapping.py."
        )
        st.stop()

    total_data = len(df)

    # PILIH EVENT
    event_list = (
        df["event_name"]
        .dropna()
        .sort_values()
        .unique()
    )

    selected_event = st.selectbox(
        "Pilih Event",
        event_list
    )

    df_event = df[df["event_name"] == selected_event].copy()

    # PILIH TANGGAL
    df_event["timestamp"] = pd.to_datetime(
        df_event["timestamp"],
        errors="coerce"
    )

    min_date = df_event["timestamp"].min().date()
    max_date = df_event["timestamp"].max().date()

    selected_dates = st.date_input(
        "Rentang Tanggal",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )

    if len(selected_dates) == 2:

        start_date, end_date = selected_dates

        df_filtered = df_event[
            (df_event["timestamp"].dt.date >= start_date)
            &
            (df_event["timestamp"].dt.date <= end_date)
        ].copy()

    else:

        df_filtered = df_event.copy()

    # TARGET PENDAFTAR
    target_pendaftar = st.number_input(
        "Target Pendaftar",
        min_value=1,
        value=1000,
        step=100
    )

    # INFORMASI DATA
    st.success(
        f"Total Spreadsheet: {total_data} baris | "
        f"Event '{selected_event}': {len(df_event)} baris | "
        f"Periode Dipilih: {len(df_filtered)} baris"
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
        df_filtered.head(),
        use_container_width=True,
        hide_index=True
    )

    # GENERATE
    if st.button(
        "Generate Dashboard",
        use_container_width=True,
        type="primary"
    ):

        st.session_state["data"] = df_filtered
        st.session_state["file_name"] = selected_sheet
        st.session_state["target"] = target_pendaftar
        st.session_state["event_name"] = selected_event
        st.session_state["saved"] = False

        st.switch_page("pages/analytics.py")

except Exception as e:
    st.error(f"Gagal membaca spreadsheet: {e}")