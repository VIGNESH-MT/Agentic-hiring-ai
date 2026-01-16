# src/agents/langchain_tools/resume_tools.py

from typing import Dict, List
from pathlib import Path
from langchain.tools import tool

from src.resume_parser import extract_text_from_pdf
from src.matcher import SkillMatcher
from src.indexer import SkillIndexer


@tool("extract_resume_skills")
def extract_resume_skills(resume_pdf_path: str) -> Dict[str, List[Dict]]:
    """
    Extract structured skills from a resume PDF.
    Deterministic, schema-safe, MCP-compatible.
    """

    pdf_path = Path(resume_pdf_path)
    if not pdf_path.exists():
        raise FileNotFoundError(f"Resume PDF not found: {resume_pdf_path}")

    resume_text = extract_text_from_pdf(pdf_path)
    if not resume_text.strip():
        return {"skills": []}

    import pandas as pd
    skills_df = pd.read_parquet("data/processed/skills_catalog.parquet")
    skills_catalog = (
        skills_df["skill"].astype(str).str.lower().unique().tolist()
    )

    matcher = SkillMatcher(skills_catalog, SkillIndexer(skills_catalog))
    extracted = matcher.extract_resume_skills(resume_text)

    structured_skills = [
        {
            "skill": s["skill"],
            "confidence": round(float(s["confidence"]), 3),
            "method": s["method"],
            "evidence_snippet": s["evidence_snippet"],
        }
        for s in extracted
    ]

    return {"skills": structured_skills}
