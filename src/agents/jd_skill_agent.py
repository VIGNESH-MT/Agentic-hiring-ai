# src/agents/jd_skill_agent.py

from typing import Set, Dict
from dataclasses import dataclass

from src.agents.skill_agent import SkillAgent, SkillExtractionResult


@dataclass
class JDSkillProfile:
    """
    Structured representation of JD skill requirements.
    """
    mandatory_skills: Set[str]
    optional_skills: Set[str]
    evidence_map: Dict[str, str]


class JDSkillAgent:
    """
    Staff-level Job Description Skill Agent.

    Responsibilities:
    - Extract role requirements from JD
    - Separate mandatory vs optional skills
    - Enforce stricter confidence threshold
    """

    def __init__(
        self,
        skill_agent: SkillAgent,
        mandatory_confidence: float = 0.30,
        optional_confidence: float = 0.15
    ):
        self.skill_agent = skill_agent
        self.mandatory_confidence = mandatory_confidence
        self.optional_confidence = optional_confidence

    def extract(self, jd_text: str) -> JDSkillProfile:
        """
        Extracts structured JD skill requirements.
        """

        result: SkillExtractionResult = self.skill_agent.extract(jd_text)

        mandatory = set()
        optional = set()
        evidence = {}

        for s in result.detailed_skills:
            skill = s["skill"]
            conf = s["confidence"]

            evidence[skill] = s.get("evidence_snippet", "")

            if conf >= self.mandatory_confidence:
                mandatory.add(skill)
            elif conf >= self.optional_confidence:
                optional.add(skill)

        return JDSkillProfile(
            mandatory_skills=mandatory,
            optional_skills=optional,
            evidence_map=evidence
        )
