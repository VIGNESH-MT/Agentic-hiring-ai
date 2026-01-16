"""
MCP Resume Match Agent
---------------------

Enterprise-grade orchestration layer that coordinates MCP tools
to produce recruiter-facing, explainable match decisions.

Design goals:
- Deterministic behavior
- Defensive validation
- Stable return contract for UI
- No UI or Streamlit dependencies
"""

from typing import List, Dict

from mcp_server.schemas import (
    ExtractSkillsRequest,
    MatchScoreRequest,
)

from mcp_server.server import MCP_TOOLS


class MCPResumeMatchAgent:
    """
    Orchestrates MCP tools for recruiter-facing workflows.

    This class acts as a *decision layer*:
    - It does NOT parse resumes directly
    - It does NOT perform UI rendering
    - It coordinates tools and aggregates results
    """

    def __init__(self) -> None:
        # Validate tool availability at initialization time
        required_tools = {
            "resume.extract_skills",
            "match.score",
        }

        missing = required_tools - set(MCP_TOOLS.keys())
        if missing:
            raise RuntimeError(
                f"MCP tools missing at startup: {missing}. "
                "Ensure MCP server is correctly initialized."
            )

    def run(self, resume_text: str, role_skills: List[str]) -> Dict:
        """
        Execute the MCP workflow.

        Parameters
        ----------
        resume_text : str
            Raw resume text extracted from PDF.
        role_skills : List[str]
            Canonical skill list for the selected role.

        Returns
        -------
        Dict with keys:
            - score (float)
            - matched_skills (List[str])
            - missing_skills (List[str])
            - summary (str)
        """

        # -------------------------
        # Defensive input validation
        # -------------------------
        if not isinstance(resume_text, str) or not resume_text.strip():
            return self._empty_result(
                reason="Empty or invalid resume text"
            )

        if not role_skills:
            return self._empty_result(
                reason="No role skills provided"
            )

        # -------------------------
        # 1. Extract resume skills
        # -------------------------
        extract_request = ExtractSkillsRequest(
            resume_text=resume_text
        )

        extract_response = MCP_TOOLS["resume.extract_skills"](
            extract_request
        )

        resume_skills = [
            s.skill for s in extract_response.skills
            if isinstance(s.skill, str)
        ]

        # -------------------------
        # 2. Score match
        # -------------------------
        score_request = MatchScoreRequest(
            resume_skills=resume_skills,
            role_skills=role_skills,
        )

        score_response = MCP_TOOLS["match.score"](
            score_request
        )

        # -------------------------
        # 3. Assemble explanation
        # -------------------------
        score = float(score_response.score)

        matched = list(score_response.matched_skills)
        missing = list(score_response.missing_skills)

        summary = self._build_summary(
            score=score,
            matched=matched,
            missing=missing,
        )

        return {
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "summary": summary,
        }

    # --------------------------------------------------
    # Helper methods (private)
    # --------------------------------------------------
    def _empty_result(self, reason: str) -> Dict:
        """
        Return a safe, UI-compatible empty result.
        """
        return {
            "score": 0.0,
            "matched_skills": [],
            "missing_skills": [],
            "summary": (
                "Unable to compute match score. "
                f"Reason: {reason}."
            ),
        }

    def _build_summary(
        self,
        score: float,
        matched: List[str],
        missing: List[str],
    ) -> str:
        """
        Generate a recruiter-facing explanation.
        """

        matched_text = (
            ", ".join(matched)
            if matched else "No strong matches identified"
        )

        missing_text = (
            ", ".join(missing)
            if missing else "No critical gaps detected"
        )

        return (
            "Recruiter Skill Match Summary\n\n"
            f"Overall Match Score: {score}%\n\n"
            f"Matched Skills: {matched_text}\n\n"
            f"Missing Skills: {missing_text}\n\n"
            "This score represents skill coverage only and "
            "should be interpreted as a decision-support signal."
        )
