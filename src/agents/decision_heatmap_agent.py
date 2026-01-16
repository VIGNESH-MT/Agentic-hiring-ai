# src/agents/decision_heatmap_agent.py

from dataclasses import dataclass
from typing import List


@dataclass
class HeatmapCell:
    skill: str
    impact: float
    zone: str        # SAFE | WARNING | CRITICAL
    crosses_threshold: bool


@dataclass
class DecisionHeatmap:
    threshold: float
    cells: List[HeatmapCell]
    explanation: str


class DecisionHeatmapAgent:
    """
    Converts sensitivity + simulation outputs into
    recruiter-facing decision heatmaps.
    """

    def build(
        self,
        sensitivity_report,
        simulation_report,
        threshold: float,
    ) -> DecisionHeatmap:

        cells: List[HeatmapCell] = []

        for sim in simulation_report.simulations:
            impact = sim.delta
            new_score = sim.new_score

            if new_score >= threshold:
                zone = "CRITICAL"
            elif new_score >= threshold - 10:
                zone = "WARNING"
            else:
                zone = "SAFE"

            cells.append(
                HeatmapCell(
                    skill=sim.skill,
                    impact=impact,
                    zone=zone,
                    crosses_threshold=(
                        sim.decision_change == "CROSSES_HIRE_THRESHOLD"
                    ),
                )
            )

        explanation = (
            "This heatmap shows how individual skill changes affect "
            "the hiring decision boundary. Skills in the CRITICAL zone "
            "can independently flip the hire decision and should be "
            "prioritized by recruiters."
        )

        return DecisionHeatmap(
            threshold=threshold,
            cells=sorted(cells, key=lambda c: abs(c.impact), reverse=True),
            explanation=explanation,
        )
