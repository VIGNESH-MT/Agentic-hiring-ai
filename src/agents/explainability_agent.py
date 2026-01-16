from dataclasses import dataclass
from typing import List, Dict, Set


@dataclass
class ExplanationResult:
    final_score: float
    base_score: float
    bias_adjustment: float
    matched_skills: List[str]
    missing_skills: List[str]
    bias_flags: Dict[str, bool]
    narrative: str


class ExplainabilityAgent:
    """
    Converts model outputs into recruiter-grade explanations.
    Staff / Principal-level explainability layer.
    """

    def generate(
        self,
        base_score: float,
        bias_adjusted_score: float,
        resume_skills: Set[str],
        jd_skills: Set[str],
        bias_flags: Dict[str, bool],
    ) -> ExplanationResult:

        matched = sorted(resume_skills & jd_skills)
        missing = sorted(jd_skills - resume_skills)

        bias_delta = round(bias_adjusted_score - base_score, 2)

        narrative = self._build_narrative(
            base_score=base_score,
            final_score=bias_adjusted_score,
            matched_skills=matched,
            missing_skills=missing,
            bias_flags=bias_flags,
            bias_delta=bias_delta,
        )

        return ExplanationResult(
            final_score=bias_adjusted_score,
            base_score=base_score,
            bias_adjustment=bias_delta,
            matched_skills=matched,
            missing_skills=missing,
            bias_flags=bias_flags,
            narrative=narrative,
        )

    def _build_narrative(
        self,
        base_score: float,
        final_score: float,
        matched_skills: List[str],
        missing_skills: List[str],
        bias_flags: Dict[str, bool],
        bias_delta: float,
    ) -> str:
        """
        Human-readable explanation with bias transparency.
        """

        explanation = []
        explanation.append(
            f"The candidate initially scored {base_score}% based on direct skill alignment."
        )

        if matched_skills:
            explanation.append(
                f"Strong alignment was observed in: {', '.join(matched_skills[:6])}."
            )

        if missing_skills:
            explanation.append(
                f"Skill gaps identified include: {', '.join(missing_skills[:6])}."
            )

        active_biases = [k for k, v in bias_flags.items() if v]

        if active_biases:
            explanation.append(
                f"The score was adjusted by +{bias_delta}% due to detected bias risks "
                f"({', '.join(active_biases)}), ensuring fairness."
            )

        explanation.append(
            f"The final match score is {final_score}%, reflecting a bias-aware evaluation."
        )

        return " ".join(explanation)
