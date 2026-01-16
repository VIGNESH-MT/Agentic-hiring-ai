# src/agents/hiring_committee_agent.py

from dataclasses import dataclass
from typing import List


@dataclass
class CommitteeDecision:
    persona: str
    verdict: str
    reasoning: str
    confidence: str


class HiringCommitteeAgent:
    """
    Simulates a multi-stakeholder hiring committee.
    Deterministic, explainable, and audit-safe.
    """

    def evaluate(
        self,
        match_score: float,
        hiring_risk: float,
        offer_probability: float,
        critical_gaps: List[str],
    ) -> List[CommitteeDecision]:

        decisions = []

        # -------------------------
        # Hiring Manager
        # -------------------------
        hm_verdict = (
            "Hire" if match_score >= 70 else "Hold"
        )
        decisions.append(
            CommitteeDecision(
                persona="Hiring Manager",
                verdict=hm_verdict,
                reasoning=(
                    f"Candidate meets core skill expectations "
                    f"with match score {match_score}%."
                ),
                confidence="High" if match_score >= 80 else "Medium",
            )
        )

        # -------------------------
        # Tech Lead
        # -------------------------
        tl_verdict = (
            "Hire" if not critical_gaps else "Conditional Hire"
        )
        decisions.append(
            CommitteeDecision(
                persona="Tech Lead",
                verdict=tl_verdict,
                reasoning=(
                    "Technical fundamentals are solid; "
                    f"gaps identified in {', '.join(critical_gaps[:2]) or 'none'}."
                ),
                confidence="Medium",
            )
        )

        # -------------------------
        # HR
        # -------------------------
        hr_verdict = (
            "Proceed" if hiring_risk < 60 else "Caution"
        )
        decisions.append(
            CommitteeDecision(
                persona="HR",
                verdict=hr_verdict,
                reasoning=(
                    f"Hiring risk assessed at {hiring_risk}%, "
                    "within acceptable limits."
                ),
                confidence="Medium",
            )
        )

        # -------------------------
        # Finance
        # -------------------------
        fin_verdict = (
            "Approve" if offer_probability >= 60 else "Review"
        )
        decisions.append(
            CommitteeDecision(
                persona="Finance",
                verdict=fin_verdict,
                reasoning=(
                    f"Projected offer probability of {offer_probability}% "
                    "supports cost justification."
                ),
                confidence="Medium",
            )
        )

        return decisions
