import sys
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go
import requests
import warnings

warnings.filterwarnings("ignore")

from src.bias_diagnostics import BiasDiagnostics
from src.resume_parser import extract_text_from_pdf
from src.indexer import SkillIndexer
from src.matcher import SkillMatcher
from src.agent_mcp import MCPResumeMatchAgent

# ==================================================
# 1. CORE ENGINES & CONFIG
# ==================================================
ADZUNA_APP_ID = "709a7827"
ADZUNA_APP_KEY = "4f538cc0961df5eee65e9c53f82d7ee2"

try:
    from src.agents.agent_langchain import ResumeSkillAgent
    LANGCHAIN_AVAILABLE = True
except Exception:
    LANGCHAIN_AVAILABLE = False

@st.cache_resource
def load_skills_catalog():
    try:
        df = pd.read_parquet("data/processed/skills_catalog.parquet")
        return df["skill"].astype(str).str.lower().unique().tolist()
    except:
        return ["python", "sql", "machine learning", "aws", "docker", "kubernetes", "system design"]

@st.cache_resource
def get_matcher():
    catalog = load_skills_catalog()
    return SkillMatcher(catalog, SkillIndexer(catalog))

def calculate_economic_impact(score, role):
    base_salaries = {"Data Scientist": 180000, "Software Engineer": 190000, "AI Engineer": 220000, "ML Engineer": 210000}
    base = base_salaries.get(role, 150000)
    return round(base * ((score / 100) ** 2) * 3.5, 2)

def fetch_hiring_companies(role, location="us"):
    """Fetches real-time job listings using Adzuna API"""
    url = f"https://api.adzuna.com/v1/api/jobs/{location}/search/1"
    params = {
        "app_id": "709a7827",
        "app_key": "4f538cc0961df5eee65e9c53f82d7ee2",
        "results_per_page": 5,
        "what": role,
        "content-type": "application/json"
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get('results', [])
    except Exception:
        return []
    return []

def generate_radar_chart(resume_skills, role_skills):
    """Principal Level: Topological Skill Mapping."""
    categories = list(role_skills)[:6]
    resume_scores = [1 if s.lower() in [rs.lower() for rs in resume_skills] else 0.2 for s in categories]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=resume_scores, theta=categories, fill='toself', 
        line_color='#E50914', marker=dict(color='#E50914')
    ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False), bgcolor="#141414"),
        paper_bgcolor="rgba(0,0,0,0)", font_color="white", showlegend=False, 
        height=350, margin=dict(t=30, b=30, l=30, r=30)
    )
    return fig

# ==================================================
# 2. UI & STYLING
# ==================================================
st.set_page_config(page_title="Vignesh's Intelligence", layout="wide")

st.markdown("""
    <style>
        .stApp { background-color: #000000; color: #FFFFFF; }
        .main-header { font-size: 2.8rem; font-weight: 800; color: #E50914; margin-bottom: 0; }
        .section-head { color: #E50914; font-weight: bold; border-bottom: 1px solid #333; padding-bottom: 5px; margin-top: 20px; }
        .job-card { background: #111; padding: 15px; border-radius: 8px; border-left: 5px solid #E50914; margin-bottom: 10px; }
        [data-testid="stMetricValue"] { color: #E50914 !important; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="main-header">AI Resume Skill Matcher</p>', unsafe_allow_html=True)
st.caption("Vignesh Murugesan's ATS with Resume vs JD comparison, bias diagnostics, confidence calibration, hiring risk estimation, offer probability")

# ==================================================
# 3. INPUT SECTION
# ==================================================
st.markdown('<p class="section-head">Upload Resume & Job Description</p>', unsafe_allow_html=True)
col_u1, col_u2 = st.columns(2)
with col_u1:
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])
with col_u2:
    uploaded_jd = st.file_uploader("Upload Job Description (PDF) [Optional]", type=["pdf"])

ROLE_SKILLS = {
    "Data Scientist": ["python", "sql", "machine learning", "statistics", "pandas", "numpy"],
    "Data Engineer": ["python", "sql", "spark", "airflow", "etl", "data pipelines"],
    "Data Analyst": ["sql", "excel", "power bi", "tableau", "statistics"],
    "AI Engineer": ["python", "deep learning", "model deployment", "mlops"],
    "ML Engineer": ["python", "mlops", "docker", "kubernetes"],
    "Software Engineer": ["java", "python", "data structures", "algorithms", "system design"],
    "DevOps Engineer": ["ci/cd", "docker", "kubernetes", "aws", "linux"],
}

selected_roles = st.multiselect("Select Target Roles for Multi-Match Analysis", 
                                list(ROLE_SKILLS.keys()), default=["Data Scientist"])

# ==================================================
# 4. PROCESSING PIPELINE
# ==================================================
if uploaded_resume and selected_roles:
    resume_path = Path("temp_resume.pdf")
    resume_path.write_bytes(uploaded_resume.read())
    resume_text = extract_text_from_pdf(resume_path)
    
    matcher = get_matcher()
    resume_skills_raw = matcher.extract_resume_skills(resume_text)
    resume_skills = [s["skill"] for s in resume_skills_raw if s["confidence"] > 0.15]
    resume_skill_set = set(s.lower() for s in resume_skills)

    # --- Resume vs JD Feature ---
    if uploaded_jd:
        jd_path = Path("temp_jd.pdf")
        jd_path.write_bytes(uploaded_jd.read())
        jd_text = extract_text_from_pdf(jd_path)
        jd_skills_raw = matcher.extract_resume_skills(jd_text)
        jd_skill_set = set(s["skill"].lower() for s in jd_skills_raw)
        
        st.markdown('<p class="section-head">📑 RESUME VS JOB DESCRIPTION</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        c1.metric("JD Skills Found", len(jd_skill_set))
        c2.metric("Overlap", len(resume_skill_set & jd_skill_set))
        c3.metric("Critical Gaps", len(jd_skill_set - resume_skill_set), delta_color="inverse")

    # --- Multi-Role Match Comparison ---
    st.markdown('<p class="section-head">🧩 MULTI-ROLE STRATEGIC ALIGNMENT</p>', unsafe_allow_html=True)
    rows = []
    for role in selected_roles:
        r_set = set(s.lower() for s in ROLE_SKILLS[role])
        match_count = len(resume_skill_set & r_set)
        score = round((match_count / len(r_set)) * 100, 2)
        rows.append({"Role": role, "Match %": score, "Matched": match_count, "Total": len(r_set)})
    
    df_compare = pd.DataFrame(rows).sort_values("Match %", ascending=False)
    st.table(df_compare)

    # --- CALIBRATION & TOPOLOGY PANEL ---
    best_role = df_compare.iloc[0]["Role"]
    best_score = df_compare.iloc[0]["Match %"]
    role_set = set(s.lower() for s in ROLE_SKILLS[best_role])
    
    st.markdown('<p class="section-head">🎯 CALIBRATION & SKILL TOPOLOGY</p>', unsafe_allow_html=True)
    col_met, col_chart = st.columns([1, 1])
    
    with col_met:
        st.metric("Overall Fit", f"{best_score}%", best_role)
        risk = round((len(role_set - resume_skill_set) / len(role_set)) * 100, 2)
        st.metric("Hiring Risk", f"{risk}%", "High" if risk > 40 else "Low", delta_color="inverse")
        prob = max(0.0, min(round(best_score * 0.6 + (100 - risk) * 0.4, 2), 100.0))
        st.metric("Offer Probability", f"{prob}%")
        st.metric("Economic Impact", f"${calculate_economic_impact(best_score, best_role):,}")

    with col_chart:
        st.plotly_chart(generate_radar_chart(resume_skills, list(role_set)), use_container_width=True)

    # --- Bias Diagnostics ---
    st.markdown('<p class="section-head">BIAS DIAGNOSTICS</p>', unsafe_allow_html=True)
    match_scores_map = {row["Role"]: row["Match %"] for _, row in df_compare.iterrows()}
    bias_engine = BiasDiagnostics(resume_skills=resume_skills_raw, role_skills_map=ROLE_SKILLS, match_scores=match_scores_map)
    st.json(bias_engine.summary())

    # --- Live Hiring ---
    st.divider()
    st.header("Who is Hiring Now?")
    st.caption(f"Live openings for **{best_role}**")

    with st.spinner("Searching live job market..."):
        jobs = fetch_hiring_companies(best_role)
        if jobs:
            for job in jobs:
                st.markdown(f"""
                <div class="job-card">
                    <h4 style="margin:0; color:#fff;">{job.get('title')}</h4>
                    <p style="color:#E50914; font-weight:bold; margin:2px 0;">{job.get('company', {}).get('display_name')}</p>
                    <p style="font-size: 0.8em; color:#aaa;">📍 {job.get('location', {}).get('display_name')}</p>
                    <a href="{job.get('redirect_url')}" target="_blank" style="color: white; text-decoration: none; background-color: #E50914; padding: 5px 12px; border-radius: 4px; font-size: 0.8em; display: inline-block; margin-top: 5px;">Apply on Adzuna</a>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No current listings found. Verify your API keys.")

    # --- Agent Insights ---
    if LANGCHAIN_AVAILABLE:
        st.divider()
        with st.expander("PRINCIPAL AGENT DEEP-DIVE"):
            if st.button("ORCHESTRATE ANALYSIS"):
                agent = ResumeSkillAgent(verbose=False)
                st.write(agent.run(resume_pdf_path=str(resume_path), role=best_role).get("summary", "Done."))

else:
    st.info("📊 Upload your dossier to begin the Assessment.")