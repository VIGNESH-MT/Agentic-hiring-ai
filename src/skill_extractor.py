# src/skill_extractor.py

from rapidfuzz import fuzz
from typing import List, Dict

def extract_skills_from_text(
    text: str,
    skills_catalog: List[str],
    threshold: int = 85
) -> List[Dict]:
    """
    Hybrid extraction:
    - exact match
    - fuzzy match
    """
    found = []

    text_lower = text.lower()

    for skill in skills_catalog:
        skill_lower = skill.lower()

        if skill_lower in text_lower:
            found.append({
                "skill": skill,
                "method": "exact",
                "confidence": 1.0
            })
        else:
            score = fuzz.partial_ratio(skill_lower, text_lower)
            if score >= threshold:
                found.append({
                    "skill": skill,
                    "method": "fuzzy",
                    "confidence": score / 100
                })

    return found
