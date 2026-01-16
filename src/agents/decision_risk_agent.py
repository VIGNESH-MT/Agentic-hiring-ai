from dataclasses import dataclass
from typing import List


@dataclass
class DecisionRiskProfile:
    decision: str
    risk_level: str
    confidence: float
    stability: str
    governance_notes: List[str]
    recruiter_summary: str


class DecisionRiskAgent:
    """
    Aggregates all decision diagnostics into a final risk-aware hiring decision.
    Staff-level governance layer.
    """

    def assess(
        self,
        final_score: float,
        risk_band: str,
        uncertainty: float,
        decision_stability: str,
        bias_flags: dict,
        counterfactual_available: bool,
    ) -> DecisionRiskProfile:

        notes = []

        # --- Bias risks ---
        for k, v in bias_flags.items():
            if v:
                notes.append(f"Bias risk detected: {k.replace('_', ' ')}")

        # --- Stability ---
        if decision_stability == "FRAGILE":
            notes.append("Decision is sensitive to small skill changes")

        # --- Uncertainty ---
        if uncertainty >= 0.3:
            notes.append("Prediction uncertainty exceeds safe threshold")

        # --- Counterfactual ---
        if counterfactual_available:
            notes.append("Decision can be flipped with feasible skill additions")

        # --- Risk level ---
        if risk_band == "HIGH" or decision_stability == "FRAGILE":
            risk_level = "HIGH"
            decision = "REVIEW"
        elif risk_band == "MEDIUM":
            risk_level = "MEDIUM"
            decision = "REVIEW"
        else:
            risk_level = "LOW"
            decision = "HIRE" if final_score >= 70 else "REVIEW"

        confidence = round(1.0 - uncertainty, 2)

        recruiter_summary = (
            f"The candidate received a final score of {final_score}%. "
            f"The decision is classified as {decision} with a {risk_level} risk profile. "
            f"The decision stability is {decision_stability}. "
            f"{' '.join(notes) if notes else 'No significant governance risks detected.'}"
        )

        return DecisionRiskProfile(
            decision=decision,
            risk_level=risk_level,
            confidence=confidence,
            stability=decision_stability,
            governance_notes=notes,
            recruiter_summary=recruiter_summary,
        )
