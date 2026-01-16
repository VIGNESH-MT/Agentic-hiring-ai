from dataclasses import dataclass
from typing import Dict


@dataclass
class ConfidenceResult:
    confidence: float
    uncertainty_level: str
    abstain: bool
    explanation: str


class ConfidenceAgent:
    """
    Estimates confidence and uncertainty of hiring decisions.
    """

    def estimate(
        self,
        *,
        model_score: float,
        bias_adjusted_score: float,
        coverage_ratio: float,
        risk_band: str,
    ) -> ConfidenceResult:
        """
        model_score: raw model score (0–100)
        bias_adjusted_score: bias-corrected score (0–100)
        coverage_ratio: matched_skills / total_required (0–1)
        risk_band: HIRE / HOLD / REJECT
        """

        # Normalize scores
        score_gap = abs(model_score - bias_adjusted_score) / 100
        coverage_penalty = 1 - coverage_ratio

        # Simple, interpretable confidence formula
        confidence = max(
            0.0,
            1.0 - (0.5 * score_gap + 0.5 * coverage_penalty)
        )

        # Uncertainty bands
        if confidence >= 0.75:
            uncertainty = "LOW"
            abstain = False
        elif confidence >= 0.45:
            uncertainty = "MEDIUM"
            abstain = risk_band == "HIRE"
        else:
            uncertainty = "HIGH"
            abstain = True

        explanation = (
            f"Confidence is {round(confidence, 2)} due to "
            f"{round(coverage_ratio*100)}% skill coverage and "
            f"{round(score_gap*100)}% bias adjustment shift."
        )

        return ConfidenceResult(
            confidence=round(confidence, 3),
            uncertainty_level=uncertainty,
            abstain=abstain,
            explanation=explanation,
        )
