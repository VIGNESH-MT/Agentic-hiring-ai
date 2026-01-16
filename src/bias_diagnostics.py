# src/bias_diagnostics.py

import pandas as pd
import numpy as np


class BiasDiagnostics:
    """
    Computes bias and correlation signals for recruiter-facing diagnostics.
    This does NOT make hiring decisions.
    """

    def __init__(self, resume_skills, role_skills_map, match_scores):
        """
        Parameters
        ----------
        resume_skills : list of dict
            Output of matcher.extract_resume_skills
        role_skills_map : dict
            ROLE_SKILLS dictionary
        match_scores : dict
            {role_name: match_score}
        """
        self.resume_skills = resume_skills
        self.role_skills_map = role_skills_map
        self.match_scores = match_scores

    # -------------------------------
    # Skill Count Bias
    # -------------------------------
    def skill_count_bias(self):
        skill_count = len(self.resume_skills)
        avg_score = np.mean(list(self.match_scores.values()))

        return {
            "skill_count": skill_count,
            "average_match_score": round(avg_score, 2)
        }

    # -------------------------------
    # Skill Diversity Bias
    # -------------------------------
    def skill_diversity_bias(self):
        skills = [s["skill"] for s in self.resume_skills]
        diversity = len(set(skills)) / max(len(skills), 1)

        return {
            "skill_diversity_ratio": round(diversity, 2)
        }

    # -------------------------------
    # Role Advantage Bias
    # -------------------------------
    def role_advantage_bias(self):
        rows = []

        for role, score in self.match_scores.items():
            role_skill_count = len(self.role_skills_map.get(role, []))

            rows.append({
                "role": role,
                "match_score": score,
                "required_skill_count": role_skill_count
            })

        df = pd.DataFrame(rows)

        if df.empty:
            return None

        corr = df["match_score"].corr(df["required_skill_count"])

        return {
            "correlation_required_skills_vs_score": (
                None if pd.isna(corr) else round(corr, 3)
            ),
            "table": df
        }

    # -------------------------------
    # Global Bias Summary
    # -------------------------------
    def summary(self):
        return {
            "skill_count_bias": self.skill_count_bias(),
            "skill_diversity_bias": self.skill_diversity_bias(),
            "role_advantage_bias": self.role_advantage_bias(),
            "disclaimer": (
                "Bias diagnostics are indicative signals only. "
                "No protected attributes are used."
            )
        }
