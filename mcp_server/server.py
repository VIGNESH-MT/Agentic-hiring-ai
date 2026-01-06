from mcp_server.tools.resume_tools import extract_skills_tool
from mcp_server.tools.skills_tools import search_skills_tool
from mcp_server.tools.match_tools import match_score_tool

MCP_TOOLS = {
    "resume.extract_skills": extract_skills_tool,
    "skills.search": search_skills_tool,
    "match.score": match_score_tool
}
