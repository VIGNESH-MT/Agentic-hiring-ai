from dataclasses import dataclass
from typing import Dict


@dataclass
class PanelDecision:
    panel_decision: str
    panel_confidence: float
    votes: Dict[str, str]
    rationale: str


class HiringPanelAgent:
    """
    Aggregates recruiter persona decisions into a final hiring panel outcome.
    """

    def aggregate(
        self,
        persona_results: Dict[str, object]
    ) -> PanelDecision:

        votes = {}
        score_sum = 0.0

        for persona, result in persona_results.items():
            votes[persona] = result.decision
            score_sum += result.offer_probability

        total_members = len(persona_results)
        proceed_votes = sum(
            1 for v in votes.values() if v == "PROCEED"
        )

        panel_confidence = round(score_sum / total_members, 2)

        if proceed_votes >= (total_members // 2 + 1):
            panel_decision = "PROCEED"
        elif proceed_votes == 0:
            panel_decision = "REJECT"
        else:
            panel_decision = "HOLD"

        rationale = (
            f"{proceed_votes} of {total_members} panel members recommend proceeding. "
            f"Panel confidence is {panel_confidence}."
        )

        return PanelDecision(
            panel_decision=panel_decision,
            panel_confidence=panel_confidence,
            votes=votes,
            rationale=rationale,
        )
