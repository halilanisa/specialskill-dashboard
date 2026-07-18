import streamlit as st
import base64

st.set_page_config(
    page_title="Special Skill Dashboard",
    page_icon="logo.png",
    layout="centered"
)

USERNAME = "DataAnalyst"
PASSWORD = "specialskill.id"

def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64_image("specialskill.png")

st.markdown(f"""
<style>

#MainMenu,
footer,
header {{
    visibility:hidden;
}}

.stApp {{
    background:#F4F7FC;
}}

.block-container {{
    max-width:620px;
    padding-top:70px;
}}

/* ---------- Login card ---------- */
div[class*="st-key-login_card"]{{
    background:#FFFFFF;
    border-radius:24px;
    padding:44px 44px 34px 44px;
    box-shadow:0 16px 40px rgba(15,23,42,.08);
    border:1px solid #EEF1F7;
}}

.eyebrow {{
    text-align:center;
    font-size:12px;
    font-weight:700;
    letter-spacing:3px;
    color:#4A82E8;
    text-transform:uppercase;
    margin-bottom:14px;
}}

.logo {{
    text-align:center;
    margin-bottom:8px;
}}

.logo img {{
    width:270px;
}}

.title {{
    text-align:center;
    color:#0B2B6B;
    font-size:24px;
    font-weight:800;
    margin-bottom:6px;
    margin-top:6px;
}}

.subtitle {{
    text-align:center;
    color:#8794A8;
    font-size:15px;
    margin-bottom:34px;
}}

div[data-testid="stTextInputRootElement"] {{
    border:1px solid #E2E6ED !important;
    border-radius:12px !important;
    background:#F7F9FC !important;
    min-height:56px !important;
    transition:border-color .15s ease, box-shadow .15s ease;
}}

div[data-testid="stTextInputRootElement"]:focus-within {{
    border:1px solid #4A82E8 !important;
    box-shadow:0 0 0 3px rgba(74,130,232,.15) !important;
}}

.stTextInput label {{
    font-size:13.5px !important;
    font-weight:700 !important;
    letter-spacing:.3px;
    color:#5A6B85 !important;
    text-transform:uppercase;
}}

.stTextInput input {{
    height:56px !important;
    line-height:56px !important;
    padding:0 16px !important;
    border:none !important;
    background:#F7F9FC !important;
    color:#111827 !important;
    box-shadow:none !important;
}}

.stTextInput button {{
    border:none !important;
    background:#F7F9FC !important;
}}

.stTextInput button:hover {{
    background:#F7F9FC !important;
}}

.stTextInput button svg {{
    color:#0B2B6B !important;
    fill:#0B2B6B !important;
}}

.stTextInput button:hover svg {{
    color:#1847A3 !important;
    fill:#1847A3 !important;
}}

.stTextInput input::placeholder {{
    line-height:56px !important;
    color:#9CA3AF !important;
}}

.stButton {{
    width:100%;
    margin-top:14px;
}}

.stButton button {{
    width:100% !important;
    height:56px !important;
    min-height:56px !important;
    border:none !important;
    border-radius:12px !important;
    background:linear-gradient(90deg,#0B2B6B,#3167E0) !important;
    color:white !important;
    font-size:16.5px !important;
    font-weight:700 !important;
    letter-spacing:.2px;
    box-shadow:0 10px 22px rgba(23,62,147,.28) !important;
}}

.stButton button:hover {{
    background:linear-gradient(90deg,#0A2560,#2857C7) !important;
    color:white !important;
    box-shadow:0 12px 26px rgba(23,62,147,.36) !important;
}}

.footer {{
    text-align:center;
    margin-top:26px;
    color:#9AA6B8;
    font-size:13.5px;
}}

</style>
""", unsafe_allow_html=True)

with st.container(key="login_card"):

    st.markdown(f"""
    <div class="eyebrow">Special Skill Workspace</div>

    <div class="logo">
        <img src="data:image/png;base64,{logo}">
    </div>

    <div class="title">
        Dashboard Login
    </div>

    <div class="subtitle">
        Masuk untuk mengakses dashboard analitik
    </div>
    """, unsafe_allow_html=True)

    username = st.text_input(
        "Username",
        placeholder="Masukkan username"
    )

    password = st.text_input(
        "Password",
        placeholder="Masukkan password",
        type="password"
    )

    if st.button("Masuk", use_container_width=True):

        if username == USERNAME and password == PASSWORD:
            st.session_state["logged_in"] = True
            st.switch_page("pages/dashboard.py")
        else:
            st.error("Username atau password salah")

st.markdown("""
<div class="footer">
© 2026 Special Skill — Data Analyst
</div>
""", unsafe_allow_html=True)