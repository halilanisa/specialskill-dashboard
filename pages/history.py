import streamlit as st
import base64
import time
from database import (
    get_history,
    load_dashboard,
    delete_dashboard
)

st.set_page_config(
    page_title="Dashboard Analiti",
    page_icon="logo.png",
    layout="wide"
)

st.markdown("""
<style>

.stApp{
    background:white !important;
}

[data-testid="stAppViewContainer"]{
    background:white !important;
}

header,
footer,
#MainMenu{
    visibility:hidden;
}

[data-testid="stSidebar"]{
    display:none;
}

.block-container{
    padding-top:1rem;
    max-width:100%;
}

.stButton button{
    border-radius:10px;
    font-weight:600;
}

</style>
""", unsafe_allow_html=True)

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64_image("specialskill.png")

col1, col2 = st.columns([9,1])

with col1:

    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:20px;">
        <img src="data:image/png;base64,{logo}" width="140">
        <span style="
            font-size:22px;
            font-weight:700;
            color:#0A2463;">
            Dashboard Analitik
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:

    if st.button(
        "",
        icon=":material/arrow_back:",
        use_container_width=True,
        help="Kembali"
    ):
        st.switch_page("pages/dashboard.py")

st.markdown("""
<hr style="
margin-top:10px;
margin-bottom:20px;
">
""", unsafe_allow_html=True)

history = get_history()

if history.empty:

    st.info(
        "Belum ada dashboard yang disimpan"
    )

    st.stop()

st.subheader("Daftar Dashboard")

for _, row in history.iterrows():

    with st.container(border=True):

        c1, c2 = st.columns([5, 2])

        with c1:

            st.markdown(f"""
            **{row['event_name']}**

            File : {row['file_name']}

            Periode : {row['periode']}

            Target : {row['target']}

            Total Pendaftar : {row['total_pendaftar']}

            Disimpan pada : {row['created_at']}
            """)

        with c2:

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

            if st.button(
                "Hapus",
                key=f"delete_{row['id']}",
                use_container_width=True,
                type="secondary"
            ):

                delete_dashboard(row["id"])
                st.rerun()