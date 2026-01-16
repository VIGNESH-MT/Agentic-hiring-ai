# src/agents/bias_aware_agent.py

from dataclasses import dataclass
from typing import Set, Dict


@dataclass
class BiasAdjustedResult:
    original_score: float
    adjusted_score: float
    bias_flags: Dict[str, bool]
    adjustment_reasoning: str


class BiasAwareAgent:
    """
    Bias-aware scoring adjustment layer.

    PURPOSE:
    - Audits potential unfair penalties
    - Applies bounded, transparent corrections
    - NEVER replaces alignment logic

    This module exists for governance, not optimization.
    """

    def __init__(self, max_adjustment: float = 10.0):
        self.max_adjustment = max_adjustment

    def adjust(
        self,
        resume_skills: Set[str],
        jd_skills: Set[str],
        original_score: float
    ) -> BiasAdjustedResult:

        resume_skills = resume_skills or set()
        jd_skills = jd_skills or set()

        bias_flags = {
            "jd_inflation_detected": False,
            "skill_density_penalty": False,
            "vocabulary_bias_risk": False,
        }

        adjustment = 0.0

        # -----------------------------
        # JD inflation detection
        # -----------------------------
        if len(jd_skills) >= 18:
            bias_flags["jd_inflation_detected"] = True
            adjustment += 4.0

        # -----------------------------
        # Skill density penalty check
        # -----------------------------
        if len(resume_skills) < 8 and original_score < 65:
            bias_flags["skill_density_penalty"] = True
            adjustment += 3.0

        # -----------------------------
        # Vocabulary bias heuristic
        # -----------------------------
        generic_tokens = {"python", "sql", "ml", "ai"}
        if resume_skills & generic_tokens and original_score < 70:
            bias_flags["vocabulary_bias_risk"] = True
            adjustment += 3.0

        # -----------------------------
        # Cap adjustment
        # -----------------------------
        adjustment = min(adjustment, self.max_adjustment)
        adjusted_score = min(round(original_score + adjustment, 2), 100.0)

        triggered = [k for k, v in bias_flags.items() if v]

        reasoning = (
            f"Bias audit applied. Original score {original_score} adjusted by +{adjustment}. "
            f"Triggered checks: {', '.join(triggered) if triggered else 'None'}. "
            f"All adjustments are bounded and require human oversight."
        )

        return BiasAdjustedResult(
            original_score=original_score,
            adjusted_score=adjusted_score,
            bias_flags=bias_flags,
            adjustment_reasoning=reasoning,
        )
