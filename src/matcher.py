import json
from rapidfuzz import fuzz
from typing import List, Dict


class SkillMatcher:
    """
    Stable hybrid skill extraction & matching engine.
    Priority: correctness > sophistication
    """

    def __init__(self, skills_catalog, indexer=None):
        self.skills_catalog = {
            s.lower().strip()
            for s in skills_catalog
            if isinstance(s, str)
        }
        self.indexer = indexer  # optional

    # ----------------------------
    # Skill hygiene
    # ----------------------------
    @staticmethod
    def is_valid_skill(skill: str) -> bool:
        return (
            isinstance(skill, str)
            and len(skill) >= 3
            and skill.isalpha()
            and not skill.isnumeric()
        )

    # ----------------------------
    # Resume skill extraction
    # ----------------------------
    def extract_resume_skills(self, resume_text: str) -> List[Dict]:
        resume_text_l = resume_text.lower()
        extracted = []

        # ---- Exact match (safe) ----
        for skill in self.skills_catalog:
            if not self.is_valid_skill(skill):
                continue

            if f" {skill} " in f" {resume_text_l} ":
                extracted.append({
                    "skill": skill,
                    "confidence": 1.0,
                    "method": "exact",
                    "evidence_snippet": skill
                })

        # ---- Fuzzy match (token-level) ----
        tokens = resume_text_l.split()

        for skill in self.skills_catalog:
            if not self.is_valid_skill(skill):
                continue

            score = max(
                (fuzz.ratio(skill, t) for t in tokens),
                default=0
            )

            if score >= 90:
                extracted.append({
                    "skill": skill,
                    "confidence": score / 100,
                    "method": "fuzzy",
                    "evidence_snippet": skill
                })

        # ---- Semantic match (OPTIONAL, SAFE) ----
        if self.indexer is not None:
            try:
                hits = self.indexer.search(resume_text, top_k=5)
                for hit in hits:
                    skill = hit.get("skill", "").lower()
                    if self.is_valid_skill(skill):
                        extracted.append({
                            "skill": skill,
                            "confidence": float(hit.get("similarity", 0)),
                            "method": "semantic",
                            "evidence_snippet": skill
                        })
            except Exception:
                # Do NOT crash the pipeline
                pass

        # ---- De-duplicate (highest confidence wins) ----
        unique = {}
        for s in extracted:
            k = s["skill"]
            if k not in unique or s["confidence"] > unique[k]["confidence"]:
                unique[k] = s

        return list(unique.values())

    # ----------------------------
    # Save extracted skills
    # ----------------------------
    def save_resume_skills(self, skills, path="outputs/resume_skills.json"):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(skills, f, indent=2)

    # ----------------------------
    # Match to role
    # ----------------------------
    def match_to_role(self, resume_skills, role_skills):
        resume_set = {s["skill"] for s in resume_skills}
        role_set = {s.lower() for s in role_skills}

        matched = sorted(resume_set & role_set)
        missing = sorted(role_set - resume_set)

        coverage = len(matched) / max(len(role_set), 1)

        report = {
            "matched_skills": matched,
            "missing_skills": missing,
            "coverage": round(coverage, 3),
            "score": round(coverage * 100, 2),
            "explanation": "Exact + fuzzy (+ optional semantic) skill matching"
        }

        with open("outputs/match_report.json", "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)

        return report
