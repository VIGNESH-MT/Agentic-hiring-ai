# src/agents/causal_sensitivity_agent.py

from dataclasses import dataclass
from typing import List, Set, Callable


@dataclass
class SkillSensitivity:
    skill: str
    impact: float
    sensitivity: float
    critical: bool
    stability_class: str


@dataclass
class SensitivityReport:
    base_score: float
    threshold: float
    decision_stability: str
    skill_sensitivities: List[SkillSensitivity]
    explanation: str


class CausalSensitivityAgent:
    """
    Evaluates how sensitive a hiring decision is to individual skill perturbations.
    """

    def analyze(
        self,
        resume_skills: Set[str],
        role_skills: Set[str],
        base_score: float,
        threshold: float,
        score_fn: Callable[[Set[str], Set[str]], float],
        max_score: float = 100.0,
    ) -> SensitivityReport:

        resume_skills = resume_skills or set()
        role_skills = role_skills or set()

        sensitivities: List[SkillSensitivity] = []

        for skill in sorted(role_skills):
            if skill in resume_skills:
                new_skills = resume_skills - {skill}
            else:
                new_skills = resume_skills | {skill}

            new_score = float(score_fn(new_skills, role_skills))
            impact = round(new_score - base_score, 2)
            sensitivity = round(abs(impact) / max_score, 3)

            critical = (
                (base_score >= threshold and new_score < threshold)
                or (base_score < threshold and new_score >= threshold)
            )

            if sensitivity >= 0.3:
                stability_class = "FRAGILE"
            elif sensitivity >= 0.15:
                stability_class = "MODERATE"
            else:
                stability_class = "ROBUST"

            sensitivities.append(
                SkillSensitivity(
                    skill=skill,
                    impact=impact,
                    sensitivity=sensitivity,
                    critical=critical,
                    stability_class=stability_class,
                )
            )

        critical_skills = [s for s in sensitivities if s.critical]

        if critical_skills:
            decision_stability = "FRAGILE"
        elif any(s.stability_class == "MODERATE" for s in sensitivities):
            decision_stability = "MODERATE"
        else:
            decision_stability = "ROBUST"

        explanation = (
            f"The decision is classified as **{decision_stability}**. "
            f"{len(critical_skills)} skill(s) have the potential to flip the outcome. "
            f"This indicates that the decision "
            f"{'requires careful review' if decision_stability != 'ROBUST' else 'is stable under perturbations'}."
        )

        return SensitivityReport(
            base_score=base_score,
            threshold=threshold,
            decision_stability=decision_stability,
            skill_sensitivities=sorted(
                sensitivities, key=lambda s: abs(s.impact), reverse=True
            ),
            explanation=explanation,
        )
