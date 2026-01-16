from dataclasses import dataclass, asdict
from typing import Dict, List
from datetime import datetime
import uuid


@dataclass
class DecisionTrace:
    decision_id: str
    timestamp_utc: str

    resume_hash: str
    jd_hash: str

    base_score: float
    bias_adjusted_score: float

    matched_skills: List[str]
    missing_skills: List[str]

    bias_flags: Dict[str, bool]

    explanation: str

    model_version: str
    pipeline_version: str

    @staticmethod
    def create(
        resume_hash: str,
        jd_hash: str,
        base_score: float,
        bias_adjusted_score: float,
        matched_skills: List[str],
        missing_skills: List[str],
        bias_flags: Dict[str, bool],
        explanation: str,
        model_version: str = "v1.0",
        pipeline_version: str = "phase2.4",
    ) -> "DecisionTrace":

        return DecisionTrace(
            decision_id=str(uuid.uuid4()),
            timestamp_utc=datetime.utcnow().isoformat(),
            resume_hash=resume_hash,
            jd_hash=jd_hash,
            base_score=base_score,
            bias_adjusted_score=bias_adjusted_score,
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            bias_flags=bias_flags,
            explanation=explanation,
            model_version=model_version,
            pipeline_version=pipeline_version,
        )

    def to_dict(self) -> Dict:
        return asdict(self)
