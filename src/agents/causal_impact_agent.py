from typing import Dict, List


class CausalImpactAgent:
    """
    Estimates marginal causal impact of individual skills
    on the hiring decision score.
    """

    def analyze(
        self,
        *,
        resume_skills: set,
        role_skills: set,
        base_score: float,
        score_fn,
    ) -> Dict:
        """
        resume_skills: current skills
        role_skills: required skills
        base_score: current score (0–100)
        score_fn: callable that recomputes score given skills
        """

        impacts = []

        # --- Impact of adding missing skills ---
        for skill in role_skills - resume_skills:
            new_skills = resume_skills | {skill}
            new_score = score_fn(new_skills, role_skills)

            impacts.append({
                "skill": skill,
                "action": "ADD",
                "impact": round(new_score - base_score, 2),
                "new_score": round(new_score, 2),
            })

        # --- Impact of removing existing skills ---
        for skill in resume_skills:
            reduced_skills = resume_skills - {skill}
            new_score = score_fn(reduced_skills, role_skills)

            impacts.append({
                "skill": skill,
                "action": "REMOVE",
                "impact": round(new_score - base_score, 2),
                "new_score": round(new_score, 2),
            })

        # Sort by absolute impact
        impacts = sorted(
            impacts,
            key=lambda x: abs(x["impact"]),
            reverse=True
        )

        return {
            "base_score": round(base_score, 2),
            "top_drivers": impacts[:5],
            "explanation": (
                "Skills are ranked by marginal impact on the decision score "
                "using counterfactual perturbations."
            ),
        }
