from mcp_server.schemas import ExtractSkillsRequest
from mcp_server.tools.resume_tools import extract_skills_tool


def test_extract_skills_tool():
    req = ExtractSkillsRequest(
        resume_text="Experienced in Python and SQL"
    )
    resp = extract_skills_tool(req)

    assert len(resp.skills) > 0
    assert any(s.skill == "python" for s in resp.skills)
