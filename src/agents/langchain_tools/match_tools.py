# src/agents/langchain_tools/match_tools.py

from typing import Dict, List
from langchain.tools import tool

def _get_all_skills() -> Dict[str, List[str]]:
    """Master skill dictionary used by the AI Agent."""
    return {
        "data scientist": ["python", "sql", "machine learning", "statistics", "pandas", "numpy"],
        "data engineer": ["python", "sql", "spark", "airflow", "etl", "data pipelines"],
        "ml engineer": ["python", "mlops", "docker", "kubernetes", "model deployment"],
        "ai engineer": ["python", "deep learning", "model deployment", "mlops"],
        "data analyst": ["sql", "excel", "power bi", "tableau", "statistics"],
        "software engineer": ["java", "python", "data structures", "algorithms", "system design"],
        "devops engineer": ["ci/cd", "docker", "kubernetes", "aws", "linux"]
    }

@tool("match_to_role")
def match_to_role(resume_skills: List[str], role_title: str) -> Dict:
    """Matches resume skills against a specific job role dynamically."""
    
    # 1. Clean the input
    role_key = str(role_title).strip().lower()
    role_map = _get_all_skills()
    
    # 2. Get requirements (Fallback to empty list if role not found)
    # THIS REMOVES THE VALUEERROR PERMANENTLY
    required_skills = role_map.get(role_key, [])
    
    # 3. Process matching
    resume_set = set(s.lower() for s in resume_skills) if resume_skills else set()
    required_set = set(required_skills)
    
    matched = sorted(list(resume_set & required_set))
    missing = sorted(list(required_set - resume_set))
    
    # 4. Calculate score
    if not required_set:
        score = 0.0
        note = f"Role '{role_title}' not in master list. Showing all found skills."
    else:
        score = round((len(matched) / len(required_set)) * 100, 2)
        note = "Success"

    return {
        "role": role_title,
        "score": score,
        "matched_skills": matched,
        "missing_skills": missing,
        "status": note
    }