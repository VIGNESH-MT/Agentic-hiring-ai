# src/agents/offer_probability_agent.py

from dataclasses import dataclass
from typing import Dict, Literal


RiskBand = Literal[
    "NEAR_CERTAIN",
    "STRONG",
    "UNCERTAIN",
    "LOW",
    "VERY_LOW"
]


@dataclass
class OfferProbabilityReport:
    min_probability: float
    max_probability: float
    expected_probability: float
    risk_band: RiskBand
    funnel_breakdown: Dict[str, float]
    explanation: str


class OfferProbabilityAgent:
    """
    Estimates the probability of receiving a job offer by simulating
    real-world hiring funnel behavior.

    This agent intentionally avoids ML to ensure:
    - auditability
    - explainability
    - governance readiness
    """

    def __init__(
        self,
        recruiter_noise: float = 0.08,
        interview_noise: float = 0.12,
    ):
        self.recruiter_noise = recruiter_noise
        self.interview_noise = interview_noise

    # --------------------------------------------------
    # Internal helpers
    # --------------------------------------------------
    def _clamp(self, value: float) -> float:
        return max(0.0, min(1.0, value))

    def _risk_band(self, expected: float) -> RiskBand:
        if expected >= 0.80:
            return "NEAR_CERTAIN"
        if expected >= 0.60:
            return "STRONG"
        if expected >= 0.40:
            return "UNCERTAIN"
        if expected >= 0.20:
            return "LOW"
        return "VERY_LOW"

    # --------------------------------------------------
    # Main API
    # --------------------------------------------------
    def estimate(
        self,
        score: float,
        threshold: float,
        decision_stability: str,
        human_review_required: bool,
    ) -> OfferProbabilityReport:
        """
        Parameters
        ----------
        score : float
            Bias-adjusted score (0–100)
        threshold : float
            Hiring threshold (e.g. 70)
        decision_stability : str
            ROBUST / MODERATE / FRAGILE
        human_review_required : bool
            Output from CalibrationAgent

        Returns
        -------
        OfferProbabilityReport
        """

        # -------------------------------
        # Base survival probabilities
        # -------------------------------
        resume_screen = 0.95 if score >= threshold else 0.65

        recruiter_review = (
            0.85 if score >= threshold + 10 else
            0.70 if score >= threshold else
            0.45
        )

        technical_interview = (
            0.80 if decision_stability == "ROBUST" else
            0.65 if decision_stability == "MODERATE" else
            0.50
        )

        final_decision = (
            0.75 if not human_review_required else
            0.60
        )

        # -------------------------------
        # Noise injection (human variance)
        # -------------------------------
        recruiter_review_min = self._clamp(recruiter_review - self.recruiter_noise)
        recruiter_review_max = self._clamp(recruiter_review + self.recruiter_noise)

        technical_min = self._clamp(technical_interview - self.interview_noise)
        technical_max = self._clamp(technical_interview + self.interview_noise)

        # -------------------------------
        # Funnel probability aggregation
        # -------------------------------
        min_probability = (
            resume_screen *
            recruiter_review_min *
            technical_min *
            final_decision
        )

        max_probability = (
            resume_screen *
            recruiter_review_max *
            technical_max *
            final_decision
        )

        expected_probability = round((min_probability + max_probability) / 2, 3)

        risk_band = self._risk_band(expected_probability)

        # -------------------------------
        # Explanation (executive-readable)
        # -------------------------------
        explanation = (
            f"The estimated offer probability is driven by a score of {score}, "
            f"with a hiring threshold of {threshold}. "
            f"The decision stability is **{decision_stability}**, "
            f"and human review is "
            f"{'required' if human_review_required else 'not required'}. "
            f"Recruiter and interview-stage variability introduce uncertainty, "
            f"resulting in an expected offer probability of "
            f"{round(expected_probability * 100, 1)}%."
        )

        return OfferProbabilityReport(
            min_probability=round(min_probability, 3),
            max_probability=round(max_probability, 3),
            expected_probability=expected_probability,
            risk_band=risk_band,
            funnel_breakdown={
                "resume_screen": resume_screen,
                "recruiter_review": recruiter_review,
                "technical_interview": technical_interview,
                "final_decision": final_decision,
            },
            explanation=explanation,
        )
