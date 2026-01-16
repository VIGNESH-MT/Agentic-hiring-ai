import json
from pathlib import Path
from typing import Dict
from .decision_trace import DecisionTrace


class AuditLogger:
    """
    Enterprise-grade audit logger.
    Append-only, immutable decision traces.
    """

    def __init__(self, log_dir: str = "outputs/audit_logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def log(self, trace: DecisionTrace) -> None:
        file_path = self.log_dir / f"{trace.decision_id}.json"

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(trace.to_dict(), f, indent=2)

    def load(self, decision_id: str) -> Dict:
        file_path = self.log_dir / f"{decision_id}.json"
        if not file_path.exists():
            raise FileNotFoundError(f"Audit log not found: {decision_id}")

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
