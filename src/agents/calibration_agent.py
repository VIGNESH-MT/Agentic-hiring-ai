# src/agents/calibration_agent.py

from dataclasses import dataclass
from typing import Literal


RiskBand = Literal[
    "STRONG_HIRE",
    "HIRE",
    "BORDERLINE",
    "WEAK_FIT",
    "REJECT",
]


@dataclass
class CalibrationResult:
    raw_score: float
    calibrated_score: float
    risk_band: RiskBand
    hiring_recommendation: str
    human_review_required: bool


class CalibrationAgent:
    """
    Converts bias-adjusted scores into executive-readable hiring outcomes.

    POLICY-DRIVEN:
    - Deterministic
    - Auditable
    - Non-ML
    """

    def calibrate(self, score: float) -> CalibrationResult:
        score = round(float(score), 2)

        if score >= 85:
            return CalibrationResult(
                raw_score=score,
                calibrated_score=score,
                risk_band="STRONG_HIRE",
                hiring_recommendation="Fast-track candidate to final interview.",
                human_review_required=False,
            )

        if score >= 70:
            return CalibrationResult(
                raw_score=score,
                calibrated_score=score,
                risk_band="HIRE",
                hiring_recommendation="Proceed with standard interview loop.",
                human_review_required=False,
            )

        if score >= 55:
            return CalibrationResult(
                raw_score=score,
                calibrated_score=score,
                risk_band="BORDERLINE",
                hiring_recommendation="Senior recruiter or hiring manager review required.",
                human_review_required=True,
            )

        if score >= 40:
            return CalibrationResult(
                raw_score=score,
                calibrated_score=score,
                risk_band="WEAK_FIT",
                hiring_recommendation="Do not proceed unless exceptional non-technical evidence exists.",
                human_review_required=True,
            )

        return CalibrationResult(
            raw_score=score,
            calibrated_score=score,
            risk_band="REJECT",
            hiring_recommendation="Reject candidate at screening stage.",
            human_review_required=False,
        )
