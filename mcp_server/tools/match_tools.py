from mcp_server.schemas import (
    MatchScoreRequest,
    MatchScoreResponse
)


def match_score_tool(
    req: MatchScoreRequest
) -> MatchScoreResponse:
    resume_set = set(req.resume_skills)
    role_set = set(req.role_skills)

    matched = sorted(resume_set & role_set)
    missing = sorted(role_set - resume_set)

    score = len(matched) / max(len(role_set), 1) * 100

    return MatchScoreResponse(
        score=round(score, 2),
        matched_skills=matched,
        missing_skills=missing
    )
