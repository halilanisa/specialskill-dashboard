import streamlit as st
import pandas as pd
import plotly.express as px
import base64

# CONFIG
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="logo.png",
    layout="wide"
)

# CEK DATA
if "data" not in st.session_state:
    st.session_state.clear()
    st.switch_page("pages/dashboard.py")
    st.stop()

df = st.session_state["data"].copy()

# CSS
st.markdown("""
<style>

.stApp{
    background:white !important;
}

[data-testid="stAppViewContainer"]{
    background:white !important;
}

#MainMenu,
footer,
header{
    visibility:hidden;
}

[data-testid="stSidebar"]{
    display:none;
}

.block-container{
    padding-top:1rem;
    max-width:100%;
}

.card{
    border-radius:20px;
    padding:20px;
    color:white;
    text-align:center;
    box-shadow:0 2px 8px rgba(0,0,0,0.15);
}

div[data-testid="stMarkdownContainer"] p{
    margin:0;
}

</style>
""", unsafe_allow_html=True)

# LOGO
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64_image("specialskill.png")

# HEADER
col1,col2,col3 = st.columns([8,2,1])

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
    if st.button("Ganti File", use_container_width=True):
        st.switch_page("pages/dashboard.py")

with col3:
    if st.button("Keluar", use_container_width=True):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown("""
<hr style="
    margin-top:5px;
    margin-bottom:10px;
">
""", unsafe_allow_html=True)

# PREPROCESS
if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

# KPI
total_pendaftar = len(df)

target = st.session_state.get(
    "target",
    1000
)

persen = round(
    (total_pendaftar / target) * 100,
    1
)

# event name otomatis
if "event_name" in df.columns:
    event_name = str(df["event_name"].iloc[0])
else:
    event_name = "EVENT"

# periode otomatis
if "timestamp" in df.columns:

    start_date = df["timestamp"].min()
    end_date = df["timestamp"].max()

    periode = (
        start_date.strftime("%d %b %Y")
        + " - " +
        end_date.strftime("%d %b %Y")
    )

else:
    periode = "-"

CARD_HEIGHT = 150

st.markdown(
    f"""
    <div style="background:#4A82E8;border-radius:20px;padding:25px;text-align:center;color:white;margin-bottom:15px;">
        <h1>DASHBOARD PENDAFTARAN<br>{event_name.upper()}</h1>
        <p style="font-size:20px;">Periode: {periode}</p>
    </div>
    """,
    unsafe_allow_html=True
)

CARD_HEIGHT = 120

c1, c2, c3 = st.columns(3)

with c1:
    st.container(border=False)
    st.markdown("""
    <div style="
    background:#F4B400;
    border-radius:20px;
    padding:3px;
    text-align:center;
    color:white;">
        <h4 style="margin:0;">Target Peserta</h4>
        <h1 style="margin:3px 0 0 0;">{}</h1>
    </div>
    """.format(f"{target:,}"), unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div style="
    background:#10B981;
    border-radius:20px;
    padding:3px;
    text-align:center;
    color:white;">
        <h4 style="margin:0;">Total Pendaftar</h4>
        <h1 style="margin:3px 0 0 0;">{}</h1>
    </div>
    """.format(total_pendaftar), unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div style="
    background:#FF6F00;
    border-radius:20px;
    padding:3px;
    text-align:center;
    color:white;">
        <h4 style="margin:0;">Capaian Target</h4>
        <h1 style="margin:3px 0 0 0;">{}%</h1>
    </div>
    """.format(persen), unsafe_allow_html=True)

st.write("")

# FILE NAME
file_name = st.session_state.get(
    "file_name",
    "File tidak diketahui"
)

st.markdown(
    f"**Sumber Data:** {file_name}"
)

# SUMBER INFORMASI
left,right = st.columns(2)

with left:

    if "source_info" in df.columns:

        all_sources = [
            "Instagram",
            "WhatssApp",
            "Tiktok",
            "Teman",
            "LinkedIn",
            "Twitter",
            "Website",
            "Iklan"
        ]

        source_count = (
            df["source_info"]
            .astype(str)
            .str.strip()
            .value_counts()
            .reset_index()
        )

        source_count.columns = [
            "Sumber",
            "Jumlah"
        ]

        source = pd.DataFrame({
            "Sumber": all_sources
        })

        source = source.merge(
            source_count,
            on="Sumber",
            how="left"
        )

        source["Jumlah"] = (
            source["Jumlah"]
            .fillna(0)
            .astype(int)
        )

        fig_source = px.bar(
            source,
            x="Sumber",
            y="Jumlah",
            text="Jumlah",
            color="Sumber",
            title="Sumber Informasi"
        )

        fig_source.update_traces(
            textposition="outside"
        )

        fig_source.update_layout(
            xaxis_title="Sumber Informasi",
            yaxis_title="Jumlah Pendaftar",
            showlegend=False
        )

        st.plotly_chart(
            fig_source,
            use_container_width=True
        )

with right:

    if "jenjang_pendidikan" in df.columns:

        pendidikan = (
            df["jenjang_pendidikan"]
            .fillna("Tidak diketahui")
            .value_counts()
            .reset_index()
        )

        pendidikan.columns = [
            "Jenjang",
            "Jumlah"
        ]

        fig_pie = px.pie(
            pendidikan,
            names="Jenjang",
            values="Jumlah",
            hole=0,
            title="Jenjang Pendidikan"
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

# GRAFIK PENDAFTARAN HARIAN
if (
    "timestamp" in df.columns and
    "source_info" in df.columns
):

    valid_sources = [
        "Instagram",
        "WhatssApp",
        "Tiktok",
        "Teman",
        "LinkedIn",
        "Twitter",
        "Website",
        "Iklan"
    ]

    trend = df.copy()

    trend["Tanggal"] = pd.to_datetime(
        trend["timestamp"],
        format="mixed",
        errors="coerce"
    )

    trend = trend.dropna(
        subset=["Tanggal"]
    )

    trend["Tanggal"] = trend["Tanggal"].dt.date

    trend["source_info"] = (
        trend["source_info"]
        .astype(str)
        .str.strip()
    )

    trend = trend[
        trend["source_info"].isin(valid_sources)
    ]

    if len(trend) > 0:

        min_date = pd.to_datetime(
            trend["Tanggal"].min()
        )

        max_date = pd.to_datetime(
            trend["Tanggal"].max()
        )

        all_dates = pd.date_range(
            start=min_date,
            end=max_date,
            freq="D"
        )

        day_labels = [
            f"Day {i+1}"
            for i in range(len(all_dates))
        ]

        day_date_df = pd.DataFrame({
            "Hari": day_labels,
            "Tanggal": all_dates.date
        })

        source_df = pd.DataFrame({
            "source_info": valid_sources
        })

        all_combinations = (
            day_date_df.assign(key=1)
            .merge(
                source_df.assign(key=1),
                on="key"
            )
            .drop(
                "key",
                axis=1
            )
        )

        day_mapping = dict(
            zip(
                all_dates.date,
                day_labels
            )
        )

        trend["Hari"] = trend["Tanggal"].map(
            day_mapping
        )

        trend = (
            trend.groupby(
                [
                    "Hari",
                    "Tanggal",
                    "source_info"
                ]
            )
            .size()
            .reset_index(name="Jumlah")
        )

        trend = all_combinations.merge(
            trend,
            on=[
                "Hari",
                "Tanggal",
                "source_info"
            ],
            how="left"
        )

        trend["Jumlah"] = (
            trend["Jumlah"]
            .fillna(0)
            .astype(int)
        )

        trend["Tanggal_Display"] = pd.to_datetime(
            trend["Tanggal"]
        ).dt.strftime(
            "%d %b %Y"
        )

        fig_trend = px.bar(
            trend,
            x="Hari",
            y="Jumlah",
            color="source_info",
            title="Grafik Pendaftaran",
            barmode="stack",
            category_orders={
                "Hari": day_labels
            },
            custom_data=[
                "Tanggal_Display"
            ]
        )

        fig_trend.update_traces(
            hovertemplate=
            "%{fullData.name}= %{y}" +
            "<extra></extra>"
        )

        fig_trend.update_layout(
            xaxis_title="Periode Pendaftaran",
            yaxis_title="Jumlah Pendaftar",
            legend_title="Sumber Informasi",
            hovermode="x unified"
        )

        st.plotly_chart(
            fig_trend,
            use_container_width=True
        )

# PROVINSI
if "provinsi" in df.columns:

    all_provinces = [
        "Jawa Barat",
        "Jawa Timur",
        "Jawa Tengah",
        "DKI Jakarta",
        "Daerah Istimewa Yogyakarta",
        "Sulawesi Selatan",
        "Banten",
        "Sumatera Utara",
        "Bali",
        "Sumatera Selatan",
        "Sumatera Barat",
        "Riau",
        "Lampung",
        "Kalimantan Timur",
        "Sulawesi Tengah",
        "Sulawesi Tenggara",
        "Maluku",
        "Nanggroe Aceh Darussalam",
        "Jambi",
        "Kalimantan Selatan",
        "Kepulauan Riau",
        "Nusa Tenggara Barat",
        "Kalimantan Barat",
        "Sulawesi Utara",
        "Nusa Tenggara Timur",
        "Kalimantan Tengah",
        "Bengkulu",
        "Maluku Utara",
        "Sulawesi Barat",
        "Papua",
        "Bangka Belitung",
        "Kalimantan Utara",
        "Gorontalo",
        "Papua Barat",
        "Papua Tengah",
        "Papua Pegunungan",
        "Papua Selatan",
        "Papua Barat Daya",
        "Luar Negeri"
    ]

    prov_count = (
        df["provinsi"]
        .fillna("Tidak diketahui")
        .value_counts()
        .reset_index()
    )

    prov_count.columns = ["Provinsi", "Jumlah"]

    prov = pd.DataFrame({
        "Provinsi": all_provinces
    })

    prov = prov.merge(
        prov_count,
        on="Provinsi",
        how="left"
    )

    prov["Jumlah"] = (
        prov["Jumlah"]
        .fillna(0)
        .astype(int)
    )

    prov = prov.sort_values(
        "Jumlah",
        ascending=False
    )

    fig_prov = px.bar(
        prov,
        x="Provinsi",
        y="Jumlah",
        color="Jumlah",
        text="Jumlah",
        title="Sebaran Pendaftar"
    )

    fig_prov.update_traces(
        textposition="outside"
    )

    fig_prov.update_layout(
        height=600,
        xaxis_title="Provinsi",
        yaxis_title="Jumlah Pendaftar",
        xaxis_tickangle=-90,
        xaxis=dict(
            categoryorder="array",
            categoryarray=prov["Provinsi"].tolist()
        )
    )

    st.plotly_chart(
        fig_prov,
        use_container_width=True
    )

# RAW DATA
with st.expander("Lihat Data Lengkap"):
    st.dataframe(
        df,
        use_container_width=True
    )