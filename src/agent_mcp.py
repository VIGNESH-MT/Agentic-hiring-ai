from mcp_server.schemas import (
    ExtractSkillsRequest,
    SkillSearchRequest,
    MatchScoreRequest
)
from mcp_server.server import MCP_TOOLS


class MCPResumeMatchAgent:
    """
    Orchestrates MCP tools for recruiter-facing workflows.
    """

    def run(self, resume_text: str, role_skills: list) -> dict:
        # 1. Extract skills
        extract_resp = MCP_TOOLS["resume.extract_skills"](
            ExtractSkillsRequest(resume_text=resume_text)
        )

        resume_skills = [s.skill for s in extract_resp.skills]

        # 2. Score match
        score_resp = MCP_TOOLS["match.score"](
            MatchScoreRequest(
                resume_skills=resume_skills,
                role_skills=role_skills
            )
        )

        # 3. Generate recruiter summary
        summary = f"""
### Recruiter Skill Match Summary

**Match Score:** {score_resp.score}%

**Matched Skills:** {", ".join(score_resp.matched_skills)}

**Missing Skills:** {", ".join(score_resp.missing_skills)}
        """

        return {
            "score": score_resp.score,
            "summary": summary.strip()
        }
