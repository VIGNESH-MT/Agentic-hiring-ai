from typing import List, Dict


class CounterfactualAgent:
    """
    Computes minimal changes required to flip a hiring decision.
    """

    def generate(
        self,
        *,
        resume_skills: set,
        role_skills: set,
        current_score: float,
        target_threshold: float = 70.0,
    ) -> Dict:
        """
        resume_skills: skills extracted from resume
        role_skills: skills required for role
        current_score: current match score (0–100)
        target_threshold: score needed to move to next band
        """

        if current_score >= target_threshold:
            return {
                "status": "ALREADY_ELIGIBLE",
                "message": "Candidate already meets the hiring threshold.",
                "actions": [],
            }

        missing_skills = list(role_skills - resume_skills)

        if not missing_skills:
            return {
                "status": "NO_SKILL_GAP",
                "message": "No skill gaps detected, score gap likely due to weighting.",
                "actions": [],
            }

        # Estimate score impact per skill (simple, explainable assumption)
        score_gap = target_threshold - current_score
        per_skill_gain = max(score_gap / len(missing_skills), 5)

        actions = []
        cumulative_score = current_score

        for skill in missing_skills:
            cumulative_score += per_skill_gain
            actions.append({
                "add_skill": skill,
                "estimated_new_score": round(min(cumulative_score, 100), 2),
            })
            if cumulative_score >= target_threshold:
                break

        return {
            "status": "COUNTERFACTUAL_AVAILABLE",
            "current_score": round(current_score, 2),
            "target_threshold": target_threshold,
            "actions": actions,
            "explanation": (
                "Adding the above skills is estimated to move the candidate "
                "into the next decision band."
            ),
        }
