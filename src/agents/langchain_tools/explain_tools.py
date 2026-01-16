# src/agents/langchain_tools/explain_tools.py

from typing import Dict
from langchain.tools import tool


@tool("explain_match")
def explain_match(match_report: Dict) -> Dict:
    """
    Deterministic recruiter explanation.
    SAFE: uses only guaranteed inputs.
    """

    # Guaranteed fields from match_to_role
    role = match_report["role"]
    score = float(match_report["score"])
    matched_skills = match_report["matched_skills"]
    missing_skills = match_report["missing_skills"]

    # Derived metrics (local computation ONLY)
    hiring_risk = round(100.0 - score, 2)
    offer_probability = round(
        (score * 0.6) + ((100.0 - hiring_risk) * 0.4),
        2
    )

    if score >= 85:
        strength = "exceptionally strong alignment"
    elif score >= 70:
        strength = "strong alignment"
    elif score >= 50:
        strength = "partial alignment"
    else:
        strength = "weak alignment"

    if offer_probability >= 75:
        decision = "Strong Hire — fast-track to final interviews."
    elif offer_probability >= 50:
        decision = "Hire with reservations — proceed with interviews."
    elif score >= 50:
        decision = "Borderline — targeted interviews recommended."
    else:
        decision = "Do not proceed."

    return {
        "summary": (
            f"For the **{role}** role, the candidate shows "
            f"{strength} with a score of **{score}%**."
        ),
        "strengths": matched_skills,
        "gaps": missing_skills,
        "hiring_risk": hiring_risk,
        "offer_probability": offer_probability,
        "panel_recommendation": decision,
    }
