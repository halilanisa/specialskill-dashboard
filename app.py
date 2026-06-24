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
    background:#EEF2F7;
}}

.block-container {{
    max-width:700px;
    padding-top:40px;
}}

.logo {{
    text-align:center;
    margin-bottom:10px;
}}

.logo img {{
    width:340px;
}}

.title {{
    text-align:center;
    color:#0B2B6B;
    font-size:22px;
    font-weight:700;
    margin-bottom:5px;
}}

.subtitle {{
    text-align:center;
    color:#6B7280;
    font-size:16px;
    margin-bottom:35px;
}}

div[data-testid="stTextInputRootElement"] {{
    border:1px solid #D1D5DB !important;
    border-radius:12px !important;
    background:#F3F4F6 !important;
    min-height:56px !important;
}}

div[data-testid="stTextInputRootElement"]:focus-within {{
    border:1px solid #0B2B6B !important;
}}

.stTextInput label {{
    font-size:16px !important;
    font-weight:600 !important;
    color:#374151 !important;
}}

.stTextInput input {{
    height:56px !important;
    line-height:56px !important;
    padding:0 16px !important;
    border:none !important;
    background:#F3F4F6 !important;
    color:#111827 !important;
    box-shadow:none !important;
}}

.stTextInput button {{
    border:none !important;
    background:#F3F4F6 !important;
}}

.stTextInput button:hover {{
    background:#F3F4F6 !important;
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
    margin-top:10px;
}}

.stButton button {{
    width:100% !important;
    height:56px !important;
    min-height:56px !important;
    border:none !important;
    border-radius:12px !important;
    background:#0B2B6B !important;
    color:white !important;
    font-size:17px !important;
    font-weight:600 !important;
}}

.stButton button:hover {{
    background:#1847A3 !important;
    color:white !important;
}}

.footer {{
    text-align:center;
    margin-top:30px;
    color:#6B7280;
    font-size:14px;
}}

</style>

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