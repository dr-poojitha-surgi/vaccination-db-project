import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import date

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="VaccinationDB | Multi-Facility EHR",
    page_icon="💉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# BOTANICAL CLINICAL THEME — Teal × Olive
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Source+Sans+3:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Source Sans 3', sans-serif;
        color: #1c2b25;
    }

    /* ── Main canvas ── */
    .stApp {
        background-color: #f2f5f0;
        background-image:
            radial-gradient(circle at 15% 20%, rgba(45,110,90,0.06) 0%, transparent 50%),
            radial-gradient(circle at 85% 75%, rgba(107,135,75,0.06) 0%, transparent 50%);
    }

    /* ── Sidebar — deep teal-forest gradient ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(175deg, #1a3a32 0%, #243d2f 45%, #2a3d20 100%);
        border-right: none;
        box-shadow: 4px 0 24px rgba(0,0,0,0.18);
    }

    /* Sidebar radio — hide default label */
    section[data-testid="stSidebar"] .stRadio > label {
        display: none;
    }

    /* Sidebar radio items — pill style */
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] {
        gap: 2px;
        display: flex;
        flex-direction: column;
    }

    section[data-testid="stSidebar"] .stRadio label {
        background: transparent;
        border-radius: 10px;
        padding: 10px 16px !important;
        font-size: 0.88rem !important;
        font-family: 'Source Sans 3', sans-serif !important;
        font-weight: 500 !important;
        color: #a8c4b0 !important;
        cursor: pointer;
        transition: all 0.2s ease;
        border: 1px solid transparent;
        display: flex;
        align-items: center;
        gap: 8px;
        letter-spacing: 0.01em;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(78,185,145,0.12) !important;
        color: #c8e6c9 !important;
        border: 1px solid rgba(78,185,145,0.2);
    }

    section[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] input:checked + div {
        background: #2DD4BF;
    }

    /* Active/selected nav item */
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] + label,
    section[data-testid="stSidebar"] .stRadio label:has(input:checked) {
        background: linear-gradient(90deg, rgba(45,212,191,0.18), rgba(107,135,75,0.12)) !important;
        color: #ffffff !important;
        border: 1px solid rgba(45,212,191,0.35) !important;
        box-shadow: 0 2px 10px rgba(45,212,191,0.12);
    }

    /* Radio button dot — teal */
    section[data-testid="stSidebar"] .stRadio [data-baseweb="radio"] div {
        border-color: #4EB991 !important;
    }
    section[data-testid="stSidebar"] .stRadio [aria-checked="true"] [data-baseweb="radio"] div {
        background: #2DD4BF !important;
        border-color: #2DD4BF !important;
    }

    /* Sidebar scrollbar */
    section[data-testid="stSidebar"]::-webkit-scrollbar { width: 4px; }
    section[data-testid="stSidebar"]::-webkit-scrollbar-track { background: transparent; }
    section[data-testid="stSidebar"]::-webkit-scrollbar-thumb { background: #4EB991; border-radius: 4px; }

    /* ── Headings ── */
    h1 {
        font-family: 'Playfair Display', serif !important;
        color: #1a3a32 !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        letter-spacing: -0.02em;
    }
    h2, h3 {
        font-family: 'Playfair Display', serif !important;
        color: #1d4d3a !important;
        font-weight: 600 !important;
    }

    /* ── Section headers ── */
    .section-header {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: #5a8c6e;
        text-transform: uppercase;
        letter-spacing: 2.5px;
        border-bottom: 1.5px solid #b8d4bc;
        padding-bottom: 7px;
        margin-bottom: 18px;
        margin-top: 10px;
    }

    /* ── KPI Cards ── */
    .kpi-card {
        background: linear-gradient(135deg, #ffffff 60%, #f0f7f2);
        border: 1px solid #c8dece;
        border-top: 4px solid #2DD4BF;
        border-radius: 12px;
        padding: 20px 22px;
        margin-bottom: 12px;
        box-shadow: 0 3px 12px rgba(26,58,50,0.07);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(26,58,50,0.12);
    }
    .kpi-card h2 {
        font-family: 'Playfair Display', serif !important;
        font-size: 2.4rem !important;
        margin: 6px 0 0 0 !important;
        color: #1a3a32 !important;
        font-weight: 700 !important;
        letter-spacing: -0.03em;
    }
    .kpi-card p {
        margin: 0;
        color: #6b8c76;
        font-size: 0.74rem;
        text-transform: uppercase;
        letter-spacing: 1.4px;
        font-family: 'JetBrains Mono', monospace;
    }

    /* ── SQL display box ── */
    .sql-box {
        background: #f0f7f2;
        border: 1px solid #b8d4bc;
        border-left: 4px solid #4EB991;
        border-radius: 8px;
        padding: 12px 16px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #1d4d3a;
        white-space: pre-wrap;
        margin-bottom: 14px;
        line-height: 1.6;
    }

    /* ── Info banner ── */
    .info-banner {
        background: linear-gradient(135deg, #e8f5ec, #f0f7ec);
        border: 1px solid #b8d4bc;
        border-left: 4px solid #6B8748;
        border-radius: 10px;
        padding: 14px 20px;
        color: #1d4d3a;
        font-size: 0.9rem;
        margin-bottom: 18px;
        line-height: 1.6;
    }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] {
        background: #e8f0e8;
        border-radius: 10px;
        padding: 4px;
        gap: 2px;
        border: 1px solid #c8dece;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        font-family: 'Source Sans 3', sans-serif;
        font-weight: 500;
        color: #4a7060;
        padding: 8px 18px;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #1a3a32, #2d5a3d) !important;
        color: #ffffff !important;
    }

    /* ── Dataframe ── */
    .stDataFrame {
        border-radius: 10px;
        border: 1px solid #c8dece;
        overflow: hidden;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(135deg, #1d4d3a, #2d6b4a);
        color: #ffffff;
        border: none;
        border-radius: 8px;
        font-family: 'Source Sans 3', sans-serif;
        font-weight: 600;
        letter-spacing: 0.03em;
        padding: 8px 20px;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(26,58,50,0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2DD4BF, #4EB991);
        color: #0d2b22;
        box-shadow: 0 4px 14px rgba(45,212,191,0.3);
        transform: translateY(-1px);
    }

    /* ── Selectbox & inputs ── */
    .stSelectbox > div > div {
        border-color: #b8d4bc !important;
        border-radius: 8px !important;
        background: #ffffff;
    }
    .stTextInput > div > div > input {
        border-color: #b8d4bc !important;
        border-radius: 8px !important;
    }
    .stTextArea > div > div > textarea {
        border-color: #b8d4bc !important;
        border-radius: 8px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
    }

    /* ── Multiselect ── */
    .stMultiSelect > div > div {
        border-color: #b8d4bc !important;
        border-radius: 8px !important;
    }

    /* ── Divider ── */
    hr { border-color: #c8dece; margin: 20px 0; }

    /* ── Download button ── */
    .stDownloadButton > button {
        background: #f0f7f2;
        color: #1d4d3a;
        border: 1px solid #4EB991;
        border-radius: 8px;
        font-family: 'Source Sans 3', sans-serif;
        font-weight: 500;
    }
    .stDownloadButton > button:hover {
        background: #4EB991;
        color: #ffffff;
    }

    /* ── Success/warning/error alerts ── */
    .stSuccess { border-radius: 8px; }
    .stWarning { border-radius: 8px; }
    .stError   { border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# DATABASE CONNECTION
# ─────────────────────────────────────────────
@st.cache_resource
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="12345",   # ← replace with your MySQL password
        database="vaccination_db"
    )

@st.cache_data(ttl=300)
def run_query(sql: str) -> pd.DataFrame:
    conn = get_connection()
    return pd.read_sql(sql, conn)


# ─────────────────────────────────────────────
# PLOTLY LIGHT THEME DEFAULTS
# ─────────────────────────────────────────────
PLOT_THEME = "plotly_white"
PLOT_BG    = "#ffffff"
BLUE_SEQ   = "Teal"
TEAL_SEQ   = "Teal"
COLOR_MAP  = {
    "IU Health Indiana":        "#2DD4BF",
    "Cleveland Clinic Ohio":    "#6B8748",
    "Northwestern Illinois":    "#1a3a32",
    "IN": "#2DD4BF",
    "IL": "#1a3a32",
    "OH": "#6B8748",
}


def plot_defaults(fig, height=380):
    fig.update_layout(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor="#fafcfa",
        font=dict(family="Source Sans 3", color="#1c2b25"),
        height=height,
        margin=dict(t=20, b=20, l=10, r=10),
        xaxis=dict(gridcolor="#e8f0e8", linecolor="#c8dece"),
        yaxis=dict(gridcolor="#e8f0e8", linecolor="#c8dece"),
    )
    return fig


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.markdown("""
<div style='padding: 24px 16px 16px 16px;'>
    <div style='display:flex; align-items:center; gap:10px; margin-bottom:6px;'>
        <div style='font-size:1.6rem; line-height:1;'>💉</div>
        <div>
            <div style='font-family:"Playfair Display",serif; font-weight:700;
                        color:#e8f5ec; font-size:1.05rem; letter-spacing:-0.01em;'>
                VaccinationDB
            </div>
            <div style='font-size:0.65rem; color:#6b9e7e; letter-spacing:1.5px;
                        text-transform:uppercase; font-family:"JetBrains Mono",monospace;'>
                Multi-Facility EHR
            </div>
        </div>
    </div>
    <div style='height:1px; background:linear-gradient(90deg,#2DD4BF,transparent);
                margin: 14px 0 18px 0; opacity:0.5;'></div>
    <div style='font-size:0.65rem; color:#5a8c6e; letter-spacing:1.8px;
                text-transform:uppercase; font-family:"JetBrains Mono",monospace;
                margin-bottom:10px;'>
        Navigation
    </div>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigate", [
    "🏠  Overview",
    "📊  Coverage Analysis",
    "🔍  Patient Lookup",
    "⚠️  CDC Gap Analysis",
    "🏥  Providers & Orgs",
    "📋  Vaccine Guidelines",
    "📈  Tableau Dashboard",
    "🗄️  SQL Query Runner",
])

st.sidebar.markdown("""
<div style='position:fixed; bottom:0; padding:16px;
            background:linear-gradient(0deg,#111f1a,transparent);
            width:inherit; box-sizing:border-box;'>
    <div style='height:1px; background:linear-gradient(90deg,#2DD4BF,transparent);
                margin-bottom:12px; opacity:0.3;'></div>
    <div style='font-size:0.64rem; color:#4a7060; text-align:left;
                font-family:"JetBrains Mono",monospace; line-height:1.8;'>
        GROUP 5 · IU INDIANAPOLIS<br>
        SCI &amp; CLINICAL DATA MGMT<br>
        SP26
    </div>
</div>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════
# PAGE 1 — OVERVIEW
# ═════════════════════════════════════════════
if page == "🏠  Overview":
    st.markdown("# VaccinationDB Dashboard")
    st.markdown("""
    <div class='info-banner'>
    Integrating patient, encounter, and immunization data across
    <b>3 simulated healthcare organizations</b> (Indiana · Illinois · Ohio)
    to identify missed vaccination opportunities using CDC ACIP 2025 guidelines.
    </div>
    """, unsafe_allow_html=True)

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)

    def kpi(col, icon, label, sql):
        try:
            val = run_query(sql).iloc[0, 0]
            col.markdown(
                f"<div class='kpi-card'><p>{icon} {label}</p><h2>{int(val):,}</h2></div>",
                unsafe_allow_html=True
            )
        except Exception as e:
            col.markdown(
                f"<div class='kpi-card'><p>{icon} {label}</p><h2>—</h2></div>",
                unsafe_allow_html=True
            )

    kpi(col1, "👤", "Total Patients",       "SELECT COUNT(*) FROM Patients;")
    kpi(col2, "💉", "Immunization Records", "SELECT COUNT(*) FROM Immunizations;")
    kpi(col3, "🏥", "Encounters",           "SELECT COUNT(*) FROM Encounters;")
    kpi(col4, "🏢", "Organizations",        "SELECT COUNT(*) FROM Organizations;")

    st.markdown("---")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-header'>Patients by Hospital System</div>", unsafe_allow_html=True)
        sql = """
SELECT facility_name AS hospital_system, COUNT(*) AS patients
FROM Patients
GROUP BY facility_name
ORDER BY patients DESC;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="hospital_system", y="patients",
                         color="hospital_system",
                         color_discrete_map=COLOR_MAP,
                         template=PLOT_THEME,
                         labels={"hospital_system": "Hospital System", "patients": "Patients"})
            fig.update_layout(showlegend=False)
            st.plotly_chart(plot_defaults(fig), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")

    with col_b:
        st.markdown("<div class='section-header'>Top 10 Vaccines Administered</div>", unsafe_allow_html=True)
        sql = """
SELECT v.description AS vaccine, COUNT(i.immunization_id) AS count
FROM Immunizations i
JOIN Vaccines v ON i.vaccine_id = v.vaccine_id
GROUP BY v.description
ORDER BY count DESC
LIMIT 10;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="count", y="vaccine", orientation="h",
                         color="count", color_continuous_scale=TEAL_SEQ,
                         template=PLOT_THEME,
                         labels={"count": "Count", "vaccine": ""})
            fig.update_layout(coloraxis_showscale=False,
                              yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_defaults(fig), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")

    st.markdown("---")
    col_c, col_d = st.columns(2)

    with col_c:
        st.markdown("<div class='section-header'>Patients by Gender</div>", unsafe_allow_html=True)
        sql = "SELECT gender, COUNT(*) AS count FROM Patients GROUP BY gender;"
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.pie(df, names="gender", values="count",
                         template=PLOT_THEME,
                         color_discrete_sequence=["#1976D2", "#26A69A", "#EF5350"])
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(plot_defaults(fig, height=320), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")

    with col_d:
        st.markdown("<div class='section-header'>Patients by Race</div>", unsafe_allow_html=True)
        sql = "SELECT race, COUNT(*) AS count FROM Patients GROUP BY race ORDER BY count DESC;"
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="count", y="race", orientation="h",
                         color="count", color_continuous_scale=BLUE_SEQ,
                         template=PLOT_THEME,
                         labels={"count": "Count", "race": ""})
            fig.update_layout(coloraxis_showscale=False,
                              yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_defaults(fig, height=320), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")


# ═════════════════════════════════════════════
# PAGE 2 — COVERAGE ANALYSIS
# ═════════════════════════════════════════════
elif page == "📊  Coverage Analysis":
    st.markdown("# Coverage Analysis")
    st.markdown(
        "<div class='section-header'>Vaccination coverage rates across hospital systems · CDC ACIP 2025</div>",
        unsafe_allow_html=True
    )

    # Filters
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        try:
            systems = run_query(
                "SELECT DISTINCT facility_name FROM Patients ORDER BY facility_name;"
            )["facility_name"].tolist()
        except Exception:
            systems = ["IU Health Indiana", "Cleveland Clinic Ohio", "Northwestern Illinois"]
        selected_systems = st.multiselect("Filter by Hospital System", systems, default=systems)

    system_list = "', '".join(selected_systems) if selected_systems else "''"

    st.markdown("---")

    # Coverage % by vaccine + hospital
    st.markdown("<div class='section-header'>Coverage Rate by Vaccine & Hospital System (%)</div>",
                unsafe_allow_html=True)
    sql = f"""
SELECT
    g.vaccine_name,
    p.facility_name                                          AS hospital_system,
    COUNT(DISTINCT p.patient_id)                             AS eligible_patients,
    COUNT(DISTINCT i.patient_id)                             AS vaccinated_patients,
    ROUND(100.0 * COUNT(DISTINCT i.patient_id) /
          NULLIF(COUNT(DISTINCT p.patient_id), 0), 1)        AS coverage_pct,
    ROUND(100 - (100.0 * COUNT(DISTINCT i.patient_id) /
          NULLIF(COUNT(DISTINCT p.patient_id), 0)), 1)       AS gap_pct
FROM VaccineGuidelines g
JOIN Patients p
    ON TIMESTAMPDIFF(YEAR, p.birthdate, CURDATE())
       BETWEEN g.min_age AND g.max_age
LEFT JOIN Immunizations i
    ON  i.patient_id = p.patient_id
    AND i.vaccine_id = g.vaccine_id
WHERE p.facility_name IN ('{system_list}')
GROUP BY g.vaccine_name, p.facility_name
ORDER BY g.vaccine_name, p.facility_name;"""
    st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
    try:
        df = run_query(sql)
        if not df.empty:
            fig = px.bar(df, x="vaccine_name", y="coverage_pct",
                         color="hospital_system",
                         barmode="group",
                         template=PLOT_THEME,
                         color_discrete_map=COLOR_MAP,
                         labels={"vaccine_name": "Vaccine", "coverage_pct": "Coverage (%)",
                                 "hospital_system": "Hospital System"},
                         text="coverage_pct")
            fig.update_traces(texttemplate="%{text}%", textposition="outside")
            fig.update_layout(xaxis_tickangle=-30, yaxis_range=[0, 115])
            st.plotly_chart(plot_defaults(fig, height=420), use_container_width=True)

            st.markdown("---")
            st.markdown("<div class='section-header'>Coverage Gap (% Patients Not Vaccinated)</div>",
                        unsafe_allow_html=True)
            fig2 = px.bar(df, x="vaccine_name", y="gap_pct",
                          color="hospital_system",
                          barmode="group",
                          template=PLOT_THEME,
                          color_discrete_map=COLOR_MAP,
                          labels={"vaccine_name": "Vaccine", "gap_pct": "Gap (%)",
                                  "hospital_system": "Hospital System"})
            fig2.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(plot_defaults(fig2, height=380), use_container_width=True)

            st.markdown("---")
            st.markdown("<div class='section-header'>Coverage Detail Table</div>", unsafe_allow_html=True)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No coverage data returned.")
    except Exception as e:
        st.error(f"Query error: {e}")


# ═════════════════════════════════════════════
# PAGE 3 — PATIENT LOOKUP
# ═════════════════════════════════════════════
elif page == "🔍  Patient Lookup":
    st.markdown("# Patient Lookup")
    st.markdown(
        "<div class='section-header'>Search individual patient vaccination and encounter history</div>",
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class='info-banner'>
    Enter a Patient ID below to view their full profile, immunization history,
    and encounter records across all 3 hospital systems.
    </div>
    """, unsafe_allow_html=True)

    patient_id = st.text_input("Enter Patient ID", placeholder="e.g. 000eb977-17e7-9b09-f624-949e4202a8d7")

    if patient_id:
        sql_pat = f"""
SELECT
    patient_id, first_name, last_name, birthdate,
    TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) AS age,
    gender, race, ethnicity, city, state, facility_name AS hospital_system
FROM Patients
WHERE patient_id = '{patient_id}';"""
        st.markdown(f"<div class='sql-box'>{sql_pat.strip()}</div>", unsafe_allow_html=True)
        try:
            df_pat = run_query(sql_pat)
            if df_pat.empty:
                st.error("No patient found with that ID. Try selecting one from the sample table below.")
            else:
                st.success("✅ Patient found")
                st.dataframe(df_pat, use_container_width=True)

                col_l, col_r = st.columns(2)

                with col_l:
                    st.markdown("---")
                    st.markdown("<div class='section-header'>Immunization History</div>",
                                unsafe_allow_html=True)
                    sql_imm = f"""
SELECT
    i.imm_date          AS date_administered,
    v.description       AS vaccine,
    v.cvx_code,
    o.name              AS hospital
FROM Immunizations i
JOIN Vaccines      v  ON i.vaccine_id      = v.vaccine_id
JOIN Encounters    e  ON i.encounter_id    = e.encounter_id
JOIN Organizations o  ON e.organization_id = o.org_id
WHERE i.patient_id = '{patient_id}'
ORDER BY i.imm_date DESC;"""
                    st.markdown(f"<div class='sql-box'>{sql_imm.strip()}</div>", unsafe_allow_html=True)
                    df_imm = run_query(sql_imm)
                    if df_imm.empty:
                        st.info("No immunization records found for this patient.")
                    else:
                        st.dataframe(df_imm, use_container_width=True)

                with col_r:
                    st.markdown("---")
                    st.markdown("<div class='section-header'>Encounter History (Last 20)</div>",
                                unsafe_allow_html=True)
                    sql_enc = f"""
SELECT
    e.start_datetime    AS visit_date,
    e.encounter_class   AS visit_type,
    o.name              AS hospital,
    o.facility_name     AS hospital_system,
    pr.name             AS provider,
    pr.specialty
FROM Encounters    e
JOIN Organizations o   ON e.organization_id = o.org_id
JOIN Providers     pr  ON e.provider_id     = pr.provider_id
WHERE e.patient_id = '{patient_id}'
ORDER BY e.start_datetime DESC
LIMIT 20;"""
                    st.markdown(f"<div class='sql-box'>{sql_enc.strip()}</div>", unsafe_allow_html=True)
                    df_enc = run_query(sql_enc)
                    if df_enc.empty:
                        st.info("No encounter records found.")
                    else:
                        st.dataframe(df_enc, use_container_width=True)

                # Missed vaccines for this patient
                st.markdown("---")
                st.markdown("<div class='section-header'>Vaccines This Patient is Missing</div>",
                            unsafe_allow_html=True)
                sql_missed = f"""
SELECT DISTINCT
    g.vaccine_name      AS due_vaccine,
    g.min_age,
    g.max_age,
    g.notes             AS guideline
FROM VaccineGuidelines g
JOIN Patients p
    ON p.patient_id = '{patient_id}'
    AND TIMESTAMPDIFF(YEAR, p.birthdate, CURDATE())
        BETWEEN g.min_age AND g.max_age
LEFT JOIN Immunizations i
    ON  i.patient_id = '{patient_id}'
    AND i.vaccine_id = g.vaccine_id
WHERE i.immunization_id IS NULL;"""
                st.markdown(f"<div class='sql-box'>{sql_missed.strip()}</div>", unsafe_allow_html=True)
                try:
                    df_missed = run_query(sql_missed)
                    if df_missed.empty:
                        st.success("✅ This patient is up to date on all CDC-recommended vaccines.")
                    else:
                        st.warning(f"⚠️ {len(df_missed)} vaccine(s) due for this patient:")
                        st.dataframe(df_missed, use_container_width=True)
                except Exception as e:
                    st.warning(f"Query error: {e}")

        except Exception as e:
            st.error(f"Query error: {e}")

    else:
        st.markdown("<div class='section-header'>Sample Patients — Click a Patient ID to copy</div>",
                    unsafe_allow_html=True)
        sql_sample = """
SELECT patient_id, first_name, last_name, birthdate,
       TIMESTAMPDIFF(YEAR, birthdate, CURDATE()) AS age,
       gender, facility_name AS hospital_system
FROM Patients
ORDER BY RAND()
LIMIT 20;"""
        st.markdown(f"<div class='sql-box'>{sql_sample.strip()}</div>", unsafe_allow_html=True)
        try:
            st.dataframe(run_query(sql_sample), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")


# ═════════════════════════════════════════════
# PAGE 4 — CDC GAP ANALYSIS
# ═════════════════════════════════════════════
elif page == "⚠️  CDC Gap Analysis":
    st.markdown("# CDC Gap Analysis")
    st.markdown(
        "<div class='section-header'>Encounter-level missed vaccination opportunities · CDC ACIP 2025</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='info-banner'>
    Uses the <b>MissedVaccinations VIEW</b> — identifies every clinical encounter where
    a CDC-eligible patient did not receive a due vaccine, either at that visit or in
    their prior history within the recommended interval.
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "By Vaccine", "By Hospital System", "Patient Risk List", "Provider Specialty"
    ])

    with tab1:
        st.markdown("<div class='section-header'>Missed Opportunities by Vaccine</div>",
                    unsafe_allow_html=True)
        sql = """
SELECT
    due_vaccine,
    COUNT(*)                    AS missed_encounters,
    COUNT(DISTINCT patient_id)  AS unique_patients
FROM MissedVaccinations
GROUP BY due_vaccine
ORDER BY missed_encounters DESC;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="missed_encounters", y="due_vaccine",
                         orientation="h",
                         color="unique_patients",
                         color_continuous_scale=BLUE_SEQ,
                         template=PLOT_THEME,
                         labels={"missed_encounters": "Missed Encounters",
                                 "due_vaccine": "",
                                 "unique_patients": "Unique Patients"},
                         text="missed_encounters")
            fig.update_traces(texttemplate="%{text:,}", textposition="outside")
            fig.update_layout(yaxis=dict(autorange="reversed"),
                              coloraxis_showscale=True)
            st.plotly_chart(plot_defaults(fig, height=400), use_container_width=True)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Query error: {e}")

    with tab2:
        st.markdown("<div class='section-header'>Missed Opportunities by Hospital System & Vaccine</div>",
                    unsafe_allow_html=True)
        sql = """
SELECT
    hospital_system,
    due_vaccine,
    COUNT(*)                    AS missed_encounters,
    COUNT(DISTINCT patient_id)  AS unique_patients
FROM MissedVaccinations
GROUP BY hospital_system, due_vaccine
ORDER BY hospital_system, missed_encounters DESC;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="due_vaccine", y="missed_encounters",
                         color="hospital_system",
                         barmode="group",
                         template=PLOT_THEME,
                         color_discrete_map=COLOR_MAP,
                         labels={"due_vaccine": "Vaccine",
                                 "missed_encounters": "Missed Encounters",
                                 "hospital_system": "Hospital System"})
            fig.update_layout(xaxis_tickangle=-30)
            st.plotly_chart(plot_defaults(fig, height=400), use_container_width=True)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Query error: {e}")

    with tab3:
        st.markdown("<div class='section-header'>Top 25 Patients with Most Missed Vaccines</div>",
                    unsafe_allow_html=True)
        sql = """
SELECT
    patient_id,
    first_name,
    last_name,
    patient_age         AS age,
    gender,
    hospital_system,
    COUNT(DISTINCT due_vaccine) AS vaccines_missed
FROM MissedVaccinations
GROUP BY patient_id, first_name, last_name, patient_age, gender, hospital_system
ORDER BY vaccines_missed DESC
LIMIT 25;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df,
                         x="vaccines_missed",
                         y=df["first_name"] + " " + df["last_name"],
                         orientation="h",
                         color="hospital_system",
                         color_discrete_map=COLOR_MAP,
                         template=PLOT_THEME,
                         labels={"x": "Vaccines Missed", "y": "Patient",
                                 "hospital_system": "Hospital System"})
            fig.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_defaults(fig, height=500), use_container_width=True)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Query error: {e}")

    with tab4:
        st.markdown("<div class='section-header'>Missed Opportunities by Provider Specialty</div>",
                    unsafe_allow_html=True)
        sql = """
SELECT
    provider_specialty,
    COUNT(*)                    AS missed_encounters,
    COUNT(DISTINCT patient_id)  AS unique_patients
FROM MissedVaccinations
WHERE provider_specialty IS NOT NULL
GROUP BY provider_specialty
ORDER BY missed_encounters DESC;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.pie(df, names="provider_specialty", values="missed_encounters",
                         template=PLOT_THEME,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
            fig.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(plot_defaults(fig, height=420), use_container_width=True)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Query error: {e}")


# ═════════════════════════════════════════════
# PAGE 5 — PROVIDERS & ORGS
# ═════════════════════════════════════════════
elif page == "🏥  Providers & Orgs":
    st.markdown("# Providers & Organizations")
    st.markdown(
        "<div class='section-header'>Hospital systems and provider-level vaccination activity</div>",
        unsafe_allow_html=True
    )

    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-header'>Top Organizations by Immunizations</div>",
                    unsafe_allow_html=True)
        sql = """
SELECT o.name AS organization, o.state, COUNT(i.immunization_id) AS total
FROM Immunizations i
JOIN Encounters    e  ON i.encounter_id     = e.encounter_id
JOIN Organizations o  ON e.organization_id  = o.org_id
GROUP BY o.name, o.state
ORDER BY total DESC
LIMIT 15;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="total", y="organization",
                         orientation="h", color="state",
                         color_discrete_map=COLOR_MAP,
                         template=PLOT_THEME,
                         labels={"total": "Immunizations", "organization": "", "state": "State"})
            fig.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_defaults(fig, height=420), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")

    with col_b:
        st.markdown("<div class='section-header'>Top Providers by Immunizations</div>",
                    unsafe_allow_html=True)
        sql = """
SELECT pr.name AS provider, pr.specialty, pr.state,
       COUNT(i.immunization_id) AS total
FROM Immunizations i
JOIN Encounters e  ON i.encounter_id = e.encounter_id
JOIN Providers  pr ON e.provider_id  = pr.provider_id
GROUP BY pr.name, pr.specialty, pr.state
ORDER BY total DESC
LIMIT 15;"""
        st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
        try:
            df = run_query(sql)
            fig = px.bar(df, x="total", y="provider",
                         orientation="h", color="state",
                         color_discrete_map=COLOR_MAP,
                         template=PLOT_THEME,
                         labels={"total": "Immunizations", "provider": "", "state": "State"})
            fig.update_layout(yaxis=dict(autorange="reversed"))
            st.plotly_chart(plot_defaults(fig, height=420), use_container_width=True)
        except Exception as e:
            st.warning(f"Query error: {e}")

    st.markdown("---")
    st.markdown("<div class='section-header'>Immunizations by Provider Specialty</div>",
                unsafe_allow_html=True)
    sql = """
SELECT pr.specialty, COUNT(i.immunization_id) AS total
FROM Immunizations i
JOIN Encounters e  ON i.encounter_id = e.encounter_id
JOIN Providers  pr ON e.provider_id  = pr.provider_id
GROUP BY pr.specialty
ORDER BY total DESC;"""
    st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
    try:
        df = run_query(sql)
        fig = px.pie(df, names="specialty", values="total",
                     template=PLOT_THEME,
                     color_discrete_sequence=px.colors.sequential.Blues_r)
        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(plot_defaults(fig, height=400), use_container_width=True)
    except Exception as e:
        st.warning(f"Query error: {e}")

    st.markdown("---")
    st.markdown("<div class='section-header'>All Organizations</div>", unsafe_allow_html=True)
    sql = "SELECT org_id, name, city, state, facility_name FROM Organizations ORDER BY state, name;"
    st.markdown(f"<div class='sql-box'>{sql.strip()}</div>", unsafe_allow_html=True)
    try:
        st.dataframe(run_query(sql), use_container_width=True)
    except Exception as e:
        st.warning(f"Query error: {e}")


# ═════════════════════════════════════════════
# PAGE 6 — VACCINE GUIDELINES
# ═════════════════════════════════════════════
elif page == "📋  Vaccine Guidelines":
    st.markdown("# Vaccine Guidelines")
    st.markdown(
        "<div class='section-header'>Vaccines reference table + CDC ACIP 2025 adult guidelines</div>",
        unsafe_allow_html=True
    )

    st.markdown("<div class='section-header'>Vaccines Reference Table (25 unique vaccines)</div>",
                unsafe_allow_html=True)
    sql_vax = "SELECT vaccine_id, description AS vaccine, cvx_code, manufacturer FROM Vaccines ORDER BY description;"
    st.markdown(f"<div class='sql-box'>{sql_vax.strip()}</div>", unsafe_allow_html=True)
    try:
        st.dataframe(run_query(sql_vax), use_container_width=True)
    except Exception as e:
        st.warning(f"Query error: {e}")

    st.markdown("---")
    st.markdown("<div class='section-header'>CDC ACIP 2025 Adult Guidelines</div>",
                unsafe_allow_html=True)
    sql_gl = """
SELECT
    g.guideline_id,
    g.vaccine_name,
    v.cvx_code,
    g.min_age,
    g.max_age,
    g.interval_years,
    g.notes,
    g.source
FROM VaccineGuidelines g
JOIN Vaccines v ON g.vaccine_id = v.vaccine_id
ORDER BY g.min_age;"""
    st.markdown(f"<div class='sql-box'>{sql_gl.strip()}</div>", unsafe_allow_html=True)
    try:
        df_gl = run_query(sql_gl)
        st.dataframe(df_gl, use_container_width=True)

        st.markdown("---")
        st.markdown("<div class='section-header'>Vaccine Age Windows (Gantt View)</div>",
                    unsafe_allow_html=True)
        if not df_gl.empty:
            fig = go.Figure()
            for _, row in df_gl.iterrows():
                max_display = min(row["max_age"], 100)
                fig.add_trace(go.Bar(
                    x=[max_display - row["min_age"]],
                    y=[row["vaccine_name"]],
                    base=row["min_age"],
                    orientation="h",
                    marker_color="#1976D2",
                    marker_line_color="#1565C0",
                    marker_line_width=1,
                    showlegend=False,
                    hovertemplate=(
                        f"<b>{row['vaccine_name']}</b><br>"
                        f"Age range: {row['min_age']}–"
                        f"{'no limit' if row['max_age'] >= 999 else str(row['max_age'])} yrs<br>"
                        f"Interval: {'one-time' if pd.isna(row['interval_years']) else str(row['interval_years']) + ' yr(s)'}"
                        f"<extra></extra>"
                    )
                ))
            fig.update_layout(
                template=PLOT_THEME,
                paper_bgcolor=PLOT_BG,
                plot_bgcolor=PLOT_BG,
                xaxis_title="Age (years)",
                xaxis_range=[15, 105],
                height=max(300, len(df_gl) * 45),
                margin=dict(t=10, b=30),
                font=dict(family="DM Sans", color="#1a2332"),
            )
            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Query error: {e}")


# ═════════════════════════════════════════════
# PAGE 7 — TABLEAU DASHBOARD
# ═════════════════════════════════════════════
elif page == "📈  Tableau Dashboard":
    st.markdown("# Tableau Dashboard")
    st.markdown(
        "<div class='section-header'>Interactive vaccination gap analysis · Published on Tableau Public</div>",
        unsafe_allow_html=True
    )
    st.markdown("""
    <div class='info-banner'>
    This dashboard shows vaccination <b>coverage gaps by hospital system</b>,
    <b>missed opportunities by vaccine</b>, and a <b>patient risk heatmap</b>.
    Click any bar in the coverage chart to filter the patient risk panel.
    </div>
    """, unsafe_allow_html=True)

    st.components.v1.iframe(
        src="https://public.tableau.com/views/VaccinationDashboard_17772254406650/Dashboard1"
            "?:embed=yes&:showVizHome=no&:toolbar=yes&:animate_transition=yes",
        width=1200,
        height=900,
        scrolling=True
    )

    st.markdown("""
    <div style='text-align:center; margin-top:12px;'>
        <a href='https://public.tableau.com/views/VaccinationDashboard_17772254406650/Dashboard1'
           target='_blank'
           style='color:#1976D2; font-size:0.85rem;'>
            🔗 Open full dashboard in Tableau Public
        </a>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════
# PAGE 8 — SQL QUERY RUNNER
# ═════════════════════════════════════════════
elif page == "🗄️  SQL Query Runner":
    st.markdown("# SQL Query Runner")
    st.markdown(
        "<div class='section-header'>Run custom queries against vaccination_db in real time</div>",
        unsafe_allow_html=True
    )

    presets = {
        "-- Select a preset --": "",
        "All table row counts": """SELECT 'Patients' AS tbl, COUNT(*) AS rows FROM Patients
UNION ALL SELECT 'Organizations', COUNT(*) FROM Organizations
UNION ALL SELECT 'Providers',     COUNT(*) FROM Providers
UNION ALL SELECT 'Vaccines',      COUNT(*) FROM Vaccines
UNION ALL SELECT 'VaccineGuidelines', COUNT(*) FROM VaccineGuidelines
UNION ALL SELECT 'Encounters',    COUNT(*) FROM Encounters
UNION ALL SELECT 'Immunizations', COUNT(*) FROM Immunizations;""",
        "Patients by hospital system": (
            "SELECT facility_name AS hospital_system, COUNT(*) AS patients "
            "FROM Patients GROUP BY facility_name ORDER BY patients DESC;"
        ),
        "Top 10 vaccines administered": (
            "SELECT v.description AS vaccine, COUNT(*) AS count "
            "FROM Immunizations i JOIN Vaccines v ON i.vaccine_id = v.vaccine_id "
            "GROUP BY v.description ORDER BY count DESC LIMIT 10;"
        ),
        "Coverage % by vaccine + hospital": """SELECT g.vaccine_name, p.facility_name AS hospital_system,
    COUNT(DISTINCT p.patient_id) AS eligible,
    COUNT(DISTINCT i.patient_id) AS vaccinated,
    ROUND(100.0 * COUNT(DISTINCT i.patient_id) /
          NULLIF(COUNT(DISTINCT p.patient_id),0), 1) AS coverage_pct
FROM VaccineGuidelines g
JOIN Patients p ON TIMESTAMPDIFF(YEAR, p.birthdate, CURDATE()) BETWEEN g.min_age AND g.max_age
LEFT JOIN Immunizations i ON i.patient_id = p.patient_id AND i.vaccine_id = g.vaccine_id
GROUP BY g.vaccine_name, p.facility_name
ORDER BY g.vaccine_name;""",
        "Missed opportunities by vaccine (VIEW)": (
            "SELECT due_vaccine, COUNT(*) AS missed_encounters, "
            "COUNT(DISTINCT patient_id) AS unique_patients "
            "FROM MissedVaccinations GROUP BY due_vaccine ORDER BY missed_encounters DESC;"
        ),
        "Top 20 patients with most missed vaccines": (
            "SELECT first_name, last_name, patient_age, hospital_system, "
            "COUNT(DISTINCT due_vaccine) AS vaccines_missed "
            "FROM MissedVaccinations "
            "GROUP BY patient_id, first_name, last_name, patient_age, hospital_system "
            "ORDER BY vaccines_missed DESC LIMIT 20;"
        ),
        "Patients with no immunizations": (
            "SELECT patient_id, first_name, last_name, facility_name "
            "FROM Patients WHERE patient_id NOT IN "
            "(SELECT DISTINCT patient_id FROM Immunizations) LIMIT 50;"
        ),
        "Encounters per organization": (
            "SELECT o.name AS organization, o.state, COUNT(e.encounter_id) AS encounters "
            "FROM Encounters e JOIN Organizations o ON e.organization_id = o.org_id "
            "GROUP BY o.name, o.state ORDER BY encounters DESC LIMIT 20;"
        ),
        "CDC Guidelines with vaccine names": (
            "SELECT g.guideline_id, g.vaccine_name, v.cvx_code, "
            "g.min_age, g.max_age, g.interval_years, g.notes "
            "FROM VaccineGuidelines g JOIN Vaccines v ON g.vaccine_id = v.vaccine_id;"
        ),
    }

    selected = st.selectbox("Load a preset query", list(presets.keys()))
    default_sql = presets[selected] if selected != "-- Select a preset --" else "SELECT * FROM Patients LIMIT 10;"

    user_sql = st.text_area("SQL Query", value=default_sql.strip(), height=160,
                             placeholder="Write any SELECT query here...")

    col_run, col_clear = st.columns([1, 5])
    with col_run:
        run_btn = st.button("▶  Run Query", type="primary")

    if run_btn:
        if user_sql.strip():
            try:
                df = run_query(user_sql)
                st.success(f"✅ {len(df):,} row(s) returned")
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "⬇  Download results as CSV",
                    data=csv,
                    file_name="query_result.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"Query error: {e}")
        else:
            st.warning("Please enter a SQL query.")
