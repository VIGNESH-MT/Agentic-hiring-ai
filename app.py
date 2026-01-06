import streamlit as st
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from src.resume_parser import extract_text_from_pdf
from src.indexer import SkillIndexer
from src.matcher import SkillMatcher
from src.agent_mcp import MCPResumeMatchAgent

# ---------------------------
# App configuration
# ---------------------------
st.set_page_config(page_title="AI Resume Skill Matcher", layout="wide")

st.title("🎯 AI Resume Skill Matcher")
st.caption(
    "Vignesh Murugesan's ATS with Resume vs JD comparison, MCP agent orchestration, "
    "multi-role evaluation, and recruiter-ready explanations"
)

CONFIDENCE_THRESHOLD = 0.15  # fixed 15%

# ---------------------------
# Load skills catalog
# ---------------------------
@st.cache_resource
def load_skills_catalog():
    df = pd.read_parquet("data/processed/skills_catalog.parquet")
    return df["skill"].astype(str).str.lower().unique().tolist()

skills_catalog = load_skills_catalog()

# ---------------------------
# Initialize engines
# ---------------------------
@st.cache_resource
def init_matcher(skills):
    return SkillMatcher(skills, SkillIndexer(skills))

@st.cache_resource
def init_mcp_agent():
    return MCPResumeMatchAgent()

matcher = init_matcher(skills_catalog)
mcp_agent = init_mcp_agent()

Path("outputs").mkdir(exist_ok=True)

# ---------------------------
# Upload Section
# ---------------------------
st.header("📄 Upload Resume & Job Description")

col1, col2 = st.columns(2)

with col1:
    uploaded_resume = st.file_uploader("Upload Resume (PDF)", type=["pdf"])

with col2:
    uploaded_jd = st.file_uploader("Upload Job Description (PDF)", type=["pdf"])

# ---------------------------
# Role Definitions (20+ roles)
# ---------------------------
ROLE_SKILLS = {
    "Data Scientist": ["python", "sql", "machine learning", "statistics", "pandas", "numpy"],
    "Data Engineer": ["python", "sql", "spark", "airflow", "etl", "data pipelines"],
    "Data Analyst": ["sql", "excel", "power bi", "tableau", "statistics"],
    "Analytics Engineer": ["sql", "dbt", "data modeling", "etl"],

    "AI Engineer": ["python", "deep learning", "model deployment", "mlops"],
    "ML Engineer": ["python", "mlops", "docker", "kubernetes"],
    "GenAI Specialist": ["llms", "prompt engineering", "rag", "vector databases"],
    "LLM Developer": ["transformers", "huggingface", "langchain", "python"],

    "Software Engineer": ["java", "python", "data structures", "algorithms", "system design"],
    "Backend Engineer": ["java", "spring", "apis", "microservices", "databases"],
    "Frontend Engineer": ["react", "javascript", "html", "css"],
    "Full Stack Engineer": ["react", "node", "apis", "databases"],

    "DevOps Engineer": ["ci/cd", "docker", "kubernetes", "aws", "linux"],
    "Cloud Engineer": ["aws", "azure", "gcp"],
    "SRE": ["monitoring", "linux", "incident management", "automation"],

    "Test Engineer": ["test automation", "selenium", "qa"],
    "QA Engineer": ["manual testing", "automation", "test cases"],

    "Tech Support Engineer": ["troubleshooting", "linux", "networking"],
    "Support Engineer": ["incident handling", "ticketing systems"],
}

# ---------------------------
# Role selection
# ---------------------------
st.header("🎯 Select Target Role(s)")
selected_roles = st.multiselect(
    "Choose one or more roles",
    list(ROLE_SKILLS.keys()),
    default=["Data Scientist"]
)

# ---------------------------
# Main pipeline
# ---------------------------
if uploaded_resume:
    # --- Extract Resume ---
    resume_path = Path("temp_resume.pdf")
    resume_path.write_bytes(uploaded_resume.read())
    resume_text = extract_text_from_pdf(resume_path)

    if not resume_text.strip():
        st.error("❌ Resume text extraction failed.")
        st.stop()

    resume_skills_raw = matcher.extract_resume_skills(resume_text)
    resume_skills = [s for s in resume_skills_raw if s["confidence"] >= CONFIDENCE_THRESHOLD]
    resume_skill_set = {s["skill"] for s in resume_skills}

    # ---------------------------
    # Resume vs JD comparison (NEW)
    # ---------------------------
    jd_skill_set = set()
    if uploaded_jd:
        jd_path = Path("temp_jd.pdf")
        jd_path.write_bytes(uploaded_jd.read())
        jd_text = extract_text_from_pdf(jd_path)

        jd_skills_raw = matcher.extract_resume_skills(jd_text)
        jd_skill_set = {s["skill"] for s in jd_skills_raw}

        st.subheader("📑 Resume vs Job Description Skill Comparison")

        matched_r_jd = resume_skill_set & jd_skill_set
        missing_r_jd = jd_skill_set - resume_skill_set

        st.markdown(f"**Matched Skills:** {len(matched_r_jd)}")
        st.markdown(f"**Missing from Resume:** {len(missing_r_jd)}")

    # ---------------------------
    # Extracted Resume Skills (MAX 5 RULE)
    # ---------------------------
    if len(resume_skills) <= 5:
        st.subheader("🧠 Extracted Resume Skills")

        for s in sorted(resume_skills, key=lambda x: x["confidence"], reverse=True):
            st.markdown(
                f"""
                <div style="
                    background:#1f1f1f;
                    padding:14px;
                    border-radius:10px;
                    margin-bottom:10px;
                    border-left:4px solid #E50914;
                ">
                    <b>{s['skill'].title()}</b><br>
                    <span style="color:#bbbbbb;">
                        Method: {s['method']} | Confidence: {round(s['confidence'],2)}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            with st.expander("🔍 Evidence"):
                st.code(s["evidence_snippet"])
    else:
        st.info("ℹ️ More than 5 skills detected. Skills hidden to reduce noise.")

    # ---------------------------
    # Multi-role comparison
    # ---------------------------
    st.subheader("🧩 Multi-Role Match Comparison")

    rows = []
    for role in selected_roles:
        role_set = set(ROLE_SKILLS[role])
        matched = len(resume_skill_set & role_set)
        total = len(role_set)
        score = round((matched / total) * 100, 2)

        rows.append({
            "Role": role,
            "Match %": score,
            "Matched Skills": matched,
            "Total Required": total
        })

    df_compare = pd.DataFrame(rows)

    if df_compare.empty:
       st.warning("⚠️ Please select at least one target role for comparison.")
       st.stop()

    if "Match %" not in df_compare.columns:
       st.error("❌ Match score could not be computed. Check role definitions.")
       st.stop()

    df_compare = df_compare.sort_values("Match %", ascending=False)
    st.dataframe(df_compare, width="stretch")

    # ---------------------------
    # Best role + MCP agent
    # ---------------------------
    best_role = df_compare.iloc[0]["Role"]
    role_set = set(ROLE_SKILLS[best_role])

    mcp_result = mcp_agent.run(
        resume_text=resume_text,
        role_skills=list(role_set)
    )

    score = mcp_result.get("score", 0)

    # ---------------------------
    # Match Score Card
    # ---------------------------
    st.subheader(f"📊 Match Score — {best_role}")
    st.markdown(
        f"""
        <div style="background:#1f1f1f;padding:22px;border-radius:14px;text-align:center;">
            <h2 style="color:#E50914;">Overall Fit</h2>
            <h1>{score}%</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------
    # Pie chart
    # ---------------------------
    matched = len(resume_skill_set & role_set)
    missing = max(len(role_set) - matched, 0)

    fig, ax = plt.subplots(figsize=(4, 4))
    ax.pie(
        [matched, missing],
        labels=["Matched", "Missing"],
        autopct="%1.0f%%",
        colors=["#2ECC71", "#E74C3C"],
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

    # ---------------------------
    # Skill Gap Recommendations
    # ---------------------------
    st.subheader("🚀 Skill Gap Recommendations")
    missing_skills = sorted(role_set - resume_skill_set)

    if missing_skills:
        for s in missing_skills:
            st.markdown(f"- 📘 Learn **{s.title()}**")
    else:
        st.success("Excellent alignment — no major gaps.")

    # ---------------------------
    # LLM-style Explanation
    # ---------------------------
    st.subheader("🧠 Recruiter Explanation")

    explanation = (
        f"For the **{best_role}** role, the candidate matches approximately "
        f"**{score}%** of the required skills. Strong alignment is observed in "
        f"{', '.join(sorted(resume_skill_set & role_set)) or 'general competencies'}. "
        f"Skill development is recommended in "
        f"{', '.join(missing_skills) if missing_skills else 'advanced role-specific areas'}."
    )

    st.markdown(
        f"""
        <div style="background:#1f1f1f;padding:18px;border-radius:12px;border-left:4px solid #E50914;">
            {explanation}
        </div>
        """,
        unsafe_allow_html=True
    )

    # ---------------------------
    # PDF Export
    # ---------------------------
    st.subheader("📄 Export Recruiter Report")

    if st.button("⬇️ Download PDF"):
        pdf_path = "outputs/recruiter_report.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        t = c.beginText(40, 800)

        t.textLine("AI Resume Skill Matcher — Recruiter Report")
        t.textLine("")
        t.textLine(f"Best Role: {best_role}")
        t.textLine(f"Match Score: {score}%")
        t.textLine("")
        t.textLine("Skill Gaps:")
        for s in missing_skills:
            t.textLine(f"- {s}")

        t.textLine("")
        t.textLine("Explanation:")
        for line in explanation.split(". "):
            t.textLine(line.strip())

        c.drawText(t)
        c.save()

        with open(pdf_path, "rb") as f:
            st.download_button(
                "📥 Download Report",
                f,
                file_name="recruiter_report.pdf",
                mime="application/pdf"
            )

    resume_path.unlink(missing_ok=True)
    if uploaded_jd:
        jd_path.unlink(missing_ok=True)

# ---------------------------
# Footer
# ---------------------------
st.markdown("---")
st.caption("⚠️ Decision-support only. Not for automated hiring decisions.")
