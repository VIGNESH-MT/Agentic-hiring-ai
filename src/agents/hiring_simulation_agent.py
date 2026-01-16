from dataclasses import dataclass
from typing import List, Set, Callable


@dataclass
class SkillSimulation:
    skill: str
    new_score: float
    delta: float
    decision_change: str


@dataclass
class SimulationReport:
    base_score: float
    simulations: List[SkillSimulation]
    top_recommendations: List[str]
    explanation: str


class HiringSimulationAgent:
    """
    Simulates candidate upskilling scenarios and estimates hiring outcome changes.
    """

    def simulate(
        self,
        resume_skills: Set[str],
        role_skills: Set[str],
        base_score: float,
        score_fn: Callable,
        hire_threshold: float = 70.0,
    ) -> SimulationReport:

        simulations: List[SkillSimulation] = []

        missing_skills = role_skills - resume_skills

        for skill in missing_skills:
            new_skills = resume_skills | {skill}
            new_score = score_fn(new_skills, role_skills)
            delta = round(new_score - base_score, 2)

            if base_score < hire_threshold and new_score >= hire_threshold:
                decision_change = "CROSSES_HIRE_THRESHOLD"
            elif delta > 0:
                decision_change = "POSITIVE_IMPACT"
            else:
                decision_change = "NO_IMPACT"

            simulations.append(
                SkillSimulation(
                    skill=skill,
                    new_score=new_score,
                    delta=delta,
                    decision_change=decision_change,
                )
            )

        # Rank by impact
        simulations = sorted(simulations, key=lambda s: s.delta, reverse=True)

        top_recommendations = [
            s.skill for s in simulations if s.delta > 0
        ][:5]

        explanation = (
            "The hiring simulation evaluates the marginal impact of acquiring "
            "each missing skill. Skills are ranked by their ability to improve "
            "the candidate’s match score and cross hiring thresholds."
        )

        return SimulationReport(
            base_score=base_score,
            simulations=simulations,
            top_recommendations=top_recommendations,
            explanation=explanation,
        )
