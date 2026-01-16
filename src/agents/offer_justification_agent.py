# src/agents/offer_justification_agent.py

from dataclasses import dataclass
from typing import List


@dataclass
class OfferJustification:
    recommendation: str
    justification: str
    risks: List[str]
    mitigation_plan: List[str]
    confidence_level: str


class OfferJustificationAgent:
    """
    Produces executive-level hiring justifications.
    Converts technical signals into board-safe decisions.
    """

    def generate(
        self,
        committee_decisions,
        match_score: float,
        hiring_risk: float,
        offer_probability: float,
        critical_gaps: List[str],
    ) -> OfferJustification:

        approvals = sum(
            1 for d in committee_decisions
            if d.verdict.lower() in {"hire", "approve", "proceed"}
        )

        if approvals >= 3 and offer_probability >= 65:
            recommendation = "APPROVE OFFER"
            confidence = "High"
        elif approvals >= 2:
            recommendation = "CONDITIONAL OFFER"
            confidence = "Medium"
        else:
            recommendation = "DO NOT PROCEED"
            confidence = "Low"

        justification = (
            f"The hiring committee evaluation indicates a match score of "
            f"{match_score}% with an estimated offer probability of "
            f"{offer_probability}%. "
            f"{approvals} out of {len(committee_decisions)} stakeholders "
            f"support proceeding. "
            f"Identified risks are considered manageable within current hiring policy."
        )

        risks = []
        if hiring_risk >= 50:
            risks.append("Elevated hiring risk due to skill gaps or role mismatch.")
        if critical_gaps:
            risks.append(
                f"Technical gaps identified in {', '.join(critical_gaps)}."
            )

        mitigation_plan = []
        if critical_gaps:
            mitigation_plan.append(
                "Address skill gaps through onboarding plan and first-90-day objectives."
            )
        if hiring_risk >= 50:
            mitigation_plan.append(
                "Schedule early performance checkpoints and mentoring support."
            )

        if not mitigation_plan:
            mitigation_plan.append("No additional mitigation required.")

        return OfferJustification(
            recommendation=recommendation,
            justification=justification,
            risks=risks or ["No material risks identified."],
            mitigation_plan=mitigation_plan,
            confidence_level=confidence,
        )
