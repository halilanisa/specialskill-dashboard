import streamlit as st
import pandas as pd
import plotly.express as px
import base64
import textwrap

# CONFIG
st.set_page_config(
    page_title="Dashboard Analitik",
    page_icon="logo.png",
    layout="wide"
)

# CEK DATA
if "data" not in st.session_state:
    st.session_state.clear()
    st.switch_page("pages/dashboard.py")
    st.stop()

df = st.session_state["data"].copy()

if "timestamp" in df.columns:
    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )

if "saved" not in st.session_state:
    st.session_state.saved = False

# CSS
st.markdown("""
<style>

.stApp{
    background:#F4F7FC !important;
}

[data-testid="stAppViewContainer"]{
    background:#F4F7FC !important;
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
    padding-bottom:2.5rem;
    max-width:1180px;
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

/* Header buttons (kembali / keluar) */
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

</style>
""", unsafe_allow_html=True)

# LOGO
def get_base64_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

logo = get_base64_image("specialskill.png")

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

event_name = st.session_state.get("event_name", "EVENT")

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

file_name = st.session_state.get(
    "file_name",
    "File tidak diketahui"
)

# HEADER
col1, col2, col3 = st.columns([10, 1, 1])

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
        icon=":material/arrow_back:",
        use_container_width=True
    ):
        st.switch_page("pages/dashboard.py")

with col3:
    if st.button(
        "",
        icon=":material/logout:",
        use_container_width=True
    ):
        st.session_state.clear()
        st.switch_page("app.py")

st.markdown("""
<hr style="
    margin-top:5px;
    margin-bottom:10px;
">
""", unsafe_allow_html=True)

st.markdown(
f"""
<div style="
background:#ffffff;
border-radius:22px;
padding:30px 40px;
margin-bottom:22px;
border-top:7px solid #4A82E8;
box-shadow:0 12px 30px rgba(15,23,42,.08);
text-align:center;
">

<div style="
font-size:12.5px;
font-weight:700;
color:#4A82E8;
letter-spacing:3px;
text-transform:uppercase;
margin-bottom:12px;">
Dashboard Pendaftaran
</div>

<div style="
font-size:38px;
font-weight:800;
color:#0B2B6B;
letter-spacing:-.5px;
margin-bottom:14px;">
{event_name}
</div>

<div style="
display:inline-block;
padding:8px 18px;
background:#F5F9FF;
border-radius:999px;
font-size:16px;
color:#5A6B8C;
border:1px solid #D8E7FF;">
<b>Periode:</b> {periode}
</div>

</div>
""",
unsafe_allow_html=True
)

c1, c2, c3 = st.columns(3)

def metric_card(title, value, gradient):
    return f"""
<div style="
background:{gradient};
border-radius:18px;
padding:24px;
box-shadow:0 10px 26px rgba(15,23,42,.16);
height:150px;
display:flex;
flex-direction:column;
justify-content:center;
align-items:center;
text-align:center;
color:#ffffff;
">

<div style="
color:#ffffff;
opacity:.85;
font-size:12.5px;
font-weight:700;
letter-spacing:1px;
text-transform:uppercase;">
{title}
</div>

<div style="
margin:14px 0 0 0;
color:#ffffff;
font-size:38px;
font-weight:800;">
{value}
</div>

</div>
"""

with c1:
    st.markdown(
        metric_card(
            "Target Peserta",
            f"{target:,}",
            "linear-gradient(135deg,#F4A100,#C9720A)"
        ),
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        metric_card(
            "Total Pendaftar",
            f"{total_pendaftar:,}",
            "linear-gradient(135deg,#0EA5A0,#0B7A87)"
        ),
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        metric_card(
            "Capaian Target",
            f"{persen:.1f}%",
            "linear-gradient(135deg,#0B2B6B,#2F5FD6)"
        ),
        unsafe_allow_html=True
    )

st.write("")
st.markdown(
    f'<span style="color:#7A8699;font-size:14px;">'
    f'<b style="color:#5A6B85;">Sumber Data:</b> {file_name}</span>',
    unsafe_allow_html=True
)

# SUMBER INFORMASI
left,right = st.columns(2)

with left:

    if "source_info" in df.columns:

        all_sources = [
            "Instagram",
            "WhatsApp",
            "TikTok",
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
            .replace({
                "WhatssApp": "WhatsApp",
                "Tiktok": "TikTok"
            })
            .value_counts()
            .reset_index()
        )

        source_count.columns = ["Sumber", "Jumlah"]

        source = pd.DataFrame({"Sumber": all_sources})

        source = source.merge(source_count, on="Sumber", how="left")
        source["Jumlah"] = source["Jumlah"].fillna(0).astype(int)

        colors = [
            "#4A82E8", "#10B981", "#F4B400", "#FF6B81",
            "#8B5CF6", "#06B6D4", "#F97316", "#EF4444"
        ]

        fig_source = px.bar(
            source,
            x="Sumber",
            y="Jumlah",
            color="Sumber",
            text="Jumlah",
            color_discrete_sequence=colors
        )

        fig_source.update_traces(
            textposition="outside",
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>%{y} Peserta<extra></extra>"
        )

        fig_source.update_layout(
            height=360,
            showlegend=False,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family="Segoe UI", color="#334155", size=13),
            xaxis=dict(title="", showgrid=False, tickangle=-25),
            yaxis=dict(title="Jumlah Peserta", gridcolor="#E8EDF5", zeroline=False)
        )

        st.markdown(textwrap.dedent("""
        <style>
        div[class*="st-key-card_source"] {
            background:white;
            border-radius:22px;
            padding:24px 26px 20px 26px;
            box-shadow:0 10px 25px rgba(15,23,42,.08);
            border:1px solid #EEF2F7;
        }
        </style>
        """), unsafe_allow_html=True)

        with st.container(key="card_source"):

            st.markdown(textwrap.dedent("""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <div>
                    <div style="font-size:20px;font-weight:700;color:#1E293B;">
                        Sumber Informasi
                    </div>
                    <div style="font-size:14px;color:#64748B;margin-top:4px;">
                        Media yang membawa peserta melakukan pendaftaran
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.plotly_chart(
                fig_source,
                use_container_width=True,
                config={
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "zoom", "pan", "lasso2d", "select2d",
                        "autoScale", "resetScale2d"
                    ]
                }
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

        colors_pie = [
            "#4A82E8",
            "#10B981",
            "#F4B400",
            "#FF6B81",
            "#8B5CF6",
            "#06B6D4",
            "#F97316",
            "#EF4444"
        ]

        fig_pie = px.pie(
            pendidikan,
            names="Jenjang",
            values="Jumlah",
            hole=0,
            color_discrete_sequence=colors_pie
        )

        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent",
            hovertemplate="<b>%{label}</b><br>%{value} Peserta<extra></extra>"
        )

        fig_pie.update_layout(
            height=360,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family="Segoe UI", color="#334155", size=13),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.02
            )
        )

        st.markdown(textwrap.dedent("""
        <style>
        div[class*="st-key-card_pendidikan"] {
            background:white;
            border-radius:22px;
            padding:24px 26px 20px 26px;
            box-shadow:0 10px 25px rgba(15,23,42,.08);
            border:1px solid #EEF2F7;
        }
        </style>
        """), unsafe_allow_html=True)

        with st.container(key="card_pendidikan"):

            st.markdown(textwrap.dedent("""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <div>
                    <div style="font-size:20px;font-weight:700;color:#1E293B;">
                        Jenjang Pendidikan
                    </div>
                    <div style="font-size:14px;color:#64748B;margin-top:4px;">
                        Latar belakang pendidikan peserta yang mendaftar
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.plotly_chart(
                fig_pie,
                use_container_width=True,
                config={
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "zoom", "pan", "lasso2d", "select2d",
                        "autoScale", "resetScale2d"
                    ]
                }
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

        daily_total = (
            trend.groupby("Hari")["Jumlah"]
            .sum()
            .reindex(day_labels)
            .reset_index()
        )

        daily_total.columns = ["Hari", "Total"]

        colors_trend = [
            "#4A82E8",
            "#10B981",
            "#F4B400",
            "#FF6B81",
            "#8B5CF6",
            "#06B6D4",
            "#F97316",
            "#EF4444"
        ]

        fig_trend = px.bar(
            trend,
            x="Hari",
            y="Jumlah",
            color="source_info",
            barmode="stack",
            category_orders={
                "Hari": day_labels
            },
            custom_data=["Tanggal_Display"],
            color_discrete_sequence=colors_trend
        )

        fig_trend.update_traces(
            hovertemplate="%{fullData.name}= %{y}<extra></extra>",
            marker_line_width=0
        )

        import plotly.graph_objects as go

        fig_trend.add_trace(
            go.Scatter(
                x=daily_total["Hari"],
                y=[0] * len(daily_total),
                mode="markers",
                marker=dict(opacity=0),
                name="Total Pendaftar",
                customdata=daily_total["Total"],
                hovertemplate="<b>Total = %{customdata}</b><extra></extra>",
                showlegend=False
            )
        )

        fig_trend.update_layout(
            height=380,
            showlegend=True,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=10, r=10, t=10, b=10),
            font=dict(family="Segoe UI", color="#334155", size=13),
            xaxis=dict(title="Periode Pendaftaran", showgrid=False),
            yaxis=dict(title="Jumlah Pendaftar", gridcolor="#E8EDF5", zeroline=False),
            legend_title="Sumber Informasi",
            hovermode="x unified"
        )

        st.markdown(textwrap.dedent("""
        <style>
        div[class*="st-key-card_trend"] {
            background:white;
            border-radius:22px;
            padding:24px 26px 20px 26px;
            box-shadow:0 10px 25px rgba(15,23,42,.08);
            border:1px solid #EEF2F7;
        }
        </style>
        """), unsafe_allow_html=True)

        with st.container(key="card_trend"):

            st.markdown(textwrap.dedent("""
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <div>
                    <div style="font-size:20px;font-weight:700;color:#1E293B;">
                        Grafik Pendaftaran
                    </div>
                    <div style="font-size:14px;color:#64748B;margin-top:4px;">
                        Tren jumlah pendaftar harian berdasarkan sumber informasi
                    </div>
                </div>
            </div>
            """), unsafe_allow_html=True)

            st.plotly_chart(
                fig_trend,
                use_container_width=True,
                config={
                    "displaylogo": False,
                    "modeBarButtonsToRemove": [
                        "zoom", "pan", "lasso2d", "select2d",
                        "autoScale", "resetScale2d"
                    ]
                }
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
        color_continuous_scale=[
            "#DCE8FF",
            "#4A82E8"
        ]
    )

    fig_prov.update_traces(
        textposition="outside",
        marker_line_width=0,
        hovertemplate="<b>%{x}</b><br>%{y} Peserta<extra></extra>"
    )

    fig_prov.update_layout(
        height=600,
        showlegend=False,
        coloraxis_showscale=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Segoe UI", color="#334155", size=13),
        xaxis=dict(
            title="Provinsi",
            showgrid=False,
            tickangle=-90,
            categoryorder="array",
            categoryarray=prov["Provinsi"].tolist()
        ),
        yaxis=dict(
            title="Jumlah Pendaftar",
            gridcolor="#E8EDF5",
            zeroline=False
        )
    )

    st.markdown(textwrap.dedent("""
    <style>
    div[class*="st-key-card_provinsi"] {
        background:white;
        border-radius:22px;
        padding:24px 26px 20px 26px;
        box-shadow:0 10px 25px rgba(15,23,42,.08);
        border:1px solid #EEF2F7;
    }
    </style>
    """), unsafe_allow_html=True)

    with st.container(key="card_provinsi"):

        st.markdown(textwrap.dedent("""
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
            <div>
                <div style="font-size:20px;font-weight:700;color:#1E293B;">
                    Sebaran Pendaftar
                </div>
                <div style="font-size:14px;color:#64748B;margin-top:4px;">
                    Jumlah pendaftar berdasarkan provinsi asal
                </div>
            </div>
        </div>
        """), unsafe_allow_html=True)

        st.plotly_chart(
            fig_prov,
            use_container_width=True,
            config={
                "displaylogo": False,
                "modeBarButtonsToRemove": [
                    "zoom", "pan", "lasso2d", "select2d",
                    "autoScale", "resetScale2d"
                ]
            }
        )

# RAW DATA
st.write("")

with st.expander("Lihat Data Lengkap"):
    st.dataframe(
        df,
        use_container_width=True
    )