# src/agents/alignment_agent.py

from dataclasses import dataclass
from typing import Set, Dict, List


@dataclass
class AlignmentResult:
    """
    Final alignment decision object.
    """
    score: float
    mandatory_coverage: float
    optional_coverage: float
    missing_mandatory: Set[str]
    matched_optional: Set[str]
    decision: str
    explanation: str


class AlignmentAgent:
    """
    Staff-level Resume ↔ JD Alignment Engine.

    Deterministic.
    Auditable.
    Recruiter-grade.
    """

    def __init__(
        self,
        mandatory_weight: float = 0.70,
        optional_weight: float = 0.20,
        depth_weight: float = 0.10,
        min_mandatory_coverage: float = 0.50
    ):
        self.mandatory_weight = mandatory_weight
        self.optional_weight = optional_weight
        self.depth_weight = depth_weight
        self.min_mandatory_coverage = min_mandatory_coverage

    def align(
        self,
        resume_skills: Set[str],
        jd_mandatory: Set[str],
        jd_optional: Set[str]
    ) -> AlignmentResult:

        # -----------------------------
        # Mandatory coverage
        # -----------------------------
        matched_mandatory = resume_skills & jd_mandatory
        missing_mandatory = jd_mandatory - resume_skills

        mandatory_coverage = (
            len(matched_mandatory) / max(len(jd_mandatory), 1)
        )

        # -----------------------------
        # Optional coverage
        # -----------------------------
        matched_optional = resume_skills & jd_optional
        optional_coverage = (
            len(matched_optional) / max(len(jd_optional), 1)
        )

        # -----------------------------
        # Depth heuristic
        # -----------------------------
        depth_bonus = min(len(resume_skills) / 20.0, 1.0)

        # -----------------------------
        # Score composition
        # -----------------------------
        score = (
            mandatory_coverage * self.mandatory_weight +
            optional_coverage * self.optional_weight +
            depth_bonus * self.depth_weight
        ) * 100

        score = round(score, 2)

        # -----------------------------
        # Decision logic
        # -----------------------------
        if mandatory_coverage < self.min_mandatory_coverage:
            decision = "Reject"
        elif score >= 75:
            decision = "Strong Match"
        elif score >= 60:
            decision = "Potential Match"
        else:
            decision = "Weak Match"

        # -----------------------------
        # Explanation
        # -----------------------------
        explanation = (
            f"Mandatory coverage: {round(mandatory_coverage*100,1)}%. "
            f"Optional coverage: {round(optional_coverage*100,1)}%. "
            f"Missing mandatory skills: "
            f"{', '.join(sorted(missing_mandatory)) if missing_mandatory else 'None'}."
        )

        return AlignmentResult(
            score=score,
            mandatory_coverage=round(mandatory_coverage, 3),
            optional_coverage=round(optional_coverage, 3),
            missing_mandatory=missing_mandatory,
            matched_optional=matched_optional,
            decision=decision,
            explanation=explanation
        )
