from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Dict


@dataclass
class DecisionTrace:
    candidate_id: str
    role: str

    model_score: float
    bias_adjusted_score: float
    risk_band: str

    model_recommendation: str

    human_decision: Optional[str] = None
    human_reason: Optional[str] = None
    reviewer_id: Optional[str] = None

    timestamp: str = datetime.utcnow().isoformat()


class DecisionTraceAgent:
    """
    Immutable decision logging for audit, compliance, and governance.
    """

    def create_trace(
        self,
        *,
        candidate_id: str,
        role: str,
        model_score: float,
        bias_adjusted_score: float,
        risk_band: str,
        model_recommendation: str,
    ) -> DecisionTrace:
        return DecisionTrace(
            candidate_id=candidate_id,
            role=role,
            model_score=model_score,
            bias_adjusted_score=bias_adjusted_score,
            risk_band=risk_band,
            model_recommendation=model_recommendation,
        )

    def apply_human_override(
        self,
        trace: DecisionTrace,
        *,
        decision: str,
        reason: str,
        reviewer_id: str,
    ) -> DecisionTrace:
        trace.human_decision = decision
        trace.human_reason = reason
        trace.reviewer_id = reviewer_id
        return trace

    def serialize(self, trace: DecisionTrace) -> Dict:
        return asdict(trace)
