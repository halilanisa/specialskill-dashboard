import streamlit as st
import pandas as pd
import base64

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
col1, col2 = st.columns([10, 1])

with col1:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:20px;">
        <img src="data:image/png;base64,{logo}" width="140">
        <span style="
            font-size:30px;
            font-weight:700;
            color:#0A2463;">
            Dashboard Analitik
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if st.button("Keluar", use_container_width=True):
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
        Upload File Data
    </h1>
    <p style="font-size:18px;color:#666;">
        Unggah file XLSX, XLS, CSV untuk menghasilkan dashboard otomatis
    </p>
</div>
""", unsafe_allow_html=True)

# FILE UPLOADER
uploaded_file = st.file_uploader(
    "Upload atau seret file ke sini",
    type=["xlsx", "xls", "csv"]
)

# INFO BOX
st.info(
    "Kolom yang dianalisis otomatis: "
    "Sumber Informasi • Jenjang Pendidikan • Provinsi • Tanggal Daftar"
)

# TARGET PENDAFTAR
target_pendaftar = st.number_input(
    "Target Pendaftar",
    min_value=1,
    value=1000,
    step=100
)

# PROCESS FILE
if uploaded_file is not None:

    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(
            f"File berhasil diunggah ({len(df)} baris data)"
        )

        st.session_state["data"] = df

        st.subheader("Preview Data")

        st.dataframe(
            df.head(),
            use_container_width=True,
            hide_index=True
        )

        if st.button(
            "Generate Dashboard",
            use_container_width=True,
            type="primary"
        ):
            st.session_state["data"] = df
            st.session_state["file_name"] = uploaded_file.name
            st.session_state["target"] = target_pendaftar
            st.switch_page("pages/analytics.py")

    except Exception as e:
        st.error(f"Gagal membaca file: {e}")