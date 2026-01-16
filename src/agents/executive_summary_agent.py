# src/agents/executive_summary_agent.py

from dataclasses import dataclass
from typing import List


@dataclass
class ExecutiveSummary:
    role: str
    overall_recommendation: str
    confidence_level: str
    risk_statement: str
    justification: str
    next_steps: List[str]


class ExecutiveSummaryAgent:
    """
    Produces C-level, recruiter-ready hiring summaries.
    Deterministic and policy-driven.
    """

    def generate(
        self,
        role: str,
        match_score: float,
        hiring_risk: float,
        offer_probability: float,
        critical_gaps: List[str],
    ) -> ExecutiveSummary:

        # -------------------------
        # Overall recommendation
        # -------------------------
        if offer_probability >= 75 and hiring_risk < 40:
            recommendation = "Strong Hire Recommendation"
            confidence = "High"
        elif offer_probability >= 55:
            recommendation = "Proceed with Caution"
            confidence = "Medium"
        else:
            recommendation = "Do Not Proceed at This Stage"
            confidence = "Low"

        # -------------------------
        # Risk statement
        # -------------------------
        if hiring_risk < 30:
            risk_statement = "Low execution and onboarding risk identified."
        elif hiring_risk < 60:
            risk_statement = (
                "Moderate risk identified; mitigations required during onboarding."
            )
        else:
            risk_statement = (
                "High risk identified; recommend reassessment after skill development."
            )

        # -------------------------
        # Justification
        # -------------------------
        gap_text = (
            ", ".join(critical_gaps[:3])
            if critical_gaps
            else "no critical skill gaps"
        )

        justification = (
            f"For the role of {role}, the candidate demonstrates a match score of "
            f"{match_score}%, with an estimated offer probability of "
            f"{offer_probability}%. The primary risks relate to {gap_text}. "
            f"The decision balances skill alignment with realistic delivery risk."
        )

        # -------------------------
        # Next steps
        # -------------------------
        if confidence == "High":
            next_steps = [
                "Advance to final technical and leadership interviews",
                "Prepare compensation benchmark",
                "Initiate reference checks",
            ]
        elif confidence == "Medium":
            next_steps = [
                "Conduct targeted technical interview on missing skills",
                "Evaluate learning velocity and adaptability",
                "Reassess after interview loop",
            ]
        else:
            next_steps = [
                "Recommend upskilling period",
                "Re-evaluate candidate in future hiring cycle",
            ]

        return ExecutiveSummary(
            role=role,
            overall_recommendation=recommendation,
            confidence_level=confidence,
            risk_statement=risk_statement,
            justification=justification,
            next_steps=next_steps,
        )
