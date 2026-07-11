import streamlit as st
from supabase import create_client, Client


@st.cache_resource(show_spinner=False)
def get_client() -> Client:
    try:
        url = st.secrets["SUPABASE_URL"]
        key = st.secrets["SUPABASE_KEY"]
    except (KeyError, FileNotFoundError):
        st.error(
            "SUPABASE_URL / SUPABASE_KEY belum diatur di secrets. "
            "Lihat README_SUPABASE.md untuk cara setting-nya."
        )
        st.stop()

    return create_client(url, key)
