# src/agents/agent_langchain.py

from src.agents.langchain_tools.resume_tools import extract_resume_skills
from src.agents.langchain_tools.match_tools import match_to_role
from src.agents.langchain_tools.explain_tools import explain_match


class ResumeSkillAgent:
    """
    Deterministic LangChain agent.
    Schema-safe. MCP-ready. No LLM.
    """

    def __init__(self, verbose: bool = False):
        self.verbose = verbose

    def run(self, resume_pdf_path: str, role: str) -> dict:

        skills_result = extract_resume_skills.invoke({
            "resume_pdf_path": resume_pdf_path
        })

        resume_skills = [
            s["skill"]
            for s in skills_result.get("skills", [])
        ]

        if self.verbose:
            print("Skills:", resume_skills)

        match_result = match_to_role.invoke({
            "resume_skills": resume_skills,
            "role_title": role
        })

        explanation = explain_match.invoke({
            "match_report": match_result
        })

        return explanation
