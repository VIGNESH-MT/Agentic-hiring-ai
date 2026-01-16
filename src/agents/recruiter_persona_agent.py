from dataclasses import dataclass
from typing import Dict


@dataclass
class PersonaDecision:
    adjusted_score: float
    offer_probability: float
    decision: str


class RecruiterPersonaAgent:
    """
    Simulates recruiter behavior under different risk tolerances.
    """

    def simulate(
        self,
        base_score: float,
        hiring_risk: float,
    ) -> Dict[str, PersonaDecision]:

        personas = {
            "Conservative Recruiter": {
                "risk_penalty": 0.6,
                "decision_threshold": 75,
            },
            "Balanced Recruiter": {
                "risk_penalty": 0.4,
                "decision_threshold": 70,
            },
            "Aggressive Recruiter": {
                "risk_penalty": 0.2,
                "decision_threshold": 65,
            },
        }

        results: Dict[str, PersonaDecision] = {}

        for persona, cfg in personas.items():
            adjusted_score = round(
                base_score - (hiring_risk * cfg["risk_penalty"]),
                2
            )

            offer_probability = round(
                max(min(adjusted_score / 100, 1.0), 0.0),
                2
            )

            decision = (
                "PROCEED"
                if adjusted_score >= cfg["decision_threshold"]
                else "HOLD"
            )

            results[persona] = PersonaDecision(
                adjusted_score=adjusted_score,
                offer_probability=offer_probability,
                decision=decision,
            )

        return results
