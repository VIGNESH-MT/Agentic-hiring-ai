# src/agents/audit_trail_agent.py

import json
import uuid
from datetime import datetime
from typing import Dict, Any


class AuditTrailAgent:
    """
    Produces immutable audit records for hiring decisions.
    """

    SYSTEM_VERSION = "v1.0.0"

    def generate(
        self,
        candidate_snapshot: Dict[str, Any],
        role: str,
        scores: Dict[str, float],
        bias_diagnostics: Dict[str, Any],
        committee_decisions: Any,
        final_decision: Dict[str, Any],
    ) -> Dict[str, Any]:

        audit_record = {
            "audit_id": str(uuid.uuid4()),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "candidate_snapshot": candidate_snapshot,
            "role_evaluated": role,
            "scores": scores,
            "bias_diagnostics": bias_diagnostics,
            "committee_decisions": [
                d.__dict__ for d in committee_decisions
            ],
            "final_decision": final_decision,
            "system_version": self.SYSTEM_VERSION,
        }

        return audit_record

    def persist(
        self,
        audit_record: Dict[str, Any],
        path: str = "outputs/audit_trail.json"
    ) -> None:

        with open(path, "w", encoding="utf-8") as f:
            json.dump(audit_record, f, indent=2)
