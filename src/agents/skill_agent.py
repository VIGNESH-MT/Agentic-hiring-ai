# src/agents/skill_agent.py

from typing import Dict, List, Set
from dataclasses import dataclass

from src.matcher import SkillMatcher


@dataclass
class SkillExtractionResult:
    """
    Canonical output of SkillAgent.
    This object is passed downstream to other agents.
    """
    skills: Set[str]
    detailed_skills: List[Dict]
    evidence_map: Dict[str, str]


class SkillAgent:
    """
    Staff-level Skill Extraction Agent.

    Responsibilities:
    - Invoke SkillMatcher
    - Enforce confidence threshold
    - Enforce max-skill constraint
    - Guarantee clean, explainable output
    """

    def __init__(
        self,
        matcher: SkillMatcher,
        confidence_threshold: float = 0.15,
        max_skills: int = 5
    ):
        self.matcher = matcher
        self.confidence_threshold = confidence_threshold
        self.max_skills = max_skills

    def extract(self, text: str) -> SkillExtractionResult:
        """
        Extracts high-signal skills from unstructured text.
        """

        raw_skills = self.matcher.extract_resume_skills(text)

        # 1. Confidence filter
        filtered = [
            s for s in raw_skills
            if s.get("confidence", 0) >= self.confidence_threshold
        ]

        # 2. Sort by confidence (descending)
        filtered.sort(key=lambda x: x["confidence"], reverse=True)

        # 3. Apply max-skill constraint
        capped = filtered[: self.max_skills]

        # 4. Canonical skill set
        skill_set = {s["skill"] for s in capped}

        # 5. Evidence map (skill → snippet)
        evidence_map = {
            s["skill"]: s.get("evidence_snippet", "")
            for s in capped
        }

        return SkillExtractionResult(
            skills=skill_set,
            detailed_skills=capped,
            evidence_map=evidence_map
        )
